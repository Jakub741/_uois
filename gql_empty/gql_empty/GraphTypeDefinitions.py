from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid
#náš import
from contextlib import asynccontextmanager
import datetime

def AsyncSessionFromInfo(info):
    return info.context["session"]
###############################################
@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context['asyncSessionMaker']
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass

def AsyncSessionFromInfo(info):
    print('obsolete function used AsyncSessionFromInfo, use withInfo context manager instead')
    return info.context['session']

def AsyncSessionMakerFromInfo(info):
    return info.context['asyncSessionMaker']

###############################################


###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################

#import resolverů
from gql_empty.GraphResolvers import resolveThesesById,resolveThesesForUser,resolveWorkTypeById,resolveThesesAll,resolveThesesForUser,resolveThesesForWork,resolveUpdateTheses


@strawberryA.federation.type(keys=["id"],description="""Entity representing a Theses""")
class ThesesGQLModel: #theses ne project
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveThesesById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result
    
    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    

    @strawberryA.field(description="""Type of Theses""")
    async def type(self,info: strawberryA.types.Info) -> "ThesesTypeModel": ##unfinished
        async with withInfo(info) as session:
            result = await resolveWorkTypeById(session,self.work_id)
            return result

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
    def lastChange(self) -> datetime.datetime:
        return self.lastChange

    @strawberryA.field(description="""State of work""")
    def state(self) -> str:
        return self.state

    @strawberryA.field(description="""Participants""")
    async def type(self,info: strawberryA.types.Info) -> "ThesesTypeModel": ##unfinished, kurva jak na to
        async with withInfo(info) as session:
            result = await resolveWorkTypeById(session,self.work_id)
            return result
##############################x
@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz




###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################




@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""Finds Theses by their id""")
    async def Theses_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[ProjectGQLModel, None]:
        result = await resolveThesesById(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[str, None]:
        result = f"Hello {id}"
        return result



###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel,))

