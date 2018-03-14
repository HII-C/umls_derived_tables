# from .db_management import db_connector
from query_execution.db_connector import execute_insert_sql


def populate_table_concept():
    """
    populate table derived.concept with data from umls.MRCONSO
    """
    sql = '''
        INSERT INTO derived.concept (cui, str)
            SELECT DISTINCT
                CUI,
                STR
            FROM umls.MRCONSO
            WHERE CUI IN (
                SELECT DISTINCT CUI
                FROM umls.MRCONSO
                WHERE SAB IN ("RXNORM", "ICD10CM", "ICD9CM", "SNOMEDCT_US",
                 "CPT", "LNC", "NDFRT")
            ) AND LENGTH(STR) <= 255 AND ISPREF = 'Y' AND LAT = 'ENG' 
            AND STT = 'PF' AND TS = 'P'
    '''
    execute_insert_sql(sql, [])


def main():
    sql = '''
        INSERT INTO derived.concept (cui, str)
            SELECT DISTINCT
                CUI,
                STR
            FROM test.mrconso
            WHERE CUI IN (
                SELECT DISTINCT CUI
                FROM test.mrconso
                WHERE SAB IN ("RXNORM", "SNOMED")
            )
    '''
    execute_insert_sql(sql, [])


if __name__ == "__main__":
    main()
