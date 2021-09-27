from __future__ import print_function

import os
from argparse import ArgumentParser

from github import Github

from gh2db.dbbase import BaseSession
from gh2db.logger import get_module_logger
from gh2db.migration import Migration
from gh2db.model import (GithubOrganization, GithubOrganizationRepository,
                         GithubOrganizationTeam, GithubUser,
                         GithubUserRepository)

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
    gh = Github(os.environ.get('GH2DB_GITHUB_TOKEN', ''))
    logger.info('GitHub API authorized OK')

    # GitHub API Rate Limitting
    logger.info('Github API Rate Limitting:')
    logger.info(' Remaining, Limit: {}'.format(gh.rate_limiting))
    logger.info(' ResetTime: {}'.format(gh.get_rate_limit().core.reset))

    # Database Session
    need_db_session = args.update_user_repos or args.update_org_repos
    if need_db_session:
        db = BaseSession().session
        logger.info('Database session established')

    # Update (exeusion user data)
    if args.update_user_repos:
        logger.info('Update database(exeusion user data) start')

        # Execusion User Data
        github_user = gh.get_user()
        _user = GithubUser()
        _user.id = github_user.id,
        _user.name = github_user.name,
        _user.url = github_user.url,
        _user.avatar_url = github_user.avatar_url,
        _user.created_at = github_user.created_at,
        _user.updated_at = github_user.updated_at,
        db.merge(_user)

        # User Repositories
        user_repositories = github_user.get_repos(visibility='all')
        if user_repositories.totalCount > 0:
            logger.info(user_repositories.totalCount)
            for repo in user_repositories:
                logger.info(repo.name)
                _repo = GithubUserRepository()
                _repo.id = repo.id
                _repo.name = repo.name
                _repo.url = repo.url
                _repo.owner = repo.owner
                _repo.default_branch = repo.default_branch
                _repo.created_at = repo.created_at
                _repo.updated_at = repo.updated_at
                db.merge(_repo)

    # Update Database (organization data)
    if args.update_org_repos:
        logger.info('Update database(organization data)')

        # Organizations
        organizations = gh.get_organizations()
        if organizations.totalCount > 0:
            logger.info(organizations.totalCount)
            target_org_name = os.environ.get('GH2DB_GITHUB_TARGET_ORGANIZATION_NAME', '')
            for org in organizations:
                if org.name != target_org_name:
                    continue

                logger.info(org.name)
                _org = GithubOrganization()
                _org.id = org.id
                _org.name = org.name
                _org.url = org.url
                _org.avatar_url = org.avatar_url
                _org.created_at = org.created_at
                _org.updated_at = org.updated_at
                db.merge(_org)

                # Organization Teams
                org_teams = org.get_teams()
                if org_teams.totalCount > 0:
                    logger.info(org_teams.totalCount)
                    for team in org_teams:
                        logger.info(team.name)
                        _team = GithubOrganizationTeam()
                        _team.id = team.id
                        _team.name = team.name
                        _team.url = team.url
                        _team.avatar_url = team.avatar_url
                        _team.created_at = team.created_at
                        _team.updated_at = team.updated_at
                        db.merge(_team)

                # Organization Repositories
                organization_repositories = org.get_repos(visibility='all')
                if organization_repositories.totalCount > 0:
                    logger.info(organization_repositories.totalCount)
                    for repo in organization_repositories:
                        logger.info(repo.name)
                        _repo = GithubOrganizationRepository()
                        _repo.id = repo.id
                        _repo.name = repo.name
                        _repo.url = repo.url
                        _repo.owner = repo.owner
                        _repo.default_branch = repo.default_branch
                        _repo.created_at = repo.created_at
                        _repo.updated_at = repo.updated_at
                        db.merge(_repo)

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
