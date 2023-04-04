from doctest import master
from functools import cache
from gql_empty.DBDefinitions import BaseModel, ThesesUserRoleModel, ThesesModel, ThesesTypeModel, ThesesRoleModel, UserModel

import random
import itertools
from functools import cache


from sqlalchemy.future import select


def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
    Dekorovana funkce je asynchronni.
    """
    resultCache = {}

    async def result():
        if resultCache.get("result", None) is None:
            resultCache["result"] = await asyncFunc()
        return resultCache["result"]

    return result


###########################################################################################################################
#
# zde definujte sva systemova data
#
###########################################################################################################################



@cache
def types1(): #pro ThesesTypeModel
    data = [
       {"id": "4b883614-6d9e-11ed-a1eb-0242ac120003", "name": "Bakalářská práce"},
       {"id": "4b883614-6d9e-11ed-a1eb-0242ac120004", "name": "Diplomová práce"},
       {"id": "4b883614-6d9e-11ed-a1eb-0242ac120005", "name": "Zápočtová práce"},
       {"id": "4b883614-6d9e-11ed-a1eb-0242ac120006", "name": "Zkoušková práce"},
       {"id": "4b883614-6d9e-11ed-a1eb-0242ac120007", "name": "Seminární práce"},
       {"id": "4b883614-6d9e-11ed-a1eb-0242ac120008", "name": "Disertační práce"},
       {"id": "4b883614-6d9e-11ed-a1eb-0242ac120009", "name": "Vědecká práce"},
       {"id": "4b883614-6d9e-11ed-a1eb-0242ac120010", "name": "Studentská tvůrčí činnost"},
       {"id": "4b883614-6d9e-11ed-a1eb-0242ac120011", "name": "Ostatní"},
    ]
    return data
@cache
def types2(): #pro ThesesRoleModel
    data = [
       {"id": "4b883614-6d9a-11ed-a1eb-0242ac120003", "name": "Autor"},
       {"id": "4b883614-6d9a-11ed-a1eb-0242ac120004", "name": "Vedoucí"},
       {"id": "4b883614-6d9a-11ed-a1eb-0242ac120005", "name": "Oponent"},
       {"id": "4b883614-6d9a-11ed-a1eb-0242ac120006", "name": "Pomocník"},
       {"id": "4b883614-6d9a-11ed-a1eb-0242ac120007", "name": "Referent"},
       {"id": "4b883614-6d9a-11ed-a1eb-0242ac120008", "name": "Ostatní"},
    ]
    return data



###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################

import asyncio


async def predefineAllDataStructures(asyncSessionMaker):
    
    asyncio.gather(
        putPredefinedStructuresIntoTable(asyncSessionMaker, ThesesTypeModel, types1),
        putPredefinedStructuresIntoTable(asyncSessionMaker, ThesesRoleModel, types2)
    )
    
    
    return


async def putPredefinedStructuresIntoTable(
    asyncSessionMaker, DBModel, structureFunction
):
    """Zabezpeci prvotni inicicalizaci typu externích ids v databazi
    DBModel zprostredkovava tabulku, je to sqlalchemy model
    structureFunction() dava data, ktera maji byt ulozena
    """
    # ocekavane typy
    externalIdTypes = structureFunction()

    # dotaz do databaze
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = list(dbSet.scalars())

    # extrakce dat z vysledku dotazu
    # vezmeme si jen atributy name a id, id je typu uuid, tak jej zkovertujeme na string
    dbRowsDicts = [{"name": row.name, "id": f"{row.id}"} for row in dbRows]

    print(structureFunction, "external id types found in database")
    print(dbRowsDicts)

    # vytahneme si vektor (list) id, ten pouzijeme pro operator in nize
    idsInDatabase = [row["id"] for row in dbRowsDicts]

    # zjistime, ktera id nejsou v databazi
    unsavedRows = list(
        filter(lambda row: not (row["id"] in idsInDatabase), externalIdTypes)
    )
    print(structureFunction, "external id types not found in database")
    print(unsavedRows)

    # pro vsechna neulozena id vytvorime entity
    rowsToAdd = [DBModel(**row) for row in unsavedRows]
    print(rowsToAdd)
    print(len(rowsToAdd))

    # a vytvorene entity jednou operaci vlozime do databaze
    async with asyncSessionMaker() as session:
        async with session.begin():
            session.add_all(rowsToAdd)
        await session.commit()

    # jeste jednou se dotazeme do databaze
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = dbSet.scalars()

    # extrakce dat z vysledku dotazu
    dbRowsDicts = [{"name": row.name, "id": f"{row.id}"} for row in dbRows]

    print(structureFunction, "found in database")
    print(dbRowsDicts)

    # znovu id, ktera jsou uz ulozena
    idsInDatabase = [row["id"] for row in dbRowsDicts]

    # znovu zaznamy, ktere dosud ulozeny nejsou, mely by byt ulozeny vsechny, takze prazdny list
    unsavedRows = list(
        filter(lambda row: not (row["id"] in idsInDatabase), externalIdTypes)
    )

    # ted by melo byt pole prazdne
    print(structureFunction, "not found in database")
    print(unsavedRows)
    if not (len(unsavedRows) == 0):
        print("SOMETHING is REALLY WRONG")

    print(structureFunction, "Defined in database")
    # nyni vsechny entity mame v pameti a v databazi synchronizovane
    print(structureFunction())
    pass
