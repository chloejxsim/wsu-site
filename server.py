from flask import Flask, render_template

app = Flask ( __name__ )

@app . route ('/')
def index():
    return

@app . route ('/competitions')
def competitions():
    return "<h1>competitions</h1>"

@app . route ('/resources')
def resources():
    return "<h1>resources</h1>"

@app . route ('/news')
def news():
    return "<h1>news</h1>"

if __name__ == "__main__":
    app.run(debug=True)