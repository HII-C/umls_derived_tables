from query_execution.db_connector import execute_insert_sql


def populate_table_sab():
    """
    populate table sab with data from umls.MRSAB
    """
    sql = '''
        INSERT INTO derived.sab (str)
            SELECT DISTINCT RSAB
            FROM umls.MRSAB;
    '''
    execute_insert_sql(sql, [])


def main():
    populate_table_sab()


if __name__ == "__main__":
    main()
