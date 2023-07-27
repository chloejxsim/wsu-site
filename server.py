import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session
from db_functions import run_search_query_tuples, run_commit_query
from datetime import datetime

app = Flask ( __name__ )
app.secret_key = "sjklfdsjlfajdalksf"
db_path = 'data/wsusite_db.sqlite'

@app.template_filter()
def news_date(sqlite_dt):
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %Y %H:%M")

@app.template_filter()
def schedule_date(sqlite_dt):
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %Y %H:%M")

@app.route ('/')
def index():
    return render_template("index.html")

@app.route ('/competitions')
def competitions():
    return render_template("competitions.html")

@app.route ('/premieradvanced')
def premieradvanced():
    sql = """select draw_id, grade, round, affirming, negating, winner from draw where grade='Prem A'"""
    result = run_search_query_tuples(sql,(),db_path,True)
    return render_template("premieradvanced.html", draw=result)

@app.route ('/premierb')
def premierb():
    return render_template("premierb.html")

@app.route ('/seniorcert')
def seniorcert():
    return render_template("seniorcert.html")

@app.route ('/juniorprem')
def juniorprem():
    sql = """select draw_id, grade, round, affirming, negating, winner from draw where grade='Junior Prem'"""
    result = run_search_query_tuples(sql,(),db_path,True)
    return render_template("juniorprem.html", draw=result)

@app.route ('/juniorcert')
def juniorcert():
    return render_template("juniorcert.html")

@app.route ('/resources')
def resources():
    return render_template("resources.html")

@app.route ('/news')
def news():

    # query for the recent news portion of the page
    sql = """select news.news_id, news.title, news.subtitle, news.content, news.newsdate, member.firstname
        from news
        join member on news.member_id = member.member_id
        order by news.newsdate desc;
    """
    news_items = run_search_query_tuples(sql, (), db_path, True)
    sql="""select news.news_id,news.title,news.subtitle, news.content, comment.comment, member.firstname
     from news
     left join comment on news.news_id = comment.news_id
     left join member on comment.member_id = member.member_id
     order by news.newsdate desc
     """
    comments = run_search_query_tuples(sql, (), db_path, True)
    #news = run_search_query_tuples(sql, (), db_path, True)
    # query for the schedule portion of the page
    sql = """select schedule.post_id, schedule.event, schedule.description, schedule.scheduledate, schedule.location, member.firstname
        from schedule
        join member on schedule.member_id = member.member_id
        order by schedule.scheduledate desc;
    """
    schedule = run_search_query_tuples(sql, (), db_path, True)

    return render_template("news.html", news=news_items, comments=comments, schedule=schedule)

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
            sql = """insert into news(title, subtitle, content, newsdate, member_id)
                        values(?,?,?, datetime('now', 'localtime'),?)"""
            values_tuple = (f['title'], f['subtitle'], f['content'], session['member_id'])
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

@app.route ('/schedule_cud', methods=["GET", "POST"])
def schedule_cud():
    data = request.args
    required_keys = ['id','task']
    for k in required_keys:
        if k not in data.keys():
            message = "Do not know what to do with read update on schedule (key not present)"
            return render_template('error.html', message=message)
    if request.method == "GET":
        if data['task'] == 'delete':
            sql = "delete from schedule where post_id = ?"
            values_tuple = (data['id'],)
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news'))
        elif data['task'] == 'update':
            sql = """ select event, description, scheduledate, location from schedule where post_id=?"""
            values_tuple = (data['id'])
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("schedule_cud.html",
                                   **result,
                                   id=data['id'],
                                   task=data['task'])
        elif data['task'] == 'add':
            return render_template("schedule_cud.html",
                                   id=0,
                                   task=data['task'])
        else:
            message = "Unrecognised task coming from news page"
            return render_template('error.html', message=message)
    elif request.method == "POST":
        f = request.form
        print(f)
        if data['task'] == 'add':
            sql = """ insert into schedule(event, description, scheduledate, location, member_id)
             values(?, ?, ?, ?, ?)"""
            sdate = f["scheduledate"].replace("T", " ")+":00"
            values_tuple = (f["event"], f["description"], sdate, f["location"],1)
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news'))
        elif data['task'] == 'update':
            sql = """update schedule set event=?, description=?, location=?, scheduledate=datetime('now') where post_id=?"""
            values_tuple = (f["event"], f["description"], f["scheduledate"], f["location"], data['id'])
            result = run_commit_query(sql, values_tuple, db_path)
            # collect the data from the form and update the database at the sent id
            return redirect(url_for('news'))
        else:
            # let's put in an error catch
            message = "Unrecognised task coming from news form submission"
            return render_template('error.html', message=message)

@app.route ('/comment_cud', methods=["GET", "POST"])
def comment_cud():
    #collect data from the web address
    data = request.args
    if request.method == "GET":
        required_keys = ['id', 'task']
    elif request.method == "POST":
        required_keys = ['news_id','member_id','task']

    for k in required_keys:
        if k not in data.keys():
            message = "Do not know what to do with read update on news (key not present)"
            return render_template('error.html', message=message)
    if request.method == "GET":
        if data['task'] == 'delete':
            sql = "delete from comment where comment_id = ?"
            values_tuple = (data['id'],)
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news'))
    elif request.method == "POST":
        f = request.form
        if data['task'] == 'add':
            sql = """insert into comment(news_id, member_id, comment, commentdate)
                values(?, ?, ?, datetime('now', 'localtime'))
                """
            values_tuple = (data['news_id'], data['member_id'], f['comment'])
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news') + "#" + data['news_id'])

@app.route ('/login', methods=["GET", "POST"])
def login():
    print(session)
    error = "Your credentials are not recognised"
    if request.method == "GET":
        return render_template("log-in.html", email='m@g.com', password="temp")
    elif request.method == "POST":
        f = request.form
        sql = """ select member_id, firstname, password, authorisation from member where email = ?"""
        values_tuple=(f['email'],)
        result = run_search_query_tuples(sql, values_tuple, db_path, True)
        if result:
            result = result[0]
            if result['password'] == f['password']:
                #start a session
                session['firstname']=result['firstname']
                session['authorisation']=result['authorisation']
                session['member_id'] = result['member_id']
                print(session)
                return redirect(url_for('index'))
            else:
                return render_template("log-in.html", email='m@g.com', password="temp", error=error)
        else:
            return render_template("log-in.html", email='m@g.com', password="temp", error=error)

@app.route ('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/signup', methods=["GET", "POST"])
def signup():
    referrer = request.referrer
    print(referrer)
    if request.method == "GET":
        temp_form_data = {
            "firstname": "James",
            "lastname": "Lovelock",
            "email": "jl@gmail.com",
            "password": "temp",
        }
        return render_template("signup.html", **temp_form_data)
    elif request.method == "POST":
        f = request.form
        sql = """insert into member(firstname, lastname, email, password, authorisation)
                    values(?,?,?,?,1)"""
        values_tuple = (f['firstname'], f['lastname'], f['email'], f['password'])
        result = run_commit_query(sql, values_tuple, db_path)
        # assuming successful go to log-in
        return render_template("log-in.html", form_data=f)
    else:
        # if result is a problem go to error page
        message = "Unrecognised task coming from signup form submission"
        return render_template('error.html', message=message)




if __name__ == "__main__":
    app.run(debug=True)