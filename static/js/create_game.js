socket.on("map_proposed", (data) => {
    const proposed_map = document.getElementById("create-game-map");
    proposed_map.innerHTML = "";
    const map_div = document.createElement("div");
    const tile_class = "tile";
    map_div.style.display = "flex";
    map_div.style.flexDirection = "column";
    map_div.style.alignItems = "center";
    map_div.style.justifyContent = "center";
    map_div.style.backgroundColor = 'white'

    const tile_size = tile_dimensions("tile")
    map_div.style.marginTop = - 2 * tile_size.marginTop + "px";
    map_div.style.marginBottom = - 2 * tile_size.marginBottom + "px";
    var tile_counter = 0;
    console.log(data)
    for (const terrain_row of data) {
        const row_div = document.createElement("div");
        row_div.style.display = "flex";
        for (const terrain of terrain_row) {
            const tile_div = document.createElement("div");
            tile_div.id = "proposed_tile_" + tile_counter;
            tile_counter++;
            tile_div.classList.add(tile_class);
            // Allow the tiles to be dragged
            tile_div.setAttribute("draggable", "true");
            // add the lower case terrain.name to the class list 
            tile_div.classList.add(terrain.toLowerCase());
            row_div.appendChild(tile_div);

            // Add event listener for dragstart to all .tile elements
            tile_div.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', tile_div.id);
            });

            // Add event listener for dragover to all .tile elements
            tile_div.addEventListener('dragover', (e) => {
                e.preventDefault();
            });

            // Add event listener for drop to all .tile elements
            tile_div.addEventListener('drop', (e) => {
                e.preventDefault();
                const from_tile_id = e.dataTransfer.getData('text/plain');
                const from_tile = document.getElementById(from_tile_id);
                const to_tile = e.target;
                // Cache the class list of the from tile
                from_classes = from_tile.className;
                from_tile.classList = to_tile.classList;
                to_tile.classList = from_classes;
            });

        }
        map_div.appendChild(row_div);
    }
    proposed_map.appendChild(map_div);
})


var create_game_status = "checking_map";
document.getElementById("create-game-accept-btn").addEventListener("click", () => {
    if (create_game_status == "checking_map") {
        create_game_status = "checking_counters"
        var current_map = document.getElementById("create-game-map");
        // Create a list of all the classes of the tiles (excluding "tile" class)
        var tile_classes = current_map.getElementsByClassName("tile");
        var tile_class_list = []
        for (var i = 0; i < tile_classes.length; i++) {
            tile_class_list.push(tile_classes[i].className);
            tile_class_list[i] = tile_class_list[i].replace("tile ", "");
        }
        socket.emit("accept_proposed_map", {map: tile_class_list});
    } else if (create_game_status == "checking_counters") {
        create_game_status = "accepting_map"
        var counters = null;
        socket.emit("accept_proposed_counters", {counters: counters });
    }
})

socket.on("counters_proposed", (counters) => {
    // Find all ".tile" elements and add a counter with the number from data.counters
    // If the tile is also a desert, do not add a counter
    const tile_class = "tile";
    const tile_class_dot = "." + tile_class;
    const tiles = document.querySelectorAll(tile_class_dot);
    // Counters is a list of lists, flatten this to make this loop easier
    counters = counters.flat();
    for (var i = 0; i < tiles.length; i++) {
        const tile = tiles[i];
        const counter_value = counters[i];
        if (counter_value == null) {
            continue
        }
        const counter = document.createElement("div");
        counter.classList.add("number-token");
        counter.classList.add("number-token-" + counter_value);
        tile.appendChild(counter);
    }
})