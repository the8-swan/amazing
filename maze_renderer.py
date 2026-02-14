import mlx

class img_data:
    def __init__(self, addr, bits_per_pixel, size_line, endian):
        self.addr = addr
        self.bits_per_pixel = bits_per_pixel
        self.size_line = size_line
        self.endian = endian

 
    def set_color_to_image(self, height, width, color: int):
        """Fill entire image with a solid color."""
        for y in range(height):
            for x in range(width):
                self.put_pixel_fast(x, y, color)

    def put_pixel_fast(self, x: int, y: int, color: int):
        """Set a single pixel color."""
        bytes_per_pixel = self.bits_per_pixel // 8
        
        # Calculate byte offset in flat array
        # size_line is bytes per row (may include padding)
        row_offset = y * self.size_line
        pixel_offset = x * bytes_per_pixel
        index = row_offset + pixel_offset
        
        # Assign color components (BGRA format)
        self.addr[index + 0] = color & 0xFF           # Blue
        self.addr[index + 1] = (color >> 8) & 0xFF    # Green
        self.addr[index + 2] = (color >> 16) & 0xFF   # Red
        if bytes_per_pixel == 4:
            self.addr[index + 3] = (color >> 24) & 0xFF if (color >> 24) else 0xFF  # Alpha


def maze_draw(maze):
    mlx_p = mlx.Mlx()
    mlx_ptr = mlx_p.mlx_init()
    window = mlx_p.mlx_new_window(mlx_ptr, 1200, 800, "MAZE")
    
    img_maze_ptr = mlx_p.mlx_new_image(mlx_ptr, 800, 800)
    img_btn_ptr = mlx_p.mlx_new_image(mlx_ptr, 400, 800)

    addr, bpp, size_line, endian = mlx_p.mlx_get_data_addr(img_maze_ptr)
    addr_btn, bpp_btn, size_line_btn, endian_btn = mlx_p.mlx_get_data_addr(img_btn_ptr)
    
    image = img_data(addr, bpp, size_line, endian)
    image_btn = img_data(addr_btn, bpp_btn, size_line_btn, endian_btn)

    image.set_color_to_image(800, 800, 0x000000)
    image_btn.set_color_to_image(800, 400, 0xFFFFFF)

    color = 0xFFFF00
    # draw rows
    for y in range(0, maze.height * maze.cell_size, maze.cell_size):
        yn = int(y / maze.cell_size)
        for x in range(0, maze.width):
            if maze.cells[yn][x].walls["N"] is True:
                for i in range(
                    x * maze.cell_size, (x * maze.cell_size) + maze.cell_size
                ):
                    for j in range(2):
                        image.put_pixel_fast(i, y + j, color)
    for x in range(0, maze.width):

            for i in range(x * maze.cell_size, (x * maze.cell_size) + maze.cell_size):
                for j in range(2):
                    image.put_pixel_fast(
                        i, (maze.height * maze.cell_size) + j, color
                    )
    # draw column
    for x in range(0, maze.width * maze.cell_size, maze.cell_size):
        xn = int(x / maze.cell_size)
        for y in range(0, maze.height):
            if maze.cells[y][xn].walls["W"] is True:
                for i in range(
                    y * maze.cell_size, (y * maze.cell_size) + maze.cell_size
                ):
                    for j in range(2):
                        image.put_pixel_fast(x + j, i, color)
    for y in range(0, maze.height):
        if maze.cells[y][maze.width - 1].walls["E"] is True:
            for i in range(y * maze.cell_size, (y * maze.cell_size) + maze.cell_size):
                for j in range(2):
                    image.put_pixel_fast(
                        (maze.width * maze.cell_size) + j, i, color
                    )
    def destroy_win(param):
        mlx_p.mlx_destroy_window(mlx_ptr, window)
        mlx_p.mlx_loop_exit(mlx_ptr)
    
    startx = int((800 - (maze.width * maze.cell_size)) / 2)
    starty = int((800 - (maze.height * maze.cell_size)) / 2)
    mlx_p.mlx_put_image_to_window(mlx_ptr, window, img_maze_ptr, startx, starty)
    mlx_p.mlx_put_image_to_window(mlx_ptr, window, img_btn_ptr, 800, 0)
    mlx_p.mlx_hook(window, 33, 0, destroy_win, None)
    mlx_p.mlx_loop(mlx_ptr)