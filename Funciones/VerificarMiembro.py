from Conexion import conection_lite
def search_name(name):
    con = conection_lite.conection()
    member = con.search_name(name)
    if member is None:
        return 0
    else:
        return member



