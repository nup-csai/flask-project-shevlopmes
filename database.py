import sqlite3
from threading import Lock
from logger import Logger
logger = Logger()
import flask_sqlalchemy
class Database:
    _instance = None
    _lock = Lock()
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_path=":memory:"):
        with self._lock:
            if not self._initialized:
                self.conn = sqlite3.connect(db_path, check_same_thread=False)
                self.cursor = self.conn.cursor()
                self._create_test()
                self.cursor.execute('SELECT COUNT(*) FROM games')
                self.game_count = self.cursor.fetchone()[0]

                self.cursor.execute('SELECT COUNT(*) FROM players')
                self.player_count = self.cursor.fetchone()[0]

                self._initialized = True
    def _create_test(self):
        self.cursor.execute('create table if not exists players (id int primary key, name text not null, status text not null)')
        self.cursor.execute('create table if not exists games (id int primary key, score_1 int, score_2 int, pl_1_id int, pl_2_id int, foreign key (pl_1_id) references players(id), foreign key (pl_2_id) references players(id))')
        self.conn.commit()

    def new_game(self, first_pl, second_pl):
        logger.info(first_pl)
        logger.info(second_pl)
        self.cursor.execute('select a.id from players a where a.name = ?', (first_pl,))
        id1 = self.cursor.fetchall()
        if not id1:
            logger.error('first player has unknown name')
            return -1
        self.cursor.execute('select a.id from players a where a.name = ?', (second_pl,))
        id2 = self.cursor.fetchall()
        if not id2:
            logger.error('second player has unknown name')
            return -1
        id1_val = id1[0][0]
        id2_val = id2[0][0]
        logger.info(f'id1 is {id1}\n id1[0] is {id1[0]}\n id1[0][0] is {id1[0][0]}')
        logger.info(f'id2 is {id2}\n id2[0] is {id2[0]}\n id2[0][0] is {id2[0][0]}')
        logger.info(f'trying to pass {id1_val,id2_val,self.game_count}')


        self.cursor.execute('insert into games (id, score_1, score_2, pl_1_id, pl_2_id) values (?,0,0,?,?)',(self.game_count,id1_val,id2_val))
        try:
            self.conn.commit()
            self.game_count += 1
            return self.game_count
        except Exception:
            return -1

    def new_player(self,name):
        logger.info(f'try to add into players id = {self.player_count}, name = {name}')
        self.cursor.execute('insert into players (id, name, status) values (?,?,"live")',(self.player_count,name))
        self.player_count+=1
        self.conn.commit()

    def one_game(self, game_id):
        if game_id < 0 or game_id >= self.game_count:
            return None
        a = {}
        logger.info(f'game_id = {game_id}')
        self.cursor.execute('select * from games a where a.id = ?',(game_id,))
        self.conn.commit()
        tmp = self.cursor.fetchall()
        logger.info(f'tmp = {tmp}')
        a['first_sc'] = tmp[0][1]
        a['second_sc'] = tmp[0][2]
        a['live'] = 0
        id1 = tmp[0][3]
        id2 = tmp[0][4]
        self.cursor.execute('select a.name from players a where a.id = ?',(id1,))
        self.conn.commit()
        a['first_pl'] = self.cursor.fetchall()
        self.cursor.execute('select a.name from players a where a.id = ?', (id2,))
        self.conn.commit()
        a['second_pl'] = self.cursor.fetchall()
        a['first_pl'] = a['first_pl'][0][0]
        a['second_pl'] = a['second_pl'][0][0]
        return a
    def change_game (self, game_id, live_status, sc_1, sc_2):
        self.cursor.execute('update games set score_1 = ?, score_2 = ? where id = ?',(sc_1,sc_2,game_id))
        self.conn.commit()
    def all_games(self):
        output = []
        for i in range(self.game_count):
            output.append(self.one_game(i))
        return output


def get_all_games(contest_id):
    d = Database(f'{contest_id}.db')
    return d.all_games()
def get_one_game(contest_id, game_id):
    d = Database(f'{contest_id}.db')
    return d.one_game(game_id)

def change_game(contest_id,game_id,live_status,sc_1,sc_2):
    d = Database(f'{contest_id}.db')
    return d.change_game(game_id,live_status,sc_1, sc_2)
def add_one_game(contest_id,p1,p2):
    d = Database(f'{contest_id}.db')
    return d.new_game(p1,p2)

def add_one_player(contest_id,p):
    logger = Logger()
    logger.info(f'contest_id = {contest_id}')
    d = Database(f'{contest_id}.db')
    logger.info(str(d.player_count))
    return d.new_player(p)





