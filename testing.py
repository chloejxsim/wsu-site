from db_functions import run_search_query_tuples


def get_schedule(db_path):
    sql = """select schedule.event, schedule.description, schedule.scheduledate, schedule.location
        from schedule
        join member on schedule.member_id = member.member_id;
    """
    result = run_search_query_tuples(sql, (), db_path, True)

    for row in result:
       for k in row.keys():
           print(k)
           print(row[k])



if __name__ == "__main__":
    db_path = 'data/wsusite_db.sqlite'
    get_schedule(db_path)
