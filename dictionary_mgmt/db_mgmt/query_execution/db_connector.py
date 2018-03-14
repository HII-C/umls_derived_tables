'''
Create MySQL database connection, and execute query with specified sql statment
'''
from __future__ import print_function
import pymysql.cursors


class db_connector_factory(object):
    """
    build db_connection
        :param object:
    """

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        # self.database = database

    def db_connection(self):
        connection = pymysql.connect(host=self.host,
                                     user=self.user,
                                     password=self.password,
                                     # db=self.database,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        # alternative, corson = connection.cursor(as_dict=True)
        return connection


def execute_select_sql(sql, parameters):
    """
    execute specified select sql statment
        :param sql:
        :param parameters:
    """
    connection = db_connector_factory(
        "localhost", "root", "wtzhou").db_connection()
    length = len(parameters)
    try:
        with connection.cursor() as cursor:
            if length <= 0:
                cursor.execute(sql)
            else:
                cursor.execute(sql, tuple(parameters))
            # the data will be fetched as dictionaries instead of
            # tuples due to cursorclass
            result = cursor.fetchall()
            return result

    except pymysql.DatabaseError as err:
        print("errors: ", err.args)
    finally:
        connection.close()


def execute_insert_sql(sql, parameters):
    """
    insert new records into specified table
        :param sql:
        :param parameters:
    """
    connection = db_connector_factory(
        "localhost", "root", "wtzhou"
    ).db_connection()
    length = len(parameters)
    try:
        with connection.cursor() as cursor:
            if length <= 0:
                cursor.execute(sql)
            else:
                cursor.execute(sql, tuple(parameters))
        # connection is not autocommit by default, so you must
        # commit to save changes
        connection.commit()
    except pymysql.DatabaseError as err:
        print("errors: ", err.args)
        # rollback in case there is any error
        connection.rollback()
    finally:
        connection.close()


def main():
    # sql = "SELECT * FROM derived.concept"
    # result = execute_select_sql(sql, [])
    # for row in result:
    #     print(row["cui"], row["str"])
        # print(row)

    parameters = []
    sql = '''
        insert into test.mrconso(cui, str, sab, preferedName)
        values (%s, %s, %s, %s);
    '''
    parameters.append("C0001")
    parameters.append("term2")
    parameters.append("SNOMED")
    parameters.append("term21")
    execute_insert_sql(sql, parameters)


if __name__ == '__main__':
    main()
