import sqlite3

class conection:
    def __init__(self):
        self.con = None

    def open_con(self):
        self.con = sqlite3.connect("member_list.db")

    def close_con(self):
        self.con.close()

    def load_data(self, members):
        self.delete_data()
        self.open_con()
        query = "INSERT INTO members(name, total_fame, pve_fame, pvp_fame, crafting_fame, ID, gather_fame,guild)  VALUES (?,?,?,?,?,?,?,?)"
        cur = self.con.cursor()
        cur.executemany(query, members)

        self.con.commit()
        cur.close()
        self.close_con()

    def delete_data(self):
        self.open_con()

        cur = self.con.cursor()
        cur.execute('DELETE FROM members;')

        self.con.commit()
        cur.close()
        self.close_con()

    def search_name(self, name):
        self.open_con()
        name = (name,)
        cur = self.con.cursor()
        member = None
        try:
            cur.execute('select * FROM members WHERE name = ?',name)
            member = cur.fetchone()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:

            self.con.commit()
            cur.close()
            self.close_con()

        return member

    def get_member_list(self):
        self.open_con()
        cur = self.con.cursor()

        cur.execute('select * FROM members')

        members = cur.fetchall()

        cur.close()
        self.close_con()

        return members
    def get_white_list(self):
            self.open_con()
            cur = self.con.cursor()
            white_list = None
            try:
                cur.execute('select * FROM white_list')
                white_list = cur.fetchall()
            except sqlite3.Error as error:
                print("Error while connecting to sqlite", error)
            finally:
                cur.close()
                self.close_con()
                return white_list
    def is_white_list(self, discord_id):
        self.open_con()
        cur = self.con.cursor()
        white_list = None
        try:
            cur.execute('select * FROM white_list where discord_id = ?',(discord_id,))
            white_list = cur.fetchone()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            cur.close()
            self.close_con()
            return white_list
