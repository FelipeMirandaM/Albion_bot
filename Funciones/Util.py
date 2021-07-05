from Conexion import Conexion
from datetime import datetime, timedelta
from Funciones import VerificarMiembro
from Conexion import conection_lite
import mysql.connector
def get_personajes_sin_registrar():
    MyConexion = Conexion.Conexion()
    MyConexion.crear_conexion()
    Lista_Sin_Registrar = []
    Diccionario = {}
    cursor = MyConexion.get_conexion().cursor(buffered=True)
    conection = conection_lite.conection()
    member_list = conection.get_member_list()
    User_Information = "SELECT name FROM player"
    try:
        cursor.execute(User_Information)
        MyConexion.get_conexion().commit()
        Info = cursor.fetchall()

        for Miembro in Info:

            Diccionario[Miembro[0].lower()] = Miembro

        for Miembro in member_list:
            if not Miembro[0].lower() in Diccionario:
                Lista_Sin_Registrar.append(Miembro[0])
        Lista_Sin_Registrar.sort()
        return Lista_Sin_Registrar
    except TypeError as e:
        MyConexion.get_conexion().rollback()
        print(e)
        cursor.close()
        MyConexion.cerrar_conexion()
        return None


def search_user(id_discord):
    MyConexion = Conexion.Conexion()
    MyConexion.crear_conexion()
    cursor = MyConexion.get_conexion().cursor(buffered=True)
    User_Information = ("SELECT * FROM player "
                        "WHERE Discord_ID= %s and is_alter = 0")
    Data = (id_discord,)
    try:
        cursor.execute(User_Information, Data)
        MyConexion.get_conexion().commit()
        Info = cursor.fetchall()
        cursor.close()
        MyConexion.cerrar_conexion()
        return Info
    except mysql.connector.Error as err:
        MyConexion.get_conexion().rollback()
        print(err)
        cursor.close()
        MyConexion.cerrar_conexion()
        return None


def search_personaje(nombre_personaje):
    MyConexion = Conexion.Conexion()
    MyConexion.crear_conexion()
    cursor = MyConexion.get_conexion().cursor(buffered=True)
    User_Information = ("SELECT * FROM player "
                        "WHERE name= %s")
    Data=(nombre_personaje,)
    try:
        cursor.execute(User_Information, Data)
        MyConexion.get_conexion().commit()
        Info = cursor.fetchall()
        cursor.close()
        MyConexion.cerrar_conexion()
        return Info
    except mysql.connector.Error as err:
        MyConexion.get_conexion().rollback()
        print(err)
        cursor.close()
        MyConexion.cerrar_conexion()
        return None


def agregar_personaje(id_discord, nombre_personaje, cursor):
    hoy = datetime.now()
    SQL_Usuario_Nuevo = ("INSERT INTO Personajes "
                         "(Nombre, ID_Discord, fecha) "
                         "VALUES (%s, %s, %s)")

    Datos = (nombre_personaje, id_discord, hoy)
    try:
        cursor.execute(SQL_Usuario_Nuevo, Datos)
    except TypeError as e:
        print(e)


