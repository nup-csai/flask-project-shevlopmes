from flask import Flask

app = Flask(__name__)
a = [{
    "name":"Maksim Shevkoplias",
    "status": "active",
    "wins":239,
    "losses": 1},
    {
    "name": "Sasha Valerian",
        "status": "active",
        "wins":500,
        "losses":0},
    {
        "name":"Timur Degteari",
        "status": "sleeping",
        "wins":20,
        "losses":31},
    {"name": "Stepan Maliarovskiy",
     "status": "unavailable",
     "wins": 97,
     "losses":40
}]
@app.route('/')
def home():
    return 'Hello World!'
@app.route('/get/<int:id>/<string:arg>')
def allinfo(id,arg):
    if(id<0 or id >= len(a)):
        return "ID out of range", 404
    value =  a[id].get(arg)
    if value is None:
        return "Value not found", 404
    return str(value)


if __name__ == '__main__':
    app.run(debug=True)