from flask import Flask, render_template, request, redirect, url_for
from db_functions import run_search_query_tuples, run_commit_query
from datetime import datetime

app = Flask ( __name__ )
db_path = 'data/wsusite_db.sqlite'

@app.template_filter()
def news_date(sqlite_dt):
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %Y %H:%M")

@app.route ('/')
def index():
    return render_template("index.html")

@app.route ('/competitions')
def competitions():
    return render_template("competitions.html")

@app.route ('/resources')
def resources():
    return render_template("resources.html")

@app.route ('/news')
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

@app.route ('/news_cud', methods=["GET", "POST"])
def news_cud():
    #collect data from the web address
    data = request.args
    required_keys = ['id','task']
    for k in required_keys:
        if k not in data.keys():
            message = "Do not know what to do with read update on news (key not present)"
            return render_template('error.html', message=message)
    # have an ID and a task key
    if request.method == "GET":
        if data['task'] == 'delete':
            sql = "delete from news where news_id = ?"
            values_tuple = (data['id'],)
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news'))
        elif data['task'] == 'update':
            sql = """ select title, subtitle, content from news where news_id=?"""
            values_tuple = (data['id'])
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("news_cud.html",
                                    **result,
                                   id=data['id'],
                                   task=data['task'])
        elif data['task'] == 'add':
            temp = {'title': 'Test Title', 'subtitle': 'Test subtitle', 'content': 'Test content' }
            return render_template("news_cud.html",
                                   id=0,
                                   task=data['task'],
                                   **temp)
        else:
            message = "Unrecognised task coming from news page"
            return render_template('error.html', message=message)
    elif request.method == "POST":
        # collected form information
        f = request.form
        print(f)
        if data['task'] == 'add':
            # add new news entry to the database
            # member is fixed for now
            sql = """insert into news(title,subtitle,content, newsdate, member_id)
                        values(?,?,?, datetime('now', 'localtime'),2)"""
            values_tuple = (f['title'], f['subtitle'], f['content'])
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news'))
        elif data['task'] == 'update':
            sql = """update news set title=?, subtitle=?, content=?, newsdate=datetime('now') where news_id=?"""
            values_tuple = (f['title'], f['subtitle'], f['content'], data['id'])
            result = run_commit_query(sql, values_tuple, db_path)
            # collect the data from the form and update the database at the sent id
            return redirect(url_for('news'))
        else:
            # let's put in an error catch
            message = "Unrecognised task coming from news form submission"
            return render_template('error.html', message=message)

@app.route ('/login', methods=["GET", "POST"])
def login():
    error = "Your credentials are not recognised"
    if request.method == "GET":
        return render_template("log-in.html", email='m@g.com', password="temp")
    elif request.method == "POST":
        f = request.form
        print(f)
        sql = """ select name, password, authorisation from member where email = ?"""
        values_tuple=(f['email'],)
        result = run_search_query_tuples(sql, values_tuple, db_path, True)
        if result:
            result = result[0]
            if result['password'] == f['password']:
                print("Log in okay")
                return redirect(url_for('index'))
            else:
                return render_template("log-in.html", email='m@g.com', password="temp", error=error)
        else:
            return render_template("log-in.html", email='m@g.com', password="temp", error=error)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        f = request.form
        return render_template("confirm.html", form_data=f)
    elif request.method == "GET":
        carried_data = request_args
        print(carried_data)
        if len(carried_data) == 0:
            temp_form_data = {
                "firstname": "James",
                "secondname": "Lovelock",
                "email": "jl@gmail.com",
                "aboutme": "I have been in love with Italian food all my life"
            }
            # temp_form_data = {}
        else:
            temp_form_data = carried_data
        return render_template("signup.html", **temp_form_data)


if __name__ == "__main__":
    app.run(debug=True)