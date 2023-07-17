from db_functions import run_search_query_tuples

def get_comments(db_path):
    sql="""select news.news_id,news.title,news.subtitle, news.content, comment.comment, member.firstname
     from news
     left join comment on news.news_id = comment.news_id
     left join member on comment.member_id = member.member_id
     order by news.newsdate desc
     """
    result = run_search_query_tuples(sql, (), db_path, True)

    newsID = 0

    for row in result:
        if row['news_id'] != newsID:
            news_item = "{} {} {}".format(row['news_id'], row['title'], row['subtitle'])
            print(news_item)
            comment = "{} {}".format(row['comment'], row['firstname'])
            print(comment)
            newsID = row['news_id']
        else:
            comment = "{} {}".format(row['comment'], row['firstname'])
            print(comment)




if __name__ == "__main__":
    db_path = 'data/wsusite_db.sqlite'
    get_comments(db_path)
