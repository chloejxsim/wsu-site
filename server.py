from flask import Flask, render_template, request, redirect, url_for
from db_functions import run_search_query_tuples
from datetime import datetime

app = Flask ( __name__ )
db_path = 'data/wsusite_db.sqlite'


@app.template_filter()
def news_date(sqlite_dt):
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %Y %H:%M")

@app . route ('/')
def index():
    return render_template("index.html")

@app . route ('/competitions')
def competitions():
    return render_template("competitions.html")

@app . route ('/resources')
def resources():
    return render_template("resources.html")

@app . route ('/news')
def news():
    # query for the page
    sql = """select news.news_id, news.title, news.subtitle, news.content, news.newsdate, member.name
        from news
        join member on news.member_id= member.member_id
        order by news.newsdate desc;
    """
    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)
    return render_template("news.html", news=result)

if __name__ == "__main__":
    app.run(debug=True)