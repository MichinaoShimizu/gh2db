from __future__ import print_function

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

from .logger import get_module_logger

logger = get_module_logger(__name__)
Base = declarative_base()


class GithubUsers(Base):
    __tablename__ = 'github_users'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column('id', String(255), primary_key=True)
    name = Column('name', String(255), index=True)
    url = Column('url', String(255))
    avatar_url = Column('avatar_url', String(255))
    created_at = Column('created_at', DateTime)
    updated_at = Column('updated_at', DateTime)

    def __init__(self, *, id, name, url, avatar_url, created_at, updated_at):
        self.id = id
        self.name = name
        self.url = url
        self.avatar_url = avatar_url
        self.created_at = created_at
        self.updated_at = updated_at

    def createFromGitHub(user):
        return GithubUsers(
            id=user.id,
            name=user.name,
            url=user.url,
            avatar_url=user.avatar_url,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class GithubRepositories(Base):
    __tablename__ = 'github_repositories'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column('id', String(255), primary_key=True)
    name = Column('name', String(255), index=True)
    full_name = Column('full_name', String(255), index=True)
    url = Column('url', String(255))
    owner = Column('owner', String(255))
    default_branch = Column('default_branch', String(255), index=True)
    created_at = Column('created_at', DateTime)
    updated_at = Column('updated_at', DateTime)

    def __init__(self, *, id, name, full_name, url, owner, default_branch, created_at, updated_at):
        self.id = id
        self.name = name
        self.full_name = full_name
        self.url = url
        self.owner = owner
        self.default_branch = default_branch
        self.created_at = created_at
        self.updated_at = updated_at

    def createFromGitHub(repository):
        return GithubRepositories(
            id=repository.id,
            name=repository.name,
            full_name=repository.full_name,
            url=repository.url,
            owner=repository.owner,
            default_branch=repository.default_branch,
            created_at=repository.created_at,
            updated_at=repository.updated_at,
        )


class GithubRepositoryLabels(Base):
    __tablename__ = 'github_repository_labels'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    repository_id = Column('repository_id', String(255), primary_key=True)
    name = Column('name', String(255), primary_key=True)
    url = Column('url', String(255))
    description = Column('description', String(255))
    color = Column('color', String(255))

    def __init__(self, *, repository_id, name, url, description, color):
        self.repository_id = repository_id
        self.name = name
        self.url = url
        self.description = description
        self.color = color

    def createFromGitHub(repository, label):
        return GithubRepositoryLabels(
            repository_id=repository.id,
            name=label.name,
            url=label.url,
            description=label.description,
            color=label.color
        )


class GithubRepositoryPullRequestLabels(Base):
    __tablename__ = 'github_repository_pull_request_labels'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    repository_id = Column('repository_id', String(255), primary_key=True)
    pull_request_id = Column('pull_request_id', String(255), primary_key=True)
    label_name = Column('label_name', String(255), primary_key=True)

    def __init__(self, *, repository_id, pull_request_id, label_name):
        self.repository_id = repository_id
        self.pull_request_id = pull_request_id
        self.label_name = label_name

    def createFromGitHub(repository, pull_request, pull_request_label):
        return GithubRepositoryPullRequestLabels(
            repository_id=repository.id,
            pull_request_id=pull_request.id,
            label_name=pull_request_label.name
        )


class GithubRepositoryPullRequestCommits(Base):
    __tablename__ = 'github_repository_pull_request_commits'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    repository_id = Column('repository_id', String(255), primary_key=True)
    pull_request_id = Column('pull_request_id', String(255), primary_key=True)
    sha = Column('sha', String(255), primary_key=True)
    comments_url = Column('comments_url', String(255))
    committer = Column('committer', String(255))
    stats = Column('stats', String(255))
    files = Column('files', String(255))
    url = Column('url', String(255))

    def __init__(self, *, repository_id, pull_request_id, sha, comments_url, committer, stats, files, url):
        self.repository_id = repository_id
        self.pull_request_id = pull_request_id
        self.sha = sha
        self.comments_url = comments_url
        self.committer = committer
        self.stats = stats
        # self.files = files
        self.url = url

    def createFromGitHub(repository, pull_request, commit):
        return GithubRepositoryPullRequestCommits(
            repository_id=repository.id,
            pull_request_id=pull_request.id,
            sha=commit.sha,
            comments_url=commit.comments_url,
            committer=commit.committer,
            stats=commit.stats,
            files=commit.files,
            url=commit.url
        )


class GithubRepositoryPullRequestReviews(Base):
    __tablename__ = 'github_repository_pull_request_reviews'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    repository_id = Column('repository_id', String(255), primary_key=True)
    pull_request_id = Column('pull_request_id', String(255), primary_key=True)
    id = Column('id', String(255), primary_key=True)
    # url = Column('url', String(255))
    body = Column('body', Text())
    user_id = Column('user_id', String(255))
    state = Column('state', String(255))
    submitted_at = Column('submitted_at', DateTime)

    def __init__(self, *, repository_id, pull_request_id, id, body, user_id, state, submitted_at):
        self.repository_id = repository_id
        self.pull_request_id = pull_request_id
        self.id = id
        self.body = body
        self.user_id = user_id
        self.state = state
        self.submitted_at = submitted_at

    def createFromGitHub(repository, pull_request, review):
        return GithubRepositoryPullRequestReviews(
            repository_id=repository.id,
            pull_request_id=pull_request.id,
            id=review.id,
            body=review.body,
            user_id=review.user.id,
            state=review.state,
            submitted_at=review.submitted_at
        )


class GithubRepositoryPullRequests(Base):
    __tablename__ = 'github_repository_pull_requests'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column('id', String(255), primary_key=True)
    number = Column('number', Integer(), index=True)
    url = Column('url', String(255))
    title = Column('title', String(255))
    user_id = Column('user_id', String(255))
    state = Column('state', String(255), index=True)
    base_ref = Column('base_ref', String(255), index=True)
    head_ref = Column('head_ref', String(255), index=True)
    merge_commit_sha = Column('merge_commit_sha', String(255))
    mergeable = Column('mergeable', String(255))
    mergeable_state = Column('mergeable_state', String(255))
    merged_by = Column('merged_by', String(255))
    merged_at = Column('merged_at', DateTime, index=True)
    merged = Column('merged', String(255), index=True)
    milestone = Column('milestone', String(255), index=True)
    deletions = Column('deletions', Integer())
    additions = Column('additions', Integer())
    changed_files = Column('changed_files', Integer())
    closed_at = Column('closed_at', DateTime)
    created_at = Column('created_at', DateTime)
    updated_at = Column('updated_at', DateTime)

    def __init__(self, *, id, number, url, title, user_id, state, base_ref, head_ref, merge_commit_sha, mergeable, mergeable_state, merged_by, merged_at, merged, milestone, deletions, additions, changed_files, closed_at, created_at, updated_at):
        self.id = id
        self.number = number
        self.url = url
        self.title = title
        self.user_id = user_id
        self.state = state
        self.base_ref = base_ref
        self.head_ref = head_ref
        self.merge_commit_sha = merge_commit_sha
        self.mergeable = mergeable
        self.mergeable_state = mergeable_state
        self.merged_by = merged_by
        self.merged_at = merged_at
        self.merged = merged
        self.milestone = milestone
        self.deletions = deletions
        self.additions = additions
        self.changed_files = changed_files
        self.closed_at = closed_at
        self.created_at = created_at
        self.updated_at = updated_at

    def createFromGitHub(pull_request):
        return GithubRepositoryPullRequests(
            id=pull_request.id,
            number=pull_request.number,
            url=pull_request.url,
            title=pull_request.title,
            user_id=pull_request.user.id,
            state=pull_request.state,
            base_ref=pull_request.base.ref,
            head_ref=pull_request.head.ref,
            merge_commit_sha=pull_request.merge_commit_sha,
            mergeable=pull_request.mergeable,
            mergeable_state=pull_request.mergeable_state,
            merged_by=pull_request.merged_by,
            merged_at=pull_request.merged_at,
            merged=pull_request.merged,
            milestone=pull_request.milestone,
            deletions=pull_request.deletions,
            additions=pull_request.additions,
            changed_files=pull_request.changed_files,
            closed_at=pull_request.closed_at,
            created_at=pull_request.created_at,
            updated_at=pull_request.updated_at
        )


class GithubOrganizations(Base):
    __tablename__ = 'github_organizations'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column('id', String(255), primary_key=True)
    name = Column('name', String(255), index=True)
    url = Column('url', String(255))
    avatar_url = Column('avatar_url', String(255))
    created_at = Column('created_at', DateTime)
    updated_at = Column('updated_at', DateTime)

    def __init__(self, *, id, name, url, avatar_url, created_at, updated_at):
        self.id = id
        self.name = name
        self.url = url
        self.avatar_url = avatar_url
        self.created_at = created_at
        self.updated_at = updated_at

    def createFromGitHub(organization):
        return GithubOrganizations(
            id=organization.id,
            name=organization.name,
            url=organization.url,
            avatar_url=organization.avatar_url,
            created_at=organization.created_at,
            updated_at=organization.updated_at
        )


class GithubOrganizationTeams(Base):
    __tablename__ = 'github_organization_teams'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    organization_id = Column('organization_id', String(255), primary_key=True)
    id = Column('id', String(255), primary_key=True)
    name = Column('name', String(255), index=True)
    url = Column('url', String(255))
    avatar_url = Column('avatar_url', String(255))
    created_at = Column('created_at', DateTime)
    updated_at = Column('updated_at', DateTime)

    def __init__(self, *, organization_id, id, name, url, avatar_url, created_at, updated_at):
        self.organization_id = organization_id
        self.id = id
        self.name = name
        self.url = url
        self.avatar_url = avatar_url
        self.created_at = created_at
        self.updated_at = updated_at

    def createFromGitHub(organization, team):
        return GithubOrganizationTeams(
            organization_id=organization.id,
            id=team.id,
            name=team.name,
            url=team.url,
            avatar_url=team.avatar_url,
            created_at=team.created_at,
            updated_at=team.updated_at
        )


class GithubOrganizationTeamMembers(Base):
    __tablename__ = 'github_organization_team_members'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    organization_id = Column('organization_id', String(255), primary_key=True)
    team_id = Column('team_id', String(255), primary_key=True)
    user_id = Column('user_id', String(255), primary_key=True)

    def __init__(self, *, organization_id, team_id, user_id):
        self.organization_id = organization_id
        self.team_id = team_id
        self.user_id = user_id

    def createFromGitHub(organization, team, member):
        return GithubOrganizationTeamMembers(
            organization_id=organization.id,
            team_id=team.id,
            user_id=member.id
        )
