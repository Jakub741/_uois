from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import (
    create1NGetter,
    createEntityByIdGetter,
    createEntityGetter,
    createInsertResolver,
    createUpdateResolver,
)
from uoishelpers.resolvers import putSingleEntityToDb

from gql_empty.DBDefinitions import BaseModel

from gql_empty.DBDefinitions import ThesesModel, ThesesRolesModel, ThesesTypeModel, ThesesRoleTypeModel #Import všech modelů z DBDefinitions

#Pokud to tady nefunguje tak stačí refreshovat docker a PGadmin!
#Theses resolvers
resolveThesesById = createEntityByIdGetter(ThesesModel) #vrací funkci
#resolveThesesForUser = create1NGetter(UserModel, foreignKeyName='user_id') #vrací uživatele, filtr je FKName, cele spravit
resolveThesesForUser = create1NGetter(ThesesModel, foreignKeyName='user_id') 
resolveThesesForWork = create1NGetter(WorkTypeModel, foreignKeyName='work_id') #vrátí list s id
resolveUpdateTheses = createUpdateResolver(ThesesModel)
resolveThesesAll = createEntityGetter(ThesesModel)

#Users resolver
#resolveUsersById = createEntityByIdGetter(UserModel)
#Type of work resolvers
resolveThesesTypeById = createEntityByIdGetter(ThesesTypeModel)
