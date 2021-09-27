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
        logger.info('Create User Model')
        user = github.get_user()
        model = GithubUsers.createFromGitHub(user)
        db.merge(model)

        logger.info(f' Repository Models (User:{user.name})')
        repositories = user.get_repos(visibility='all')
        for repository in repositories:
            model = GithubRepositories.createFromGitHub(repository)
            db.merge(model)

            logger.info(f'  Label Models (Repository:{repository.full_name})')
            labels = repository.get_labels()
            for label in labels:
                model = GithubRepositoryLabels.createFromGitHub(repository, label)
                db.merge(model)

            logger.info(f'  Pull Request Models (Repository:{repository.full_name})')
            pull_requests = repository.get_pulls(
                state='closed',
                sort='merged',
                base=repository.default_branch
            )
            for pull_request in pull_requests:
                model = GithubRepositoryPullRequests.createFromGitHub(pull_request)
                db.merge(model)

                logger.info(f'   Pull Request Label Models (#{pull_request.number})')
                pull_request_labels = pull_request.get_labels()
                for pull_request_label in pull_request_labels:
                    model = GithubRepositoryPullRequestLabels.createFromGitHub(
                        repository, pull_request, pull_request_label)
                    db.merge(model)

                logger.info(f'   Review Models (#{pull_request.number})')
                reviews = pull_request.get_reviews()
                for review in reviews:
                    model = GithubRepositoryPullRequestReviews.createFromGitHub(
                        repository, pull_request, review)
                    db.merge(model)

                logger.info(f'   Commit Models (#{pull_request.number})')
                commits = pull_request.get_commits()
                for commit in commits:
                    model = GithubRepositoryPullRequestCommits.createFromGitHub(
                        repository, pull_request, commit)
                    db.merge(model)

    # Update Database (organization data)
    if args.update_org_repos:
        target_org_name = os.environ.get('GH2DB_GITHUB_TARGET_ORGANIZATION_NAME', '')

        logger.info(f'Organization Model ({target_org_name})')
        organization = github.get_organization(target_org_name)
        model = GithubOrganizations.createFromGitHub(organization)
        db.merge(model)

        logger.info(f' Team Models (Organization:{organization.name})')
        teams = organization.get_teams()
        for team in teams:
            model = GithubOrganizationTeams(organization, team)
            db.merge(model)

            logger.info(f'  Team Member Models (Team:{team.name})')
            team_member = team.get_members()
            for member in team_member:
                model = GithubOrganizationTeamMembers(organization, team, member)
                db.merge(model)

        logger.info(f' Repository Models (Organization:{organization.name})')
        repositories = organization.get_repos(visibility='all')
        for repository in repositories:
            model = GithubRepositories.createFromGitHub(repository)
            db.merge(model)

            logger.info(f'  Label Models (Repository:{repository.full_name})')
            labels = repository.get_labels()
            for label in labels:
                model = GithubRepositoryLabels.createFromGitHub(repository, label)
                db.merge(model)

            logger.info(f'  Pull Request Models (Organization:{organization.name})')
            pull_requests = repository.get_pulls(
                state='closed',
                sort='merged',
                base=repository.default_branch
            )
            for pull_request in pull_requests:
                model = GithubRepositoryPullRequests.createFromGitHub(pull_request)
                db.merge(model)

                logger.info(f'   Pull Request Label Models (#{pull_request.number})')
                pull_request_labels = pull_request.get_labels()
                for pull_request_label in pull_request_labels:
                    model = GithubRepositoryPullRequestLabels.createFromGitHub(
                        repository, pull_request, pull_request_label)
                    db.merge(model)

                logger.info(f'   Review Models (#{pull_request.number})')
                reviews = pull_request.get_reviews()
                for review in reviews:
                    model = GithubRepositoryPullRequestReviews.createFromGitHub(
                        repository, pull_request, review)
                    db.merge(model)

                logger.info(f'  Commit Models (#{pull_request.number})')
                commits = pull_request.get_commits()
                for commit in commits:
                    model = GithubRepositoryPullRequestCommits.createFromGitHub(
                        repository, pull_request, commit)
                    db.merge(model)

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
