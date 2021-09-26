from __future__ import print_function
from gh2db.migration import Migration
from gh2db.model import GithubOrganizationRepository
from gh2db.model import GithubOrganizationTeam
from gh2db.model import GithubOrganization
from gh2db.model import GithubUserRepository
from gh2db.model import GithubUser
from gh2db.logger import get_logger
from gh2db.dbbase import BaseSession
from argparse import ArgumentParser
from github import Github
import os
from dotenv import load_dotenv
load_dotenv()
logger = get_logger(__name__)


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
        logger.info('create all tables')
        return Migration().create_all()

    # Drop tables
    if args.drop_all:
        logger.info('drop all tables')
        return Migration().drop_all()

    # Count all of table rows
    if args.count_all:
        logger.info('count all of table rows')
        return Migration().count_all()

    # Delete all of table rows
    if args.delete_all:
        logger.info('delete all of table rows')
        return Migration().delete_all()

    # Establish GitHub API Connection
    gh = Github(os.environ['GITHUB_TOKEN'])
    logger.info('github api authorize ok')

    # Rate Limitting
    logger.info('github api rate limitting:')
    logger.info(gh.rate_limiting)
    logger.info(gh.get_rate_limit().core.reset)

    # Establish Database Connection
    if args.update_user_repos or args.update_org_repos:
        db = BaseSession().session
        logger.info('database session established')

    # Update Database (exeusion user data)
    if args.update_user_repos:
        logger.info('update database(exeusion user data)')
        github_user = gh.get_user()
        _user = GithubUser()
        _user.id = github_user.id,
        _user.name = github_user.name,
        _user.url = github_user.url,
        _user.avatar_url = github_user.avatar_url,
        _user.created_at = github_user.created_at,
        _user.updated_at = github_user.updated_at,
        db.add(_user)

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
                db.add(_repo)

    # Update Database (organization data)
    if args.update_org_repos:
        logger.info('update database(organization data)')
        organizations = gh.get_organizations()
        if organizations.totalCount > 0:
            approved_org_name = os.environ['APPROVED_ORGANIZATION_NAME']
            logger.info(organizations.totalCount)
            for org in organizations:
                logger.info(org.name)
                if approved_org_name and (org.name != approved_org_name):
                    logger.info(f'org {org.name} was skipped')
                    continue

                _org = GithubOrganization()
                _org.id = org.id
                _org.name = org.name
                _org.url = org.url
                _org.avatar_url = org.avatar_url
                _org.created_at = org.created_at
                _org.updated_at = org.updated_at
                db.add(_org)

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
                        db.add(_team)

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
                        db.add(_repo)

    if args.update_user_repos or args.update_org_repos:
        try:
            db.commit()
            logger.info('committed')
        except Exception as e:
            logger.info('commit error')
            db.rollback()
            logger.info('rollbacked')
            raise(e)
        finally:
            db.close()
            logger.info('closed')

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
