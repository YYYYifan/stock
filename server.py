from flask import Flask, render_template
import json

with open("../result.json") as f:
    data = json.load(f)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return('Hello, World!')

@app.route("/hello", methods=['GET', 'POST'])
def Hello():
    message = "hello"
    return render_template("temp.html", temp=message)

@app.route("/index")
def test():    
    title = ["", "市场", "代码", "MA60 天 涨幅", "MA60 30分钟 涨幅"]

    return render_template("table.html",LAST_UPDATE = data["LastUpdate"], date=data["Date"], codeAmount=len(data["Data"]), labels=title, content=data["Data"])



if __name__ == '__main__':
    app.run(host = '192.168.2.119', port=8080, debug=True)