def agregar_usuario(id_discord, nombre_personaje):
    Albion_ID = VerificarMiembro.search_name(nombre_personaje)
    if Albion_ID is 0:
        return "El personaje no es parte del gremio"
    if len(search_user(id_discord)) > 0:
        return "La cuenta de Discord ya esta registrada"
    if len(search_personaje(nombre_personaje)) > 0:
        return "El personaje ya esta registrado"

    Albion_ID = Albion_ID[5]
    MyConexion = Conexion.Conexion()
    MyConexion.crear_conexion()
    cursor = MyConexion.get_conexion().cursor()
    hoy = datetime.today().strftime('%Y-%m-%d')
    SQL_Usuario_Nuevo = ("INSERT INTO player "
                         "(name, Albion_API_ID, Discord_ID, active, last_update, is_alter, guild) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    Datos = (nombre_personaje, Albion_ID, id_discord,1, hoy, 0, 0)
    try:
        cursor.execute(SQL_Usuario_Nuevo, Datos)
        MyConexion.get_conexion().commit()
    except mysql.connector.Error as err:
        MyConexion.get_conexion().rollback()
        print(err)
        cursor.close()
        MyConexion.cerrar_conexion()
        return "Error al registrar la cuenta, favor contactar al administrador"

    cursor.close()
    MyConexion.cerrar_conexion()
    return "Usuario Registrado"


def agregar_alter(id_discord, nombre_personaje):
    Albion_ID = VerificarMiembro.search_name(nombre_personaje)
    if Albion_ID is 0:
        return "El personaje no es parte de la Alianza"
    if len(search_user(id_discord)) == 0:
        return "Aun no te registras, debes Registrarte Ingresando el commando !Reg NombreMain"
    if len(search_personaje(nombre_personaje)) > 0:
        return "El personaje ya esta registrado"
    Albion_ID = Albion_ID[5]
    MyConexion = Conexion.Conexion()
    MyConexion.crear_conexion()
    cursor = MyConexion.get_conexion().cursor()
    hoy = datetime.now()
    SQL_Usuario_Nuevo = ("INSERT INTO player "
                         "(name, Albion_API_ID, Discord_ID, active, last_update, is_alter, guild) "
                         "VALUES (%s, %s, %s,%s, %s, %s, %s)")

    Datos = (nombre_personaje, Albion_ID, id_discord, 1, hoy, 1, 0)
    try:
        cursor.execute(SQL_Usuario_Nuevo, Datos)
        MyConexion.get_conexion().commit()
    except mysql.connector.Error as err:
        print(err)
        cursor.close()
        MyConexion.get_conexion().rollback()
        MyConexion.cerrar_conexion()
    cursor.close()
    MyConexion.cerrar_conexion()
    return "Alter Registrado"


def actualizar_estado(id_discord, nuevo_estado):
    MyConexion = Conexion.Conexion()
    MyConexion.crear_conexion()
    cursor = MyConexion.get_conexion().cursor()
    SQL_Actualizar_Estado = "UPDATE Usuarios SET Estado = %s WHERE UsuarioDiscord = %s"
    datos = (nuevo_estado, id_discord)
    try:
        cursor.execute(SQL_Actualizar_Estado, datos)
        MyConexion.get_conexion().commit()
    except TypeError as e:
        print(e)
        cursor.close()
        MyConexion.get_conexion().rollback()
        MyConexion.cerrar_conexion()
    cursor.close()
    MyConexion.cerrar_conexion()




def get_advertencia(id):
    informacion = search_user(id)
    if len(informacion) > 0:
        MyConexion = Conexion.Conexion()
        MyConexion.crear_conexion()
        cursor = MyConexion.get_conexion().cursor()
    User_Information = ("SELECT * FROM Personajes "
                        "WHERE = %s")


def get_member_list():
    MyConexion = Conexion.Conexion()
    MyConexion.crear_conexion()
    cursor = MyConexion.get_conexion().cursor(buffered=True)
    User_Information = ("SELECT * FROM player")
    Info = None
    try:
        cursor.execute(User_Information)
        MyConexion.get_conexion().commit()
        Info = cursor.fetchall()
    except TypeError as e:
        MyConexion.get_conexion().rollback()
        print(e)
    finally:
        cursor.close()
        MyConexion.cerrar_conexion()
        return Info

def temp_load(data):
    MyConexion = Conexion.Conexion()
    MyConexion.crear_conexion()
    cursor = MyConexion.get_conexion().cursor()
    load_data = ("INSERT INTO postulation_list "
                         "(id_post, postulant_id, recruiter_id, open, close, status, comment, message_id) "
                         "VALUES (%s, %s, %s,%s, %s, %s, %s, %s)")
    try:
        cursor.executemany(load_data, data)
        MyConexion.get_conexion().commit()
    except mysql.connector.Error as err:
        print(err)
        cursor.close()
        MyConexion.get_conexion().rollback()
        MyConexion.cerrar_conexion()
        cursor.close()
        MyConexion.cerrar_conexion()
    cursor.close()
    MyConexion.cerrar_conexion()

def GetCurrentFame():
    MyConexion = Conexion.Conexion()
    MyConexion.crear_conexion()
    cursor = MyConexion.get_conexion().cursor(buffered=True)
    User_Information = ("SELECT p.name, pf.total, pf.pvp, pf.pve, pf.gather, pf.craft, pf.total, pf.id  FROM player_fame as pf, player as p where pf.current = 1 and p.guild <> 0  and p.playerid = pf.playerid  ")
    Info = None
    try:
        cursor.execute(User_Information)
        MyConexion.get_conexion().commit()
        Info = cursor.fetchall()
    except TypeError as e:
        MyConexion.get_conexion().rollback()
        print(e)
    finally:
        cursor.close()
        MyConexion.cerrar_conexion()
        return Info
def load_fame_history():
    con = conection_lite.conection()
    member_list = con.get_member_list()
    today = datetime.now()
    currentData = GetCurrentFame()
    dataMap = {}
    for data in currentData:
        dataMap[data[0].lower()] = data
    data_load = []
    changeList = []
    member_list_db = get_member_list()
    member_list_dictionary = {}
    if member_list_db is not None:

        for member in member_list_db:

            member_list_dictionary[member[1].lower()] = member

        for member in member_list:
            if member[0] in member_list_dictionary and member[0] not in dataMap.keys():
                id = member_list_dictionary[member[0]][0]
                pvp = member[3]
                pve = member[2]
                gather = member[6]
                craft = member[4]
                total = member[1]
                current = 1
                date = today
                data_load.append((id, pvp, pve, gather, craft, total, current, date))
            elif member[0] in member_list_dictionary and member[0] in dataMap.keys() and (member[1] != dataMap[member[0]][1]):
                id = member_list_dictionary[member[0]][0]
                pvp = member[3]
                pve = member[2]
                gather = member[6]
                craft = member[4]
                total = member[1]
                current = 1
                date = today
                changeList.append(dataMap[member[0]][7])
                data_load.append((id, pvp, pve, gather, craft, total, current, date))
    dataLoad = [data_load, changeList]

    load_data_fame(dataLoad)
    print("fama actualizada")

def load_data_fame(data):
    update_current(data[1])
    MyConexion = Conexion.Conexion()
    MyConexion.crear_conexion()
    cursor = MyConexion.get_conexion().cursor()
    load_data = ("INSERT INTO player_fame "
                 "(playerid, pvp, pve, gather, craft, total, current, date) "
                 "VALUES (%s, %s, %s,%s, %s, %s, %s, %s)")
    try:
        cursor.executemany(load_data, data[0])
        MyConexion.get_conexion().commit()
    except mysql.connector.Error as err:
        print(err)
        MyConexion.get_conexion().rollback()
    finally:
        cursor.close()
        MyConexion.cerrar_conexion()


def update_current(data):
    if len(data) > 0:
        print(len(data))
        MyConexion = Conexion.Conexion()
        MyConexion.crear_conexion()
        cursor = MyConexion.get_conexion().cursor()
        load_data = ("UPDATE player_fame SET current = 0 WHERE id IN (%s) ")
        try:
            format_strings = ','.join(['%s'] * len(data))
            cursor.execute(load_data % format_strings, tuple(data))
            MyConexion.get_conexion().commit()
        except mysql.connector.Error as err:
            print(err)
            MyConexion.get_conexion().rollback()
        finally:
            cursor.close()
            MyConexion.cerrar_conexion()


def is_white_list(discord_id):
    con = conection_lite.conection()
    white_list = con.is_white_list(discord_id)
    if white_list is None:
        return True
    else:
        return False
def reg_cta(member_list, time, creator_id):

    MyConexion = Conexion.Conexion()
    MyConexion.crear_conexion()
    cursor = MyConexion.get_conexion().cursor()

    author_info = search_user(creator_id)
    if len(author_info) == 0:
        return "No estas registrado"
    data = []
    today = datetime.now()
    insert_head = "INSERT INTO cta(date, creation_date, creator) VALUES (%s, %s, %s)"
    cta_head = (time, today, author_info[0][0])

    try:
        cursor.execute(insert_head, cta_head)
        MyConexion.get_conexion().commit()
        id_cta = cursor.lastrowid
    except mysql.connector.Error as err:
        print(err)
        MyConexion.get_conexion().rollback()
        cursor.close()
        MyConexion.cerrar_conexion()
        return "Hubo un error al cargar la cta, contactar al administrador"

    txt_list = "====Participante Registrados========\n"
    txt_list_errors = "======Discord con problemas=======\n"
    count = 0
    insert_cta_list = "INSERT INTO cta_player(playerid, id_cta) VALUES (%s, %s)"
    for list in member_list:
        for member in list:
            info = search_user(member.id)
            if len(info) > 0:
                info = info[0]
                if VerificarMiembro.search_name(info[1].lower()) != 0:
                    data.append((info[0], id_cta))
                    if count < 3:
                        txt_list += info[1] + " | "
                        count += 1
                    else:
                        txt_list += info[1] + "\n"
                        count = 0
                else:
                    txt_list_errors+= member.display_name  + "‼️No esta en el gremio ‼️ \n"
            else:
                #Sin Registrar
                txt_list_errors+= member.display_name  + "⚠️No esta registrado ⚠ \n"
    try:
            cursor.executemany(insert_cta_list, data)
            MyConexion.get_conexion().commit()

    except mysql.connector.Error as err:

            print(err)
            MyConexion.get_conexion().rollback()
            cursor.close()
            MyConexion.cerrar_conexion()
            return "Hubo un error al cargar la cta, contactar al administrador"
    txt_list+="\n=====end====="
    txt_list_errors+="=====end====="
    cursor.close()
    MyConexion.cerrar_conexion()
    return txt_list, txt_list_errors

def add_warning(playerid_offender, playerid_creator, url_photo, reason):
    MyConexion = Conexion.Conexion()
    MyConexion.crear_conexion()
    cursor = MyConexion.get_conexion().cursor()
    today = datetime.now()
    new_warning = ("INSERT INTO warning "
                   "(playerid, date, reason, finish_date, creator, photo_url) "
                   "VALUES (%s, %s, %s, %s, %s, %s)")

    data = (playerid_offender, today, reason, today + timedelta(30), playerid_creator, url_photo)

    try:
        cursor.execute(new_warning, data)
        MyConexion.get_conexion().commit()
    except mysql.connector.Error as err:
        print(err)
        cursor.close()
        MyConexion.get_conexion().rollback()
        MyConexion.cerrar_conexion()
        cursor.close()
        MyConexion.cerrar_conexion()
    return "advertencia agregada"

def update_active():
    MyConexion = Conexion.Conexion()
    MyConexion.crear_conexion()
    cursor = MyConexion.get_conexion().cursor()
    conection = conection_lite.conection()
    member_list = conection.get_member_list()
    reset_data = ("UPDATE player SET guild = 0")
    load_data = ("UPDATE player SET guild = %s where name = %s")
    try:
        cursor.execute(reset_data)
        MyConexion.get_conexion().commit()
    except mysql.connector.Error as err:
        print(err)
        MyConexion.get_conexion().rollback()
    data = ""
    for member in member_list:
        if member[7] == "DOOM 1":
            data = (1, member[0])
        else:
            data = (2, member[0])
        try:
            cursor.execute(load_data, data)
            MyConexion.get_conexion().commit()
        except mysql.connector.Error as err:
            print(err)
            MyConexion.get_conexion().rollback()
    cursor.close()
    MyConexion.cerrar_conexion()


def full_check(member_list_disc, rol):

    MyConexion = Conexion.Conexion()
    MyConexion.crear_conexion()
    conection = conection_lite.conection()


    #check alters

    member_list = conection.get_member_list()
    cursor = MyConexion.get_conexion().cursor(buffered=True)
    user_list = ("select p.name as alt, t.name as main   from player as p, "
                 "(SELECT * FROM doom_db.player where is_alter = 0) as t where t.Discord_ID = p.Discord_ID and p.is_alter = 1;")

    member_list_sql = None

    try:
        cursor.execute(user_list)
        MyConexion.get_conexion().commit()
        member_list_sql = cursor.fetchall()
    except mysql.connector.Error as err:
        MyConexion.get_conexion().rollback()
        print(err)
    print("alt:")
    dict_member = {}
    list_active_member = []
    for member in member_list_sql:
        dict_member[member[0].lower()] = member[1].lower()
    for member in member_list:
        list_active_member.append(member[0].lower())
    for member in member_list:
        if member[0].lower() in dict_member.keys():
            if dict_member[member[0].lower()] not in list_active_member:
                print(member[0])
    print("end")
    #check_not_in_discord
    user_list = ("select p.Discord_ID, name from player as p where guild <> 0 and is_alter = 0")

    member_list_sql = None

    try:
        cursor.execute(user_list)
        MyConexion.get_conexion().commit()
        member_list_sql = cursor.fetchall()
    except mysql.connector.Error as err:
        MyConexion.get_conexion().rollback()
        print(err)
    active_disc = {}
    for member in member_list_disc:
        if rol in member.roles:
            active_disc[member.id] = member
    print("disc:")
    for member in member_list_sql:
        if int(member[0]) not in active_disc.keys():
            print(member[1])
    print("end")


    print("end")
    cursor.close()
    MyConexion.cerrar_conexion()


def get_active_war(discord_id):
    info_user = search_user(discord_id)
    if info_user is not None and len(info_user) > 0:
        MyConexion = Conexion.Conexion()
        MyConexion.crear_conexion()
        cursor = MyConexion.get_conexion().cursor(buffered=True)
        date = datetime.now()
        get_warning = ("SELECT * FROM warning "
                       "WHERE finish_date> %s  and playerid= %s")
        Data = (date, info_user[0][0])
        warning_list = None
        try:
            cursor.execute(get_warning, Data)
            MyConexion.get_conexion().commit()
            Info = cursor.fetchall()
            if len(Info) > 0:
                warning_list = Info
        except TypeError as e:
            MyConexion.get_conexion().rollback()
            print(e)
        finally:
            cursor.close()
            MyConexion.cerrar_conexion()
            return warning_list
    return False