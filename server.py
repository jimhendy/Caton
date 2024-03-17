import uuid
from dataclasses import dataclass, field

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from loguru import logger

from caton import generate_random_number_tokens, generate_random_terrains

players = {}
games = {}


@dataclass
class Player:
    id: str  # request.sid
    name: str


@dataclass
class Game:
    id: str  # uuid
    host: Player
    name: str = field(default="")
    players: list[Player] = field(init=False, default_factory=list)

    def __post_init__(self):
        logger.debug(f"Creating game {self.id} with host {self.host.name}")
        self.add_player(self.host)
        if not self.name:
            self.name = f"{self.host.name}'s Game"

    def add_player(self, player: Player):
        logger.info(f"Adding player {player.name} to game {self.id}")
        self.players.append(player)
        join_room(self.id, sid=player.id)

    def remove_player(self, player: Player):
        self.players.remove(player)
        leave_room(self.id, sid=player.id)


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store game state (in memory, replace with DB for production)
games = {}


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("sign_in")
def handle_sign_in(data):
    player = Player(id=request.sid, name=data["player_name"])
    logger.info(f"Player {player.name} signed in (sid: {player.id})")
    players[player.id] = player
    emit("signed_in", {"is_logged_in": True}, to=player.id)


@socketio.on("sign_out")
def handle_sign_out():
    player = players.pop(request.sid)
    logger.info(f"Player {player.name} signed out (sid: {player.id})")
    # Remove any games the player is hosting
    games_to_remove = []
    for game in games.values():
        if game.host.id == player.id:
            games_to_remove.append(game)
    for game in games_to_remove:
        game = games.pop(game.id)
        emit("game_killed", to=game.host.id)
    list_games()
    emit("signed_in", {"is_logged_in": False}, to=player.id)


@socketio.on("create_game")
def handle_create_game():
    game_id = uuid.uuid4().hex
    games[game_id] = Game(id=game_id, host=players[request.sid])
    list_games()


@socketio.on("join_game")
def handle_join_game(data):
    game_id = data["game_id"]
    player = players[request.sid]
    if not (game := games.get(game_id)):
        logger.error(f"Player {player.name} tried to join non-existent game {game_id}")
        return

    game.add_player(player)
    emit("game_joined", {"game_id": game_id}, to=game.id)


@socketio.on("list_games")
def handle_list_games():
    list_games()


def list_games():
    emit(
        "games_listed",
        {"games": [{"name": game.name, "id": game.id} for game in games.values()]},
        broadcast=True,
    )


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("propose_map")
def handle_propose_map():
    board = generate_random_terrains(serialised=True)
    emit("map_proposed", board)


@socketio.on("accept_proposed_map")
def handle_accept_map(board):
    print(board)
    counters = generate_random_number_tokens()
    emit("counters_proposed", counters)


if __name__ == "__main__":
    socketio.run(app)
