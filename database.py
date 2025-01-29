import sqlite3
from threading import Lock
import logging
from logger import Logger
logger=Logger()


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
                logger.info("Initializing database connection")
                self.conn = sqlite3.connect(db_path, check_same_thread=False)
                self.cursor = self.conn.cursor()
                self._create_test()
                self._initialized = True

    def _create_test(self):
        logger.info("Creating tables if they do not exist")
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                                id INTEGER PRIMARY KEY, 
                                name TEXT NOT NULL, 
                                status TEXT NOT NULL, 
                                contest_id INTEGER NOT NULL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS games (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                game_number INTEGER NOT NULL,
                                score_1 INTEGER, 
                                score_2 INTEGER, 
                                pl_1_id INTEGER, 
                                pl_2_id INTEGER, 
                                contest_id INTEGER NOT NULL, 
                                FOREIGN KEY (pl_1_id) REFERENCES players(id), 
                                FOREIGN KEY (pl_2_id) REFERENCES players(id))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS knockout_status (
                                contest_id INTEGER NOT NULL,
                                knockout_status INTEGER)''')
        self.conn.commit()
        logger.info("Tables successfully created or verified")
    def new_game_ref_by_id(self,contest_id,id1_val,id2_val):
        self.cursor.execute('SELECT COALESCE(MAX(game_number), 0) + 1 FROM games WHERE contest_id = ?', (contest_id,))
        game_number = self.cursor.fetchone()[0]

        self.cursor.execute(
            'INSERT INTO games (game_number, score_1, score_2, pl_1_id, pl_2_id, contest_id) VALUES (?, 0, 0, ?, ?, ?)',
            (game_number, id1_val, id2_val, contest_id))
        try:
            self.conn.commit()
            logger.info(f"Game {game_number} successfully created in contest {contest_id}")
            return game_number
        except Exception as e:
            logger.error(f"Failed to create game: {e}")
            return -1
    def new_game(self, contest_id, first_pl, second_pl):
        logger.info(f"Creating new game in contest {contest_id} between {first_pl} and {second_pl}")

        self.cursor.execute('SELECT id FROM players WHERE name = ? AND contest_id = ?', (first_pl, contest_id))
        id1 = self.cursor.fetchone()
        if not id1:
            logger.error(f"First player '{first_pl}' not found in contest {contest_id}")
            return -1

        self.cursor.execute('SELECT id FROM players WHERE name = ? AND contest_id = ?', (second_pl, contest_id))
        id2 = self.cursor.fetchone()
        if not id2:
            logger.error(f"Second player '{second_pl}' not found in contest {contest_id}")
            return -1

        id1_val, id2_val = id1[0], id2[0]
        self.new_game_ref_by_id(contest_id,id1_val, id2_val)


    def new_player(self, contest_id, name):
        logger.info(f"Adding new player '{name}' to contest {contest_id}")
        self.cursor.execute('INSERT INTO players (name, status, contest_id) VALUES (?, "live", ?)', (name, contest_id))
        self.conn.commit()
        logger.info(f"Player '{name}' successfully added to contest {contest_id}")

    def all_games(self, contest_id):
        logger.info(f"Fetching all games for contest {contest_id}")
        self.cursor.execute('SELECT game_number FROM games WHERE contest_id = ?', (contest_id,))
        games = self.cursor.fetchall()
        return [self.one_game(contest_id, game[0]) for game in games]

    def one_game(self, contest_id, game_number):
        logger.info(f"Fetching game {game_number} from contest {contest_id}")
        self.cursor.execute('SELECT * FROM games WHERE game_number = ? AND contest_id = ?', (game_number, contest_id))
        game = self.cursor.fetchone()
        if not game:
            logger.warning(f"Game {game_number} not found in contest {contest_id}")
            return None

        return {
            'game_number': game[1],
            'first_sc': game[2],
            'second_sc': game[3],
            'first_pl': self.get_player_name(game[4]),
            'second_pl': self.get_player_name(game[5])
        }

    def change_game(self, contest_id, game_id, sc_1, sc_2):
        logger.info(f"Updating game {game_id} in contest {contest_id} with scores {sc_1}-{sc_2}")

        self.cursor.execute('UPDATE games SET score_1 = ?, score_2 = ? WHERE game_number = ? AND contest_id = ?',
                            (sc_1, sc_2, game_id, contest_id))
        self.conn.commit()

        logger.info(f"Game {game_id} successfully updated in contest {contest_id}")

        self.cursor.execute('SELECT id, game_number, score_1, score_2, pl_1_id, pl_2_id FROM games WHERE contest_id = ?',
                            (contest_id,))
        games = self.cursor.fetchall()
        cnt = 0
        for game in games:
            cnt = max(cnt,game[1])

        l=1
        r = self.player_cnt(contest_id)//2
        diff = r
        while r < cnt:
            l = r+1
            diff = diff//2
            r += diff
        logger.info(f"Looking for games in [{l},{r}]")
        if any(game[2] == game[3] for game in games[(l-1):r]):
            logger.info("Not all games have a winner yet, skipping next round creation.")
            return

        logger.info("All games have a winner, proceeding to next round.")

        winners = []
        for game in games[(l-1):r]:
            winner_id = game[4] if game[2] > game[3] else game[5]
            winners.append(winner_id)

        if len(winners) <= 1:
            logger.info("Tournament completed, final winner determined.")
            return

        for i in range(0, len(winners), 2):
            if i + 1 < len(winners):
                cnt+=1
                self.cursor.execute(
                    'INSERT INTO games (game_number, score_1, score_2, pl_1_id, pl_2_id, contest_id) VALUES (?, 0, 0, ?, ?, ?)',
                    (cnt, winners[i], winners[i + 1], contest_id))

        self.conn.commit()
        logger.info("Next round games created successfully.")

    def get_player_name(self, player_id):
        self.cursor.execute('SELECT name FROM players WHERE id = ?', (player_id,))
        return self.cursor.fetchone()[0]

    def player_cnt(self, contest_id):
        logger.info(f"Fetching player count from contest {contest_id}")
        self.cursor.execute('SELECT COUNT(*) FROM players WHERE contest_id = ?', (contest_id,))
        return self.cursor.fetchone()[0]

    def start_knockout(self, contest_id):
        logger.info(f"Starting knockout in contest {contest_id}")
        self.cursor.execute('UPDATE knockout_status SET knockout_status = 1 WHERE contest_id = ?', (contest_id,))

        self.cursor.execute('SELECT id FROM players WHERE contest_id = ?', (contest_id,))
        players = [row[0] for row in self.cursor.fetchall()]

        for i in range(0, len(players), 2):
            if i + 1 < len(players):
                self.new_game_ref_by_id(contest_id, players[i], players[i + 1])

        self.conn.commit()
        logger.info("First round games created successfully.")


def get_all_games(contest_id):
    d = Database(f'release.db')
    return d.all_games(contest_id)


def get_one_game(contest_id, game_id):
    d = Database(f'release.db')
    return d.one_game(contest_id, game_id)


def change_game(contest_id, game_id, live_status, sc_1, sc_2):
    d = Database(f'release.db')
    return d.change_game(contest_id, game_id, sc_1, sc_2)


def add_one_game(contest_id, p1, p2):
    d = Database(f'release.db')
    return d.new_game(contest_id, p1, p2)


def add_one_player(contest_id, p):
    logger.info(f'contest_id = {contest_id}')
    d = Database(f'release.db')
    return d.new_player(contest_id, p)

def player_count(contest_id):
    d = Database(f'release.db')
    return d.player_cnt(contest_id)

def start_knockout(contest_id):
    d = Database(f'release.db')
    d.start_knockout(contest_id)

