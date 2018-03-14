from query_execution.db_connector import execute_insert_sql


def populate_table_term():
    sql = '''
        INSERT INTO derived.term (str)
            SELECT DISTINCT str
            FROM umls.MRCONSO
            WHERE length(STR) <= 255 AND LAT = 'ENG';
    '''
    execute_insert_sql(sql, [])


def main():
    populate_table_term()


if __name__ == "__main__":
    main()
