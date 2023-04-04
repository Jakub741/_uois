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

from gql_empty.DBDefinitions import ThesesModel, ThesesUserRoleModel, ThesesRoleModel, ThesesTypeModel #Import všech modelů z DBDefinitions

#Theses resolvers
resolveThesesById = createEntityByIdGetter(ThesesModel) 
resolveThesesRole = createEntityByIdGetter(ThesesRoleModel)
resolveThesesUserRole = createEntityByIdGetter(ThesesUserRoleModel)
resolveRolesForThesis = create1NGetter(ThesesUserRoleModel, foreignKeyName='theses_id')
resolveRolesForUser = create1NGetter(ThesesUserRoleModel, foreignKeyName='user_id')
resolveThesisTypeById = createEntityByIdGetter(ThesesTypeModel)
