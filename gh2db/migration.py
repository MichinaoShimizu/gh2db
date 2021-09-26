from gh2db.dbbase import BaseEngine, BaseSession
from gh2db.model import Base
from gh2db.model import GithubUser
from gh2db.model import GithubUserRepository
from gh2db.model import GithubUserRepositoryPullRequest
from gh2db.model import GithubOrganization
from gh2db.model import GithubOrganizationTeam
from gh2db.model import GithubOrganizationUser
from gh2db.model import GithubOrganizationRepository
from gh2db.model import GithubOrganizationRepositoryPullRequest


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
