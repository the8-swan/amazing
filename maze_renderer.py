import mlx
from interface import font
from interface import buttons
from interface import colors
import random


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
        self.addr[index + 0] = color & 0xFF  # Blue
        self.addr[index + 1] = (color >> 8) & 0xFF  # Green
        self.addr[index + 2] = (color >> 16) & 0xFF  # Red
        if bytes_per_pixel == 4:
            self.addr[index + 3] = (
                (color >> 24) & 0xFF if (color >> 24) else 0xFF
            )  # Alpha


class MazeAnimation:
    def __init__(self, mlx, mlx_ptr, maze, image, img_maze_ptr, window, color):
        self.mlx = mlx
        self.mlx_ptr = mlx_ptr
        self.maze = maze
        self.image = image
        self.window = window
        self.img_maze_ptr = img_maze_ptr
        self.color = color
        self.currentx = 0
        self.currenty = 0
        self.is_animating = True


def clear_image(params):
    width = int((800 - (params.maze.width * params.maze.cell_size)) / 2)
    height = int((800 - (params.maze.height * params.maze.cell_size)) / 2)
    for i in range(height):
        for j in range(width):
            params.image.put_pixel_fast(j, i, colors[0]["background"])


def upade_image_maze(params):
    if params.is_animating is False:
        return 0
    clear_image(params)
    startx = int((800 - (params.maze.width * params.maze.cell_size)) / 2)
    starty = int((800 - (params.maze.height * params.maze.cell_size)) / 2)
    entryx, entryy = params.maze.entry
    exitx, exity = params.maze.exit

    for y in range(
        starty,
        (params.maze.height * params.maze.cell_size) + starty,
        params.maze.cell_size,
    ):
        yn = int((y - starty) / params.maze.cell_size)
        for x in range(0, params.currentx):
            if params.maze.cells[yn][x].walls["N"] is True:
                for i in range(
                    startx + (x * params.maze.cell_size),
                    startx + (x * params.maze.cell_size) + params.maze.cell_size,
                ):
                    for j in range(params.maze.wall_size):
                        params.image.put_pixel_fast(i, y + j, params.color)
    # # draw column
    for x in range(
        startx,
        (params.maze.width * params.maze.cell_size) + startx,
        params.maze.cell_size,
    ):
        xn = int((x - startx) / params.maze.cell_size)
        for y in range(0, params.currenty):
            if params.maze.cells[y][xn].walls["W"] is True:
                for i in range(
                    starty + (y * params.maze.cell_size),
                    (y * params.maze.cell_size) + starty + params.maze.cell_size,
                ):
                    for j in range(params.maze.wall_size):
                        params.image.put_pixel_fast(x + j, i, params.color)

    if params.currentx >= params.maze.width and params.currenty >= params.maze.height:
        for y in range(0, params.maze.height):
            if params.maze.cells[y][params.maze.width - 1].walls["E"] is True:
                for i in range(
                    starty + (y * params.maze.cell_size),
                    (y * params.maze.cell_size) + starty + params.maze.cell_size,
                ):
                    for j in range(params.maze.wall_size):
                        params.image.put_pixel_fast(
                            startx + (params.maze.width * params.maze.cell_size) + j,
                            i,
                            params.color,
                        )
        for x in range(0, params.maze.width):
            for i in range(
                startx + (x * params.maze.cell_size),
                startx + (x * params.maze.cell_size) + params.maze.cell_size,
            ):
                for j in range(params.maze.wall_size):
                    params.image.put_pixel_fast(
                        i,
                        starty + (params.maze.height * params.maze.cell_size) + j,
                        params.color,
                    )
        for eny in range(
            starty + (entryy * params.maze.cell_size),
            starty + ((entryy + 1) * params.maze.cell_size),
        ):
            for enx in range(
                startx + (entryx * params.maze.cell_size),
                startx + ((entryx + 1) * params.maze.cell_size),
            ):
                params.image.put_pixel_fast(enx, eny, colors[1]["entry"])
        for eny in range(
            starty + (exity * params.maze.cell_size),
            starty + ((exity + 1) * params.maze.cell_size),
        ):
            for enx in range(
                startx + (exitx * params.maze.cell_size),
                startx + ((exitx + 1) * params.maze.cell_size),
            ):
                params.image.put_pixel_fast(enx, eny, colors[5]["exit"])
        params.is_animating = False
    params.mlx.mlx_put_image_to_window(
        params.mlx_ptr, params.window, params.img_maze_ptr, 0, 0
    )
    params.currentx += 1
    params.currenty += 1


