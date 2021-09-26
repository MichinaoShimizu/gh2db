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
    def __init__(self):
        self.e = BaseEngine().engine

    def create_all(self):
        Base.metadata.create_all(self.e)

    def drop_all(self):
        Base.metadata.drop_all(self.e)

    def delete_all(self):
        s = BaseSession().session
        s.query(GithubUser).delete()
        s.query(GithubUserRepository).delete()
        s.query(GithubUserRepositoryPullRequest).delete()
        s.query(GithubOrganization).delete()
        s.query(GithubOrganizationTeam).delete()
        s.query(GithubOrganizationUser).delete()
        s.query(GithubOrganizationRepository).delete()
        s.query(GithubOrganizationRepositoryPullRequest).delete()
        s.commit()

    def __debug(self, s, model):
        print(f"{model.__tablename__}:{s.query(model).count()}")

    def count_all(self):
        s = BaseSession().session
        self.__debug(s, GithubUser)
        self.__debug(s, GithubUserRepository)
        self.__debug(s, GithubUserRepositoryPullRequest)
        self.__debug(s, GithubOrganization)
        self.__debug(s, GithubOrganizationTeam)
        self.__debug(s, GithubOrganizationUser)
        self.__debug(s, GithubOrganizationRepository)
        self.__debug(s, GithubOrganizationRepositoryPullRequest)
