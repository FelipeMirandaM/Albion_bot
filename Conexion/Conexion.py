import mysql
from configparser import ConfigParser
from mysql.connector import (connection)
from mysql.connector import errorcode


class Conexion:
    def __init__(self):
        self.Conexion = None

    def crear_conexion(self):
        config_object = ConfigParser()
        config_object.read("config.ini")
        userInfo = config_object["USERINFO"]
        serverConfig = config_object["SERVERCONFIG"]
        try:
            self.Conexion = connection.MySQLConnection(user=userInfo['user'],
                                                       password=userInfo['password'],
                                                       host=serverConfig['host'],
                                                       database=serverConfig['database'])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def get_conexion(self):
        return self.Conexion

    def cerrar_conexion(self):
        self.Conexion.close()