def buttons_section(mlx_p, mlx_ptr, image_btn, img_btn_ptr):
    start = 225
    texts = ["regenerate maze", "show or hide path", "change color"]

    def draw_text(text, button_top):
        text = text.upper()

        scale = 2
        thickness = 2
        letter_spacing = scale * 6

        text_width = len(text) * letter_spacing
        button_width = 260
        button_left = 70

        startx = button_left + (button_width - text_width) // 2
        starty = button_top + (70 - (5 * scale)) // 2

        for char in text:
            if char not in font:
                startx += letter_spacing
                continue

            l_font = font[char]

            for y in range(5):
                for x in range(5):
                    if l_font[y][x] == "X":
                        for dy in range(scale):
                            for dx in range(scale):
                                for t in range(thickness):
                                    image_btn.put_pixel_fast(
                                        startx + x * scale + dx + t,
                                        starty + y * scale + dy,
                                        0xFFFFFF,
                                    )

            startx += letter_spacing

    for text in texts:
        for y in range(start, start + 70):
            for x in range(70, 70 + 260):
                image_btn.put_pixel_fast(x, y, colors[2]["button_bg"])

        draw_text(text, start)
        start += 110

    mlx_p.mlx_put_image_to_window(mlx_ptr, mlx_ptr, img_btn_ptr, 800, 0)


def clicked_button(button: int, x: int, y: int, params: MazeAnimation):
    i = 0
    while i < 3:
        if x >= buttons[i]["start_x"] and x <= buttons[i]["end_x"]:
            if y >= buttons[i]["start_y"] and y <= buttons[i]["end_y"]:
                if buttons[i]["text"] == "regenerate maze":
                    params.image.set_color_to_image(800, 800, colors[0]["background"])
                    params.maze.reset_maze()
                    params.maze.my_42()
                    params.maze.dsf_algorith(0, 0)
                    params.currentx = 0
                    params.currenty = 0
                    params.is_animating = True
                    break
                elif buttons[i]["text"] == "change color":
                    params.image.set_color_to_image(800, 800, colors[0]["background"])
                    params.color = random.choice(colors[4]["wall_colors"])
                    params.currentx = 0
                    params.currenty = 0
                    params.is_animating = True
                    break

        i += 1


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

    image.set_color_to_image(800, 800, colors[0]["background"])
    image_btn.set_color_to_image(800, 400, colors[0]["background"])

    def destroy_win(param):
        mlx_p.mlx_destroy_window(mlx_ptr, window)
        mlx_p.mlx_loop_exit(mlx_ptr)

    params = MazeAnimation(
        mlx_p, mlx_ptr, maze, image, img_maze_ptr, window, colors[3]["base_wall_color"]
    )
    buttons_section(mlx_p, mlx_ptr, image_btn, img_btn_ptr)
    mlx_p.mlx_loop_hook(params.mlx_ptr, upade_image_maze, params)
    mlx_p.mlx_put_image_to_window(mlx_ptr, window, img_btn_ptr, 800, 0)
    mlx_p.mlx_mouse_hook(window, clicked_button, params)
    mlx_p.mlx_hook(window, 33, 0, destroy_win, None)
    mlx_p.mlx_loop(mlx_ptr)
