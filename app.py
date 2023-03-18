from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/character")
def character():
    print("Yes")
    return render_template("character.html")

@app.route("/lunchlist")
def lunchlist():
    print("Yes")
    return render_template("lunchlist.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')