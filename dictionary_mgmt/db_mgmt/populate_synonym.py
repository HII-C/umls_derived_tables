from query_execution.db_connector import execute_insert_sql


def populate_table_synonym():
    """
    populate table synonym with data from MRCONSON
    """
    sql = '''
        INSERT INTO derived.synonym (tid, cid, sid)
            SELECT
                tid,
                cid,
                sid
            FROM umls.MRCONSO
            JOIN derived.term ON umls.MRCONSO.str = derived.term.str
            JOIN derived.sab ON derived.sab.str = umls.MRCONSO.sab
            JOIN derived.concept ON derived.concept.cui = umls.MRCONSO.cui
            WHERE length(umls.MRCONSO.str) <= 255 AND LAT = 'ENG';
    '''
    execute_insert_sql(sql, [])


def main():
    populate_table_synonym()


if __name__ == "__main__":
    main()
