from __future__ import print_function

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from .logger import get_module_logger

logger = get_module_logger(__name__)


@declarative_base
class Base:
    __table_args__ = {'mysql_engine': 'InnoDB'}

    @declared_attr
    def created_at(cls):
        return Column(DateTime)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime)


class GithubUsers(Base):
    """GitHub User Master
    """
    __tablename__ = 'github_users'
    id = Column('id', String(255), primary_key=True)
    name = Column('name', String(255), index=True)
    url = Column('url', String(255))
    avatar_url = Column('avatar_url', String(255))


class GithubRepositories(Base):
    """GitHub Repository Master
    """
    __tablename__ = 'github_repositories'
    id = Column('id', String(255), primary_key=True)
    name = Column('name', String(255), index=True)
    full_name = Column('full_name', String(255), index=True)
    url = Column('url', String(255))
    owner = Column('owner', String(255))
    default_branch = Column('default_branch', String(255), index=True)


class GithubRepositoryLabels(Base):
    """GitHub Repository Label Master
    """
    __tablename__ = 'github_repository_labels'
    repisitory_id = Column('repisitory_id', String(255), primary_key=True)
    name = Column('name', String(255), index=True)
    url = Column('url', String(255))
    description = Column('description', String(255))
    color = Column('color', String(255))


class GithubRepositoryPullRequestLabels(Base):
    """GitHub Repository Pull Request Label Table
    """
    __tablename__ = 'github_repository_pull_request_labels'
    repisitory_id = Column('repisitory_id', String(255), primary_key=True)
    pull_request_id = Column('pull_request_id', String(255), primary_key=True)
    label_name = Column('label_name', String(255), primary_key=True)


class GithubRepositoryPullRequestCommits(Base):
    """GitHub Repository Pull Request Commits Table
    """
    __tablename__ = 'github_repository_pull_request_commits'
    repisitory_id = Column('repisitory_id', String(255), primary_key=True)
    pull_request_id = Column('pull_request_id', String(255), primary_key=True)
    sha = Column('sha', String(255), primary_key=True)
    comments_url = Column('comments_url', String(255))
    user_id = Column('user_id', String(255))
    stats = Column('stats', String(255))
    files = Column('files', String(255))
    url = Column('url', String(255))


class GithubRepositoryPullRequestReviews(Base):
    """GitHub Repository Pull Request Reviews Table
    """
    __tablename__ = 'github_repository_pull_request_reviews'
    repisitory_id = Column('repisitory_id', String(255), primary_key=True)
    pull_request_id = Column('pull_request_id', String(255), primary_key=True)
    id = Column('id', String(255), primary_key=True)
    # url = Column('url', String(255))
    body = Column('body', Text())
    user_id = Column('user_id', String(255))
    state = Column('state', String(255))
    submitted_at = Column('submitted_at', DateTime)


class GithubRepositoryPullRequests(Base):
    """GitHub Repository Pull Request Master
    """
    __tablename__ = 'github_repository_pull_requests'
    id = Column('id', String(255), primary_key=True)
    number = Column('number', Integer(), index=True)
    url = Column('url', String(255))
    title = Column('title', String(255))
    user_id = Column('user_id', String(255))
    state = Column('state', String(255), index=True)
    base_ref = Column('base_ref', String(255), index=True)
    head_ref = Column('head_ref', String(255), index=True)
    mrege_commit_sha = Column('mrege_commit_sha', String(255))
    mergeable = Column('mergeable', String(255))
    mergeable_state = Column('mergeable_state', String(255))
    merged_user_id = Column('merged_user_id', String(255))
    merged_at = Column('merged_at', DateTime, index=True)
    merged = Column('merged', String(255), index=True)
    milestone = Column('milestone', String(255), index=True)
    deletions = Column('deletions', Integer())
    additions = Column('additions', Integer())
    changed_files = Column('changed_files', Integer())
    closed_at = Column('closed_at', DateTime)


class GithubOrganizations(Base):
    """GitHub Repository Organization Master
    """
    __tablename__ = 'github_organizations'
    id = Column('id', String(255), primary_key=True)
    name = Column('name', String(255), index=True)
    url = Column('url', String(255))
    avatar_url = Column('avatar_url', String(255))


class GithubOrganizationTeams(Base):
    """GitHub Repository Organization Team Master
    """
    __tablename__ = 'github_organization_teams'
    organization_id = Column('organization_id', String(255), primary_key=True)
    id = Column('id', String(255), primary_key=True)
    name = Column('name', String(255), index=True)
    url = Column('url', String(255))
    avatar_url = Column('avatar_url', String(255))


class GithubOrganizationTeamMembers(Base):
    """GitHub Repository Organization Team Member Table
    """
    __tablename__ = 'github_organization_team_members'
    organization_id = Column('organization_id', String(255), primary_key=True)
    team_id = Column('team_id', String(255), primary_key=True)
    user_id = Column('user_id', String(255), primary_key=True)
