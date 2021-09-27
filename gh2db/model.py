from __future__ import print_function

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from .logger import get_module_logger

logger = get_module_logger(__name__)


@declarative_base
class Base:
    @declared_attr
    def created_at(cls):
        return Column(DateTime)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime)


class GithubUser(Base):
    __tablename__ = 'gh_user'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column('id', String(255), primary_key=True)
    name = Column('name', String(255), index=True)
    url = Column('url', String(255))
    avatar_url = Column('avatar_url', String(255))
    created_at = Column('created_at', DateTime)
    updated_at = Column('updated_at', DateTime)


class GithubUserRepository(Base):
    __tablename__ = 'gh_user_repository'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column('id', String(255), primary_key=True)
    name = Column('name', String(255), index=True)
    url = Column('url', String(255))
    owner = Column('owner', String(255))
    default_branch = Column('default_branch', String(255), index=True)


class GithubUserRepositoryPullRequest(Base):
    __tablename__ = 'gh_user_repository_pull_request'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column('id', String(255), primary_key=True)
    number = Column('number', Integer(), index=True)
    url = Column('url', String(255))
    status = Column('status', String(255), index=True)
    author = Column('author', String(255))
    committers = Column('committers', String(255))
    reviewers = Column('reviewers', String(255))
    title = Column('title', String(255))
    head_ref = Column('head_ref', String(255), index=True)
    base_ref = Column('base_ref', String(255), index=True)
    description = Column('description', Text)
    labels = Column('labels', String(255))
    file_addition = Column('file_addition', Integer())
    file_deletion = Column('file_deletion', Integer())
    file_change = Column('file_change', Integer())
    line_addition = Column('line_addition', Integer())
    line_deletion = Column('line_deletion', Integer())
    first_committed_at = Column('first_committed_at', DateTime)
    first_reviewed_at = Column('first_reviewed_at', DateTime)
    approve_time = Column('approve_time', DateTime)
    closed_at = Column('closed_at', DateTime)
    merged_at = Column('merged_at', DateTime, index=True)


class GithubOrganization(Base):
    __tablename__ = 'gh_organization'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column('id', String(255), primary_key=True)
    name = Column('name', String(255), index=True)
    url = Column('url', String(255))
    avatar_url = Column('avatar_url', String(255))


class GithubOrganizationUser(Base):
    __tablename__ = 'gh_organization_user'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column('id', String(255), primary_key=True)
    name = Column('name', String(255), index=True)
    url = Column('url', String(255))
    avatar_url = Column('avatar_url', String(255))


class GithubOrganizationTeam(Base):
    __tablename__ = 'gh_organization_team'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column('id', String(255), primary_key=True)
    name = Column('name', String(255), index=True)
    url = Column('url', String(255))
    avatar_url = Column('avatar_url', String(255))


class GithubOrganizationRepository(Base):
    __tablename__ = 'gh_organization_repository'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column('id', String(255), primary_key=True)
    name = Column('name', String(255), index=True)
    url = Column('url', String(255))
    owner = Column('owner', String(255))
    default_branch = Column('default_branch', String(255), index=True)


class GithubOrganizationRepositoryPullRequest(Base):
    __tablename__ = 'gh_organization_repository_pull_request'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column('id', String(255), primary_key=True)
    number = Column('number', Integer(), index=True)
    url = Column('url', String(255))
    status = Column('status', String(255), index=True)
    author = Column('author', String(255))
    committers = Column('committers', String(255))
    reviewers = Column('reviewers', String(255))
    title = Column('title', String(255))
    head_ref = Column('head_ref', String(255), index=True)
    base_ref = Column('base_ref', String(255), index=True)
    description = Column('description', Text)
    labels = Column('labels', String(255))
    file_addition = Column('file_addition', Integer())
    file_deletion = Column('file_deletion', Integer())
    file_change = Column('file_change', Integer())
    line_addition = Column('line_addition', Integer())
    line_deletion = Column('line_deletion', Integer())
    first_committed_at = Column('first_committed_at', DateTime)
    first_reviewed_at = Column('first_reviewed_at', DateTime)
    approve_time = Column('approve_time', DateTime)
    closed_at = Column('closed_at', DateTime)
    merged_at = Column('merged_at', DateTime, index=True)
