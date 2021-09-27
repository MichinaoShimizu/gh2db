from __future__ import print_function

from .dbbase import BaseEngine, BaseSession
from .logger import get_module_logger
from .model import (Base, GithubOrganizations, GithubOrganizationTeamMembers,
                    GithubOrganizationTeams, GithubRepositories,
                    GithubRepositoryLabels, GithubRepositoryPullRequestCommits,
                    GithubRepositoryPullRequestLabels,
                    GithubRepositoryPullRequestReviews,
                    GithubRepositoryPullRequests, GithubUsers)

logger = get_module_logger(__name__)


class Migration(object):
    MODELS = [
        GithubUsers,
        GithubOrganizations,
        GithubOrganizationTeams,
        GithubOrganizationTeamMembers,
        GithubRepositories,
        GithubRepositoryLabels,
        GithubRepositoryPullRequests,
        GithubRepositoryPullRequestLabels,
        GithubRepositoryPullRequestCommits,
        GithubRepositoryPullRequestReviews,
    ]

    def __init__(self):
        self.e = BaseEngine().engine

    def create_all(self):
        Base.metadata.create_all(self.e)

    def drop_all(self):
        Base.metadata.drop_all(self.e)

    def delete_all(self):
        s = BaseSession().session
        for m in self.MODELS:
            s.query(m).delete()
        s.commit()

    def count_all(self):
        s = BaseSession().session
        for m in self.MODELS:
            print(f"{m.__tablename__}:{s.query(m).count()}")
