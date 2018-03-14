"""
    DB operations
"""
from __future__ import print_function
from db_management.query_execution. \
    db_connector import execute_select_sql


def fetch_concepts():
    sql = "SELECT * FROM derived.concept"
    result = execute_select_sql(sql, [])
    return result


def fetch_parents(cid1, distance):
    """
    fetch parent concepts whose distance is equal or less than 3 from
    specified concept
        :param cid1:
        :param distance:
    """
    parameters = []
    # assume that cid2s are the parents of cid1
    sql = '''
        SELECT cui FROM derived.concept WHERE cid in (
            SELECT cid2 FROM derived.isa WHERE cid1 = %s and distance <= %s
        )
    '''
    parameters.append(cid1)
    parameters.append(distance)
    result = execute_select_sql(sql, parameters)
    return result


def fetch_semantic_type(cid):
    """
    fetch semantic type with specified cid
        :param cid:
    """
    parameters = []
    results = {}
    sql = """
        SELECT tui FROM derived.sty WHERE cid = %s
    """
    parameters.append(cid)
    results = execute_select_sql(sql, parameters)
    if len(results) > 0:
        # one cid refers to one sty
        result = [row['tui'] for row in results][0]
    else:
        result = ""

    return result


def fetch_sab(stringName, cid):
    """
    fetch particular ontology
        :param cid:
        :param stringName:
    """
    parameters = []
    results = {}
    sql = """
        SELECT * FROM derived.sab WHERE sid = (
            SELECT sid from derived.synonym WHERE tid = (
                SELECT tid from derived.term WHERE str = %s
            ) AND cid = %s
        )
    """
    parameters.append(stringName)
    parameters.append(cid)
    results = execute_select_sql(sql, parameters)
    # stringName and cid determine one sab
    if len(results) > 0:
        result = [row['str'] for row in results][0]
    else:
        result = ""

    return result


def main():
    result = fetch_concepts()
    for row in result:
        print(row["cui"], row["str"])
    # result = fetch_parents(1, 3)

    # result = fetch_semantic_type(1)
    # print([row['tui'] for row in result])
    # for row in result:
    #     print(row['tui'])

    # result = fetch_parents(1, 3)
    # parents = []
    # for row in result:
    #     parents.append(row['cui'])
    # print(parents)
    # result = fetch_sab("acs", "C1232")


if __name__ == "__main__":
    main()
