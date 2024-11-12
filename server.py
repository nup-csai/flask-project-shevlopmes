from flask import Flask

app = Flask(__name__)
class Player:
    def __init__ (self, name, status):
        self.name = name
        self.status = status
        self.wins= 0
        self.losses =0
    def change_name (self,name):
        self.name = name
    def change_status(self,status):
        self.status = status
    def add_win(self, add):
        self.wins += add
    def add_loss(self,add):
        self.losses+=add
p = [Player("$i","active") for i in range(5)]
@app.route('/')
def home():
    return 'Hello World!'
@app.route('/getall/<int=id>')
def allinfo(id):
    return '$p[id].name \n$p[id].status \n$p[id].wins \n$p[id].losses'

