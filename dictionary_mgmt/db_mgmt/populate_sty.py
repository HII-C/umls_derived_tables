from query_execution.db_connector import execute_insert_sql, execute_select_sql


def populate_table_sty():
    # sql = '''
    #     INSERT INTO derived.sty (cid, tui, sid)
    #         SELECT
    #             derived.concept.cid,
    #             tui,
    #             sid
    #         FROM umls.MRSTY
    #         JOIN derived.concept ON derived.concept.cui = umls.MRSTY.cui
    #         JOIN derived.synonym ON derived.concept.cid = derived.synonym.cid;
    # '''
    sql = '''
        SELECT
            derived.concept.cid,
            tui,
            sid
        FROM umls.MRSTY
        JOIN derived.concept ON derived.concept.cui = umls.MRSTY.cui
        JOIN derived.synonym ON derived.concept.cid = derived.synonym.cid;
    '''
    # results = execute_select_sql(sql, [])
    # for row in results:
    '''
    TODO: need to map tui to semantic group not availale right now,
    and the semantic group, e.g. drug, procedure, etc. will be
    saved into table sty, rather than tui.
    '''
