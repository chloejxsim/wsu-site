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










if __name__ == "__main__":
    db_path = 'data/wsusite_db.sqlite'
    get_comments(db_path)
