from flask import Flask, render_template

app = Flask ( __name__ )

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
    return render_template("news.html")

if __name__ == "__main__":
    app.run(debug=True)