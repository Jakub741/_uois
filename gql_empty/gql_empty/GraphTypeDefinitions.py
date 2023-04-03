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
from gql_empty.GraphResolvers import (resolveThesesById,
                                      resolveThesesRole,
                                      resolveThesesUserRole,
                                      resolveUserRole,
                                      resolveRolesForThesis,
                                      resolveRolesForUser,
                                      resolveThesisTypeById)


@strawberryA.federation.type(keys=["id"],description="""Entity representing a Theses""")
class ThesesGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveThesesById(session, id)
            result._type_definition = cls._type_definition 
            return result
    
    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
     

    @strawberryA.field(description="""Type of Theses""")
    async def type(self,info: strawberryA.types.Info) -> "ThesesTypeGQLModel":
        async with withInfo(info) as session:
            result = await resolveThesisTypeById(session,self.work_id)
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

    @strawberryA.field(description="""Users and their roles""")
    async def roles(self,info: strawberryA.types.Info) -> List["ThesesUserRoleGQLModel"]: 
        async with withInfo(info) as session:
            result = await resolveRolesForThesis(session,self.id)
            return result
##############################
@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz
    
    @strawberryA.field(description="""Possible roles within Theses""")
    async def thesesRoles(self, info: strawberryA.types.Info)->List['ThesesUserRoleGQLModel']:
        async with withInfo(info) as session:
            result = await resolveRolesForUser(session, self.id)
            return result
##############################
@strawberryA.federation.type(keys=["id"],description="""Entity representing a UserRole""")
class ThesesRoleTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveThesesRole(session, id)
            result._type_definition = cls._type_definition
            return result
        
    @strawberryA.field(description="""Name of role""")
    def name(self) -> str:
        return self.name
################################
@strawberryA.federation.type(keys=["id"],description="""Entity representing a ThesesUserRole""")
class ThesesUserRoleGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveThesesUserRole(session, id) 
            result._type_definition = cls._type_definition 
            return result
   
    @strawberryA.field(description="""User assigned to Thesis""")
    async def user(cls, info: strawberryA.types.Info, id: strawberryA.ID)->UserGQLModel:
        async with withInfo(info) as session:
            result = await resolveRolesForUser(session, id) 
            result._type_definition = cls._type_definition 
            return result
   
    @strawberryA.field(description="""Thesis which we are pointing to""") ##vylepsit nazev - je to xopowo?
    async def thesis(cls, info: strawberryA.types.Info, id: strawberryA.ID)->ThesesGQLModel:
        async with withInfo(info) as session:
            result = await resolveRolesForThesis(session, id) 
            result._type_definition = cls._type_definition
            return result
    
    @strawberryA.field(description="""Role of User in Thesis""")
    async def roleType(cls, info: strawberryA.types.Info, id: strawberryA.ID)->ThesesRoleTypeGQLModel:
        async with withInfo(info) as session:
            result = await resolveUserRole(session, id) 
            result._type_definition = cls._type_definition 
            return result

@strawberryA.federation.type(keys=["id"],description="""Entity representing a ThesesType""") #Je to spravne?
class ThesesTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveThesesUserRole(session, id)
            result._type_definition = cls._type_definition 
            return result
    @strawberryA.field(description="""Type of Thesis""")
    def name(self) -> str:
        return self.name


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################




@strawberryA.type(description="""Type for query root""")  #whaaaaat
class Query:
    @strawberryA.field(description="""Finds Theses by their id""")
    async def Theses_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[ThesesGQLModel, None]:
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

