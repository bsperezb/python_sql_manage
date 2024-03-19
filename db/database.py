import psycopg2
import logging

class Database:
    def __init__(self, host, port, user, password, database):
        self.connection = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result

        except psycopg2.Error as e:
            logging.error(f"Error al ejecutar la consulta: {e}")
            return None

    def execute_insert_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            logging.info("Operación de inserción exitosa.")
            return True

        except psycopg2.Error as e:
            self.connection.rollback()
            logging.error(f"Error al ejecutar la consulta de inserción: {e}")
            return False

    def execute_delete_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            logging.info("Operación de eliminación exitosa.")
            return True

        except psycopg2.Error as e:
            self.connection.rollback()
            logging.error(f"Error al ejecutar la consulta de eliminación: {e}")
            return False 

    def get_user_by_id(self, id):
        query = ( f'SELECT id, "name", email, "clientId"'
            f'FROM channel."user"'
            f'WHERE id = {id};')
        return self.execute_query(query)

    def get_user_by_email(self, id):
        query = ( f'SELECT id, "name", email, "clientId"'
            f'FROM channel."user"'
            f'WHERE email = {id};')
        return self.execute_query(query)

    def delet_user_by_id(self, id):
        query = ( f' DELETE FROM channel."user"'
            f'WHERE id = {id};')
        return self.execute_delete_query(query)

    def delet_client_by_id(self, id):
        query = ( f' DELETE FROM channel."client"'
            f'WHERE id = {id};')
        return self.execute_delete_query(query)
