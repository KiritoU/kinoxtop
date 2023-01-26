import sys

import mysql.connector

from settings import CONFIG


class Database:
    def get_conn(self):
        config = {
            "user": CONFIG.user,
            "password": CONFIG.password,
            "host": CONFIG.host,
            "port": CONFIG.port,
            "database": CONFIG.database,
        }
        try:
            return mysql.connector.connect(**config)
        except Exception as e:
            print(f"Error connecting to Database: {e}")
            sys.exit(1)

    def select_with(self, query: str) -> list:
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        conn.close()

        return res

    def select_all_from(self, table: str, condition: str = "1=1", cols: str = "*"):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(
            f"SELECT {cols} FROM {CONFIG.TABLE_PREFIX}{table} WHERE {condition}"
        )
        res = cur.fetchall()
        cur.close()
        conn.close()

        return res

    def insert_into(self, table: str, data: tuple = None):
        conn = self.get_conn()
        cur = conn.cursor()

        columns = f"({', '.join(CONFIG.INSERT[table])})"
        values = f"({', '.join(['%s'] * len(CONFIG.INSERT[table]))})"
        query = f"INSERT INTO {CONFIG.TABLE_PREFIX}{table} {columns} VALUES {values}"
        cur.execute(query, data)
        id = cur.lastrowid

        conn.commit()
        cur.close()
        conn.close()
        return id

    def update_table(
        self, table: str, set_cond: str, where_cond: str, data: tuple = ()
    ):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(
            f"UPDATE {CONFIG.TABLE_PREFIX}{table} set {set_cond} WHERE {where_cond}",
            data,
        )
        conn.commit()
        cur.close()
        conn.close()

    def delete_from(self, table: str = "", condition: str = "1=1"):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {CONFIG.TABLE_PREFIX}{table} WHERE {condition}")
        conn.commit()
        cur.close()
        conn.close()

    def select_or_insert(self, table: str, condition: str, data: tuple):
        res = self.select_all_from(table=table, condition=condition)
        if not res:
            self.insert_into(table, data)
            res = self.select_all_from(table, condition=condition)
        return res


database = Database()


def test_select(post_id: int = 241183):
    res = database.select_all_from(table="posts", condition=f"ID={post_id}")
    print(res)


if __name__ == "__main__":
    test_select()
