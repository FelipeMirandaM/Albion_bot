import json

import aiohttp
import requests
import os
import time
from Conexion import conection_lite

async def load_members():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://gameinfo.albiononline.com/api/gameinfo/guilds/xzUVNm_NRcKYzg8OAUkeNQ/members') as response:
                    html = await response.text()
                    data = json.loads(html)
            async with aiohttp.ClientSession() as session:
                async with session.get('a') as response:
                    html = await response.text()
                    data2 = json.loads(html)

            members_list = []
            for Miembro in data:
                PVP = int(Miembro["KillFame"])
                PVE = int(Miembro["LifetimeStatistics"]["PvE"]["Total"])
                Gathering = int(Miembro["LifetimeStatistics"]["Gathering"]["All"]["Total"])
                Crafting = int(Miembro["LifetimeStatistics"]["Crafting"]["Total"])
                ID = Miembro["Id"]
                Total = PVP+PVE+Gathering+Crafting

                members_list.append((Miembro["Name"].lower(), Total, PVE, PVP, Crafting, ID, Gathering, 'DOOM 1'))


            for Miembro in data2:
                PVP = int(Miembro["KillFame"])
                PVE = int(Miembro["LifetimeStatistics"]["PvE"]["Total"])
                Gathering = int(Miembro["LifetimeStatistics"]["Gathering"]["All"]["Total"])
                Crafting = int(Miembro["LifetimeStatistics"]["Crafting"]["Total"])
                ID = Miembro["Id"]
                Total = PVP+PVE+Gathering+Crafting

                members_list.append((Miembro["Name"].lower(), Total, PVE, PVP, Crafting, ID, Gathering, 'DOOM 2'))

            connection = conection_lite.conection()

            connection.load_data(members_list)

            print("Lista de personajes cargados")
            return True
        except Exception as e:
            print(e)
            print("Error al cargar los datos del gremio, intentando de nuevo")

