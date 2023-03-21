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
    return "<h1>resources</h1>"

@app . route ('/news')
def news():
    return "<h1>news</h1>"

if __name__ == "__main__":
    app.run(debug=True)