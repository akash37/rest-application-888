import mysql.connector
from mysql.connector import Error
import config


class DBConnect:

    @staticmethod
    def get_connection_object():
        try:
            connection = mysql.connector.connect(host=config.host_address,
                                                 database=config.database_name,
                                                 user=config.user_name,
                                                 password=config.password)

            return connection

        except Error as e:
            print("Error while connecting to MySQL", e)
