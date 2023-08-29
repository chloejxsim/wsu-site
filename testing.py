from db_functions import run_search_query_tuples

def get_comments(db_path):
    sql="""select news.news_id,news.title,news.subtitle, news.content
     from news
     order by news.newsdate desc
     """
    news_items = run_search_query_tuples(sql, (), db_path, True)
    sql="""select news.news_id,news.title,news.subtitle, news.content, comment.comment, member.firstname
     from news
     left join comment on news.news_id = comment.news_id
     left join member on comment.member_id = member.member_id
     order by news.newsdate desc
     """
    comments = run_search_query_tuples(sql, (), db_path, True)
    for row in news_items:
        print(row['title'])
        for com in comments:
            if com['news_id'] == row['news_id']:
                print(com['comment'])

def get_news(db_path):
    sql = """select news.title, news.subtitle, news.content, member.firstname
        from news
        join member on news.member_id = member.member_id;
    """
    result = run_search_query_tuples(sql, (), db_path, True)

    for row in result:
        for k in row.keys():
            print(k)
            print(row[k])

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

def get_draw(db_path):
    sql = """select draw_id, grade, round, affirming, negating, winner from draw where grade='Prem A'"""
    result = run_search_query_tuples(sql, (), db_path, True)

    for row in result:
     for k in row.keys():
        print(k)
        print(row[k])

if __name__ == "__main__":
    db_path = 'data/wsusite_db.sqlite'
    #get_news(db_path)
    #get_schedule(db_path)
    get_draw(db_path)
    #get_comments(db_path)

