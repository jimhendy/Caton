
function signIn() {
    const username = document.getElementById('catan-game-username').value;
    console.log('User signed in as', username);
    socket.emit('sign_in', { 'player_name': username });
}

function signOut() {
    console.log('User signed out');
    socket.emit('sign_out');
}

function createGame() {
    console.log("Creating game");
    document.getElementById('create-game-screen').style.display = 'block';
    document.getElementById('login-screen').style.display = 'none';
    socket.emit('propose_map');
}

// Disable the sign in button until something is entered in the username input
function disableSignInButton() {
    const signInButton = document.getElementById('sign-in-btn');
    // Ensure the catan-game-username input has non-space text in it
    signInButton.disabled = document.getElementById('catan-game-username').value.trim() === '';
}

function backToLogin() {
    document.getElementById('create-game-screen').style.display = 'none';
    document.getElementById('login-screen').style.display = 'block';
}



function joinGame() {
    const game_id = document.getElementById('game_id_to_join').value;
    console.log("Joining game", game_id);
    socket.emit('join_game', { game_id });
}

socket.on('games_listed', (data) => {
    const gamesList = document.getElementById('games');
    gamesList.innerHTML = ''; // Clear existing list

    data.games.forEach(game => {
        const li = document.createElement('li');
        li.textContent = `Game ID: ${game.name}`;
        gamesList.appendChild(li);
    });

    if (data.games.length === 0) {
        const li = document.createElement('li');
        li.textContent = 'No games available';
        gamesList.appendChild(li);
    }
});

// Create a listener on the socker for the logged-in event to enable the create game button
socket.on('signed_in', (data) => {
    document.getElementById('create-btn').disabled = data.is_logged_in === false;
    document.getElementById('sign-in-btn').disabled = data.is_logged_in === true;
    document.getElementById('sign-out-btn').disabled = data.is_logged_in === false;
    document.getElementById('create-game').style.display = data.is_logged_in === true ? 'block' : 'none';
    document.getElementById('game-list').style.display = data.is_logged_in === true ? 'block' : 'none';
});

// Ask the server for a list of available games for the initial list
socket.emit('list_games');

// Create a canvas element behind all above element, spanning the whole body
const canvas = document.createElement('div');
canvas.className = 'background-canvas';

// Add the canvas to the body
document.body.appendChild(canvas);

// Entirely tile the canvas with tile class divs
var tiles = null;
function tile_background() {
    // Clear all children from the canvas
    canvas.innerHTML = '';

    var window_height = window.innerHeight;
    var window_width = window.innerWidth;
    
    const tile_size = tile_dimensions();
    var current_height = - tile_size.height / 2;
    var row_num = 0

    while (current_height < window_height + tile_size.height) {
        var current_width = - tile_size.width / 2;
        if (row_num % 2 == 1) {
            current_width += tile_size.width / 2
        }
        while (current_width < window_width + tile_size.width) {
            const tile = document.createElement('div');
            tile.className = 'outline-tile';
            tile.classList.add('canvas-tile');
            tile.style.position = 'absolute';
            tile.style.left = current_width + 'px';
            tile.style.top = current_height + 'px';
            canvas.appendChild(tile);
            current_width += tile_size.width;
        }
        current_height += tile_size.height + tile_size.marginTop + tile_size.marginBottom;
        row_num += 1
    }
    tiles = document.querySelectorAll('.canvas-tile');
}

window.onresize = tile_background;
tile_background();

// Each 100 milliseconds, pick a random tile from the background canvas
// and transition it's background colour to a random color and back to white
setInterval(() => {
    const tile = tiles[Math.floor(Math.random() * tiles.length)];
    const newColor = `rgb(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)})`;
    tile.style.backgroundColor = newColor;
    setTimeout(() => {
        tile.style.backgroundColor = "white";
    }, 7000);
}, 1000);
