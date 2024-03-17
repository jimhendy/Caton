function tile_dimensions() {
    const tile_class = "tile";
    const tile_class_dot = "." + tile_class;
    
    let width = $(tile_class_dot).width();
    let tile = null

    if (width === undefined) {
        tile = document.createElement('div');
        tile.classList.add(tile_class);
        document.body.appendChild(tile);
        width = $(tile_class_dot).width();
    }

    height = $(tile_class_dot).height();
    // Extract the margin values (t,l,r,b) as floating point numbers
    marginTop = parseFloat($(tile_class_dot).css('margin-top'));
    marginBottom = parseFloat($(tile_class_dot).css('margin-bottom'));
    marginRight = parseFloat($(tile_class_dot).css('margin-right'));
    marginLeft = parseFloat($(tile_class_dot).css('margin-left'));

    if (tile){
       document.body.removeChild(tile);
    }

    return {
        width: width,
        height: height,
        marginTop: marginTop,
        marginBottom: marginBottom,
        marginRight: marginRight,
        marginLeft: marginLeft
    }
}