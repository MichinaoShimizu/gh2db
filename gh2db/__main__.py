from __future__ import print_function

import os
from argparse import ArgumentParser

from github import Github

from gh2db.dbbase import BaseSession
from gh2db.logger import get_module_logger
from gh2db.migration import Migration
from gh2db.model import (GithubOrganizations, GithubOrganizationTeamMembers,
                         GithubOrganizationTeams, GithubRepositories,
                         GithubRepositoryLabels,
                         GithubRepositoryPullRequestCommits,
                         GithubRepositoryPullRequestLabels,
                         GithubRepositoryPullRequestReviews,
                         GithubRepositoryPullRequests, GithubUsers)

logger = get_module_logger(__name__)


def get_option():
    parser = ArgumentParser()
    parser.add_argument('--update_user_repos', action='store_true', help='Update User Data')
    parser.add_argument('--update_org_repos', action='store_true', help='Update Organization Data')
    parser.add_argument('--create_all', action='store_true', help='Create All Tables')
    parser.add_argument('--drop_all', action='store_true', help='Drop All Tables')
    parser.add_argument('--delete_all', action='store_true', help='Delete All Table Data')
    parser.add_argument('--count_all', action='store_true', help='Count All Table Rows')
    return parser.parse_args()


def main():
    args = get_option()

    # Create tables
    if args.create_all:
        logger.info('Create all tables start')
        Migration().create_all()
        return 0

    # Drop tables
    if args.drop_all:
        logger.info('Drop all tables start')
        Migration().drop_all()
        return 0

    # Count all of table rows
    if args.count_all:
        logger.info('Count all of table rows start')
        Migration().count_all()
        return 0

    # Delete all of table rows
    if args.delete_all:
        logger.info('Delete all of table rows start')
        Migration().delete_all()
        return 0

    # GitHub API
    github = Github(os.environ.get('GH2DB_GITHUB_TOKEN', ''))
    logger.info('---------------------------')
    logger.info('GitHub API Authorized By Personal AccessToken: OK')
    logger.info('Github API Rate Limitting Information:')
    logger.info('Remaining, Limit: {}'.format(github.rate_limiting))
    logger.info('ResetTime: {}'.format(github.get_rate_limit().core.reset))
    logger.info('---------------------------')

    # Database Session
    need_db_session = args.update_user_repos or args.update_org_repos
    if need_db_session:
        db = BaseSession().session
        logger.info('Database session established')

    # Update (exeusion user data)
    if args.update_user_repos:
        logger.info('Update database(exeusion user data) start')

        # User
        logger.info('Create User Model')
        user = github.get_user()
        _user = GithubUsers()
        _user.id = user.id,
        _user.name = user.name,
        _user.url = user.url,
        _user.avatar_url = user.avatar_url,
        _user.created_at = user.created_at,
        _user.updated_at = user.updated_at,
        db.merge(_user)

        # Repositories
        logger.info('Start Create Repository Models (User:{})'.format(user.name))
        repositories = user.get_repos(visibility='all')
        for repository in repositories:
            # Repository
            _repo = GithubRepositories()
            _repo.id = repository.id
            _repo.name = repository.name
            _repo.full_name = repository.full_name
            _repo.url = repository.url
            _repo.owner = repository.owner
            _repo.default_branch = repository.default_branch
            _repo.created_at = repository.created_at
            _repo.updated_at = repository.updated_at
            db.merge(_repo)

            # Labels
            logger.info('Start Create Repository Label Models (Repository:{})'.format(repository.full_name))
            labels = repository.get_labels()
            for label in labels:
                # Label
                _label = GithubRepositoryLabels()
                _label.repisitory_id = repository.id
                _label.name = label.name
                _label.url = label.url
                _label.description = label.description
                _label.color = label.color
                db.merge(_label)

            # Pull Reuests
            logger.info('Start Create Repository Pull Request Models (Repository:{})'.format(repository.full_name))
            pull_requests = repository.get_pulls(
                state='closed',
                sort='merged',
                base=repository.default_branch
            )
            for pull_request in pull_requests:
                # Pull Reuest
                _pr = GithubRepositoryPullRequests()
                _pr.id = pull_request.id
                _pr.number = pull_request.number
                _pr.url = pull_request.url
                _pr.title = pull_request.title
                _pr.user_id = pull_request.user.id
                _pr.state = pull_request.state
                _pr.base_ref = pull_request.base.ref
                _pr.head_ref = pull_request.head.ref
                _pr.merge_commit_sha = pull_request.merge_commit_sha
                _pr.mergeable = pull_request.mergeable
                _pr.mergeable_state = pull_request.mergeable_state
                _pr.merged_user_id = pull_request.merged_by
                _pr.merged_at = pull_request.merged_at
                _pr.merged = pull_request.merged
                _pr.milestone = pull_request.milestone
                _pr.deletions = pull_request.deletions
                _pr.additions = pull_request.additions
                _pr.changed_files = pull_request.changed_files
                _pr.created_at = pull_request.created_at
                _pr.updated_at = pull_request.updated_at
                _pr.closed_at = pull_request.closed_at
                db.merge(_pr)

                # Pull Request Labels
                logger.info('Start Create Repository Pull Request Label Models (Pull Request:#{})'.format(pull_request.number))
                pull_request_labels = pull_request.get_labels()
                for pull_request_label in pull_request_labels:
                    # Pull Request Label
                    _pr_label = GithubRepositoryPullRequestLabels()
                    _pr_label.repisitory_id = repository.id
                    _pr_label.pull_request_id = pull_request.id
                    _pr_label.label_name = pull_request_label.name
                    db.merge(_pr_label)

                # Pull Request Reviews
                logger.info('Start Create Repository Pull Request Review Models (Pull Request:#{})'.format(pull_request.number))
                reviews = pull_request.get_reviews()
                for review in reviews:
                    # Pull Request Review
                    _review = GithubRepositoryPullRequestReviews()
                    _review.repisitory_id = repository.id
                    _review.pull_request_id = pull_request.id
                    _review.id = review.id
                    # _review.url = review.url
                    _review.body = review.body
                    _review.user_id = review.user.id
                    _review.state = review.state
                    _review.submitted_at = review.submitted_at
                    db.merge(_review)

                # Pull Request Commits
                logger.info('Start Create Repository Pull Request Commit Models (Pull Request:#{})'.format(pull_request.number))
                commits = pull_request.get_commits()
                for commit in commits:
                    # Pull Request Commit
                    _commit = GithubRepositoryPullRequestCommits()
                    _commit.repisitory_id = repository.id
                    _commit.pull_request_id = pull_request.id
                    _commit.comments_url = commit.comments_url
                    _commit.sha = commit.sha
                    # _commit.stats = commit.stats
                    # _commit.files = commit.files
                    _commit.url = commit.url
                    _commit.user_id = commit.committer
                    db.merge(_commit)

    # Update Database (organization data)
    if args.update_org_repos:
        logger.info('Update database(organization data)')
        target_org_name = os.environ.get('github2DB_GITHUB_TARGET_ORGANIZATION_NAME', '')

        # Organization
        logger.info('Start Create Organization Model')
        organization = github.get_organization(target_org_name)
        _org = GithubOrganizations()
        _org.id = organization.id
        _org.name = organization.name
        _org.url = organization.url
        _org.avatar_url = organization.avatar_url
        _org.created_at = organization.created_at
        _org.updated_at = organization.updated_at
        db.merge(_org)

        # Teams
        logger.info('Start Create Organization Team Models (Organization:{})'.format(organization.name))
        teams = organization.get_teams()
        for team in teams:
            # Team
            _team = GithubOrganizationTeams()
            _team.id = team.id
            _team.name = team.name
            _team.url = team.url
            _team.avatar_url = team.avatar_url
            _team.created_at = team.created_at
            _team.updated_at = team.updated_at
            db.merge(_team)

            # Team Members
            logger.info('Start Create Organization Team Member Models (Team:{})'.format(team.name))
            team_member = team.get_members()
            for member in team_member:
                _member = GithubOrganizationTeamMembers()
                _member.organization_id = organization.id
                _member.team_id = team.id
                _member.user_id = member.id
                db.merge(_member)

        # Repositories
        logger.info('Start Create Organization Repository Models (Organization:{})'.format(organization.name))
        repositories = organization.get_repos(visibility='all')
        for repository in repositories:
            # Repository
            _repo = GithubRepositories()
            _repo.id = repository.id
            _repo.name = repository.name
            _repo.full_name = repository.full_name
            _repo.url = repository.url
            _repo.owner = repository.owner
            _repo.default_branch = repository.default_branch
            _repo.created_at = repository.created_at
            _repo.updated_at = repository.updated_at
            db.merge(_repo)

            # Labels
            logger.info('Start Create Organization Repository Label Models (Repository:{})'.format(repository.full_name))
            labels = repository.get_labels()
            for label in labels:
                # Label
                _label = GithubRepositoryLabels()
                _label.repisitory_id = repository.id
                _label.name = label.name
                _label.url = label.url
                _label.description = label.description
                _label.color = label.color
                db.merge(_label)

            # Pull Requests
            logger.info('Start Create Organization Repository Pull Request Models (Organization:{})'.format(organization.name))
            pull_requests = repository.get_pulls(
                state='closed',
                sort='merged',
                base=repository.default_branch
            )
            for pull_request in pull_requests:
                # Pull Request
                _pr = GithubRepositoryPullRequests()
                _pr.id = pull_request.id
                _pr.number = pull_request.number
                _pr.url = pull_request.url
                _pr.title = pull_request.title
                _pr.user_id = pull_request.user.id
                _pr.state = pull_request.state
                _pr.base_ref = pull_request.base.ref
                _pr.head_ref = pull_request.head.ref
                _pr.merge_commit_sha = pull_request.merge_commit_sha
                _pr.mergeable = pull_request.mergeable
                _pr.mergeable_state = pull_request.mergeable_state
                _pr.merged_user_id = pull_request.merged_by
                _pr.merged_at = pull_request.merged_at
                _pr.merged = pull_request.merged
                _pr.milestone = pull_request.milestone
                _pr.deletions = pull_request.deletions
                _pr.additions = pull_request.additions
                _pr.changed_files = pull_request.changed_files
                _pr.created_at = pull_request.created_at
                _pr.updated_at = pull_request.updated_at
                _pr.closed_at = pull_request.closed_at
                db.merge(_pr)

                # Pull Request Labels
                logger.info(
                    'Start Create Organization Repository Pull Request Label Models (Pull Request:#{}'.format(pull_request.number))
                pull_request_labels = pull_request.get_labels()
                for pull_request_label in pull_request_labels:
                    # Pull Request Label
                    _pr_label = GithubRepositoryPullRequestLabels()
                    _pr_label.repisitory_id = repository.id
                    _pr_label.pull_request_id = pull_request.id
                    _pr_label.label_name = pull_request_label.name
                    db.merge(_pr_label)

                # Pull Request Reviews
                logger.info(
                    'Start Create Organization Repository Pull Request Review Models (Pull Request:#{}'.format(pull_request.number))
                reviews = pull_request.get_reviews()
                for review in reviews:
                    # Pull Request Review
                    _review = GithubRepositoryPullRequestReviews()
                    _review.repisitory_id = repository.id
                    _review.pull_request_id = pull_request.id
                    _review.id = review.id
                    # _review.url = review.url
                    _review.body = review.body
                    _review.user_id = review.user.id
                    _review.state = review.state
                    _review.submitted_at = review.submitted_at
                    db.merge(_review)

                # Pull Request Commits
                logger.info(
                    'Start Create Organization Repository Pull Request Commit Models (Pull Request:#{}'.format(pull_request.number))
                commits = pull_request.get_commits()
                for commit in commits:
                    # Pull Request Commit
                    _commit = GithubRepositoryPullRequestCommits()
                    _commit.repisitory_id = repository.id
                    _commit.pull_request_id = pull_request.id
                    _commit.comments_url = commit.comments_url
                    _commit.sha = commit.sha
                    # _commit.stats = commit.stats
                    # _commit.files = commit.files
                    _commit.url = commit.url
                    _commit.user_id = commit.committer
                    db.merge(_commit)

    if need_db_session:
        try:
            db.commit()
            logger.info('Database committed')
        except Exception as e:
            logger.info('Database commit error')
            db.rollback()
            logger.info('Database rollbacked')
            raise(e)
        finally:
            db.close()
            logger.info('Database session closed')

    return 0


if __name__ == '__main__':
    try:
        exit_code = main()
        exit(exit_code)
    except KeyboardInterrupt:
        exit(1)
    except Exception as e:
        logger.error(e)
        exit(1)
