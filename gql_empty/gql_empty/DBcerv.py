from email.policy import default
import sqlalchemy
import datetime

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

def UUIDColumn(name=None):
    if name is None:
        return Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    else:
        return Column(name, UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
#id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)    


# mezitabulka thesis-user-role
class ThesesUserRoleModel(BaseModel):
    __tablename__ = 'thesesuser'
    id = UUIDColumn()
   
    user_id = Column(ForeignKey('users.id'))
    theses_id = Column(ForeignKey('theses.id'))
    role_id = Column(ForeignKey('thesesrole.id'))
 
    user  = relationship('UserModel', back_populates = 'theses')
    thesis = relationship('ThesesModel', back_populates = 'users')
    thesesrole = relationship('ThesesRoleModel', back_populates = 'theses')# s čím má být propojený? - 1. varianta - propojení th.role s prací
    thesisr = relationship('ThesesModel', back_populates = 'thesesroles')                       
    # thesesroles = relationship('ThesesRoleModel', back_populates = 'users') # 2. varianta - propojeni th.role s uživatelem 

class ThesesModel(BaseModel):
    """Spravuje data spojena se závěrečnými prácemi
        typ práce, stav práce..."""
    __tablename__ = 'theses'
    
    id = UUIDColumn()
    name = Column(String) #Název práce
    startDate = Column(DateTime) #Datum zahájení
    endDate = Column(DateTime) #Datum ukončení
    lastchange = Column(DateTime, default=datetime.datetime.now)
    state = Column(String) #Stav práce
    
    thesestype_id = Column(ForeignKey('thesestype.id')) #work type id/theses type id 
    
    thesestype  = relationship('ThesesTypeModel', back_populates='theses')
    users = relationship('ThesesUserRoleModel', back_populates = 'thesis')
    thesesroles = relationship('ThesesUserRoleModel', back_populates = 'thesisr')
    

class ThesesTypeModel(BaseModel): #theses types 82 řádek
    """popis typu práce (diplomka, bakalářka...)"""
    __tablename__ = 'thesestype'
    id = UUIDColumn()
    name = Column(String) #diplomka...
    
    theses = relationship('ThesesModel', back_populates='thesestype')

class ThesesRoleModel(BaseModel): 
    """druhy rolí které můžou které můžou být lidem přiřazeny"""
    __tablename__ = 'thesesrole'
    id = UUIDColumn()
    name = Column(String) #konzultant, vedoucí, autor...
    
    theses = relationship('ThesesUserRoleModel', back_populates='thesesrole')

class UserModel(BaseModel):
    __tablename__ = 'user'
    id = UUIDColumn()
    
    theses = relationship('ThesesUserRoleModel', back_populates = 'user')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker """
    asyncEngine = create_async_engine(connectionstring) 

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print('BaseModel.metadata.drop_all finished')
        if makeUp:
            await conn.run_sync(BaseModel.metadata.create_all)    
            print('BaseModel.metadata.create_all finished')

    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker

import os
def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
       Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database =  os.environ.get("POSTGRES_DB", "data")
    hostWithPort =  os.environ.get("POSTGRES_HOST", "postgres:5432")
    
    driver = "postgresql+asyncpg" #"postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring