from flask import Flask, render_template
from database import get_all_games
from database import get_one_game
from database import change_game
from database import get_scoreboard
from database import create_contest
from database import add
from database import remove
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('base_page.html')


@app.route('/contests/<int: contest_id>/games', methods=['GET'])
def all_games(contest_id):
    output = get_all_games(contest_id)
    if output is None:
        return render_template('incorrect_page.html')
    return render_template('games.html', games=output)


@app.route('/contests/<int: contest_id>/games/<int: game_id>', methods = ['GET'])
def one_game(contest_id, game_id):
    output = get_one_game(contest_id, game_id)
    if output is None:
        return render_template('incorrect_page.html')
    return render_template('one_game.html', game=output)

@app.route('/contests/<int: contest_id>/games/<int: game_id>', methods = ['POST'])
def change(contest_id, game_id):
    live_status = request.form.get('live')
    p1 = request.form.get('p1')
    p2 = request.form.get('p2')
    change_game(contest_id,game_id,live_status,p1,p2)
    output = get_one_game(contest_id, game_id)
    if output is None:
        return render_template('incorrect_page.html')
    return render_template('one_game.html',game=output)

@app.route('/contests/<int: contest_id>/scoreboard', methods = ['GET'])
def scoreboard(contest_id):
    participants_sorted = get_scoreboard(contest_id,0)
    if participants_sorted is None:
        return render_template('incorrect_page.html')
    return render_template('scoreboard.html', scoreboard = participants_sorted)

@app.route('/contests/<int: contest_id>/scoreboard/live', methods = ['GET'])
def scoreboard(contest_id):
    participants_sorted = get_scoreboard(contest_id,1)
    if participants_sorted is None:
        return render_template('incorrect_page.html')
    return render_template('scoreboard.html', scoreboard = participants_sorted)

@app.route('/new_contest', methods=['GET'])
def new_contest():
    new_id = create_contest()
    return render_template('new_contest.html', id=new_id)

@app.route('/<int: contest_id>/add_player/result', methods= ['POST'])
def add_player(contest_id):
    player_name = request.form.get('name')
    if(add(contest_id, player_name) == -1):
        return render_template('incorrect_page.html')
    else:
        return render_template('added.html',id=contest_id, name=player_name)

@app.route('/<int: contest_id>/add_player', methods = ['GET'])
def show_form(contest_id):
    return render_template('form_for_adding.html', id=contest_id)


if __name__ == '__main__':
    app.run(debug=True)
