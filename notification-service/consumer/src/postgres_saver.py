from dataclasses import dataclass

from psycopg2.extensions import connection as _connection
from models.notifications import Message


class PostgresSaver:
    def __init__(self, connection: _connection):
        self.data = {}
        self.connection = connection

        self.page_size = 100

    def insert_message(self, data: Message) -> None:

        insert_sql = """INSERT INTO notify.messages(id, created, modified, address, source, subject, text, send_at, status)
         values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        curs = self.connection.cursor()
        try:
            curs.execute(insert_sql, (str(data.id), data.created, data.modified, data.address, data.source, data.subject, data.text, data.send_at, data.status))

            self.connection.commit()

        except Exception as error:
            if self.connection:
                self.connection.rollback()
            print(str(error))
            raise

        finally:
            curs.close()

    def update_message(self, data: Message) -> None:

        update_sql = """UPDATE notify.messages set modified=%s, status=%s where id=%s"""

        curs = self.connection.cursor()
        try:
            curs.execute(update_sql, (data.modified, data.status, str(data.id)))

            self.connection.commit()

        except Exception as error:
            if self.connection:
                self.connection.rollback()
            print(str(error))
            raise

        finally:
            curs.close()
