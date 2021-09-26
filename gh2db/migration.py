from __future__ import print_function
from .dbbase import BaseEngine, BaseSession
from .model import Base
from .model import GithubUser
from .model import GithubUserRepository
from .model import GithubUserRepositoryPullRequest
from .model import GithubOrganization
from .model import GithubOrganizationTeam
from .model import GithubOrganizationUser
from .model import GithubOrganizationRepository
from .model import GithubOrganizationRepositoryPullRequest


class Migration(object):
    MODELS = [
        GithubUser,
        GithubUserRepository,
        GithubUserRepositoryPullRequest,
        GithubOrganization,
        GithubOrganizationTeam,
        GithubOrganizationUser,
        GithubOrganizationRepository,
        GithubOrganizationRepositoryPullRequest
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
