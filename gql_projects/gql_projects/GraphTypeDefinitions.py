from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager


@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass


def AsyncSessionFromInfo(info):
    print(
        "obsolete function used AsyncSessionFromInfo, use withInfo context manager instead"
    )
    return info.context["session"]


###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
# GQL PROJECT
import datetime
from gql_projects.GraphResolvers import (
    resolveProjectById,
    resolveProjectAll,
    resolveUpdateProject,
    resolveInsertProject,
)


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a project"""
)
class ProjectGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveProjectById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Start date""")
    def startDate(self) -> datetime.date:
        return self.startDate

    @strawberryA.field(description="""End date""")
    def endDate(self) -> datetime.date:
        return self.endDate

    @strawberryA.field(description="""Last change""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Project type of project""")
    async def projectType(self, info: strawberryA.types.Info) -> "ProjectTypeGQLModel":
        async with withInfo(info) as session:
            result = await resolveProjectTypeById(session, self.projectType_id)
            return result

    @strawberryA.field(description="""List of finances, related to a project""")
    async def finances(
        self, info: strawberryA.types.Info
    ) -> typing.List["FinanceGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveFinancesForProject(session, self.id)
            return result

    @strawberryA.field(description="""List of milestones, related to a project""")
    async def milestones(
        self, info: strawberryA.types.Info
    ) -> typing.List["MilestoneGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveMilestonesForProject(session, self.id)
            return result

    @strawberryA.field(description="""Group, related to a project""")
    async def group(self, info: strawberryA.types.Info) -> "GroupGQLModel":
        return GroupGQLModel(id=self.group_id)


# GQL PROJECT TYPE
from gql_projects.GraphResolvers import (
    resolveProjectTypeById,
    resolveProjectTypeAll,
    resolveUpdateProjectType,
    resolveInsertProjectType,
    resolveProjectsForProjectType,
    resolveFinancesForProject,
    resolveMilestonesForProject,
)


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a project types"""
)
class ProjectTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveProjectTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Name""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""List of projects, related to project type""")
    async def projects(
        self, info: strawberryA.types.Info
    ) -> typing.List["ProjectGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveProjectsForProjectType(session, self.id)
            return result


# GQL FINANCE
from gql_projects.GraphResolvers import (
    resolveFinanceById,
    resolveFinanceAll,
    resolveUpdateFinance,
    resolveInsertFinance,
)


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a finance"""
)
class FinanceGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveFinanceById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Amount""")
    def amount(self) -> float:
        return self.amount

    @strawberryA.field(description="""Last change""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Project of finance""")
    async def project(self, info: strawberryA.types.Info) -> "ProjectGQLModel":
        async with withInfo(info) as session:
            result = await resolveProjectById(session, self.project_id)
            return result

    @strawberryA.field(description="""Finance type of finance""")
    async def financeType(self, info: strawberryA.types.Info) -> "FinanceTypeGQLModel":
        async with withInfo(info) as session:
            result = await resolveFinanceTypeById(session, self.financeType_id)
            return result


# GQL FINANCE TYPE
from gql_projects.GraphResolvers import (
    resolveFinanceTypeById,
    resolveFinanceTypeAll,
    resolveUpdateFinanceType,
    resolveInsertFinanceType,
    resolveFinancesForFinanceType,
)


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a finance type"""
)
class FinanceTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveFinanceTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Name""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""List of finances, related to finance type""")
    async def finances(
        self, info: strawberryA.types.Info
    ) -> typing.List["FinanceGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveFinancesForFinanceType(session, self.id)
            return result


# GQL MILESTONE
from gql_projects.GraphResolvers import (
    resolveMilestoneById,
    resolveMilestoneAll,
    resolveUpdateMilestone,
    resolveInsertMilestone,
)


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a milestone"""
)
class MilestoneGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveMilestoneById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Date""")
    def startdate(self) -> datetime.date:
        return self.startdate

    @strawberryA.field(description="""Date""")
    def enddate(self) -> datetime.date:
        return self.enddate

    @strawberryA.field(description="""Last change""")
    def lastChange(self) -> datetime.datetime:
        return self.lastChange

    @strawberryA.field(description="""Project of milestone""")
    async def project(self, info: strawberryA.types.Info) -> "ProjectGQLModel":
        async with withInfo(info) as session:
            result = await resolveProjectById(session, self.project_id)
            return result


# GQL GROUP
from gql_projects.GraphResolvers import resolveProjectsForGroup


@strawberryA.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return GroupGQLModel(id=id)

    @strawberryA.field(description="""List of projects, related to group""")
    async def projects(
        self, info: strawberryA.types.Info
    ) -> typing.List["ProjectGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveProjectsForGroup(session, self.id)
            return result


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

from gql_projects.DBFeeder import randomDataStructure


@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""Returns a list of projects""")
    async def project_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[ProjectGQLModel]:
        async with withInfo(info) as session:
            result = await resolveProjectAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Returns project by its id""")
    async def project_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[ProjectGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolveProjectById(session, id)
            return result

    @strawberryA.field(description="""Returns a list of project types""")
    async def project_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[ProjectTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveProjectTypeAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Returns a list of finances""")
    async def finance_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[FinanceGQLModel]:
        async with withInfo(info) as session:
            result = await resolveFinanceAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Returns a list of finance types""")
    async def finance_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[FinanceTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveFinanceTypeAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Returns a list of milestones""")
    async def milestone_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[MilestoneGQLModel]:
        async with withInfo(info) as session:
            result = await resolveMilestoneAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Returns a list of projects for group""")
    async def project_by_group(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> List[ProjectGQLModel]:
        async with withInfo(info) as session:
            result = await resolveProjectsForGroup(session, id)
            return result

    @strawberryA.field(description="""Random publications""")
    async def randomProject(
        self, info: strawberryA.types.Info
    ) -> Union[ProjectGQLModel, None]:
        async with withInfo(info) as session:
            result = await randomDataStructure(AsyncSessionFromInfo(info))
            return result


###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(GroupGQLModel,))
