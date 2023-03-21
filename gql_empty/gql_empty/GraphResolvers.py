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

from gql_empty.DBDefinitions import UserModel,ThesesModel, WorkTypeModel #Import všech modelů z DBDefinitions

#Pokud to tady nefunguje tak stačí refreshovat docker a PGadmin!
#Theses resolvers
resolveThesesById = createEntityByIdGetter(ThesesModel)
resolveThesesForUser = create1NGetter(UserModel, foreignKeyName='user_id')
resolveThesesForWork = create1NGetter(WorkTypeModel, foreignKeyName='work_id')
resolveUpdateTheses = createUpdateResolver(ThesesModel)
resolveThesesAll = createEntityGetter(ThesesModel)

#Users resolver
resolveUsersById = createEntityByIdGetter(UserModel)
#Type of work resolvers
resolveWorkTypeById = createEntityByIdGetter(WorkTypeModel)
