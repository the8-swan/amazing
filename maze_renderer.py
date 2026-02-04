import ctypes
import struct
from math import sqrt

"""
# C Type          →  Python ctypes
# -----------------------------------
# void*           →  ctypes.c_void_p
# int             →  ctypes.c_int
# char*           →  ctypes.c_char_p
# unsigned int    →  ctypes.c_uint
name_of_the_function.argtypes = [] -------
return value name_of_the_function.restype = return
"""


class Minilibx:
    def __init__(self, lib_url):
        self.mlx = ctypes.CDLL(lib_url)
        self.mlx_ptr = self.initalize()
        self._callbacks = []

    def initalize(self):
        self.mlx.mlx_init.restype = ctypes.c_void_p
        return self.mlx.mlx_init()

    def create_window(self, size_x: int, size_y: int, title: str):
        self.mlx.mlx_new_window.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_char_p,
        ]
        self.mlx.mlx_new_window.restype = ctypes.c_void_p
        return self.mlx.mlx_new_window(self.mlx_ptr, size_x, size_y, title.encode())

    def destroy_window(self, window):
        self.mlx.mlx_destroy_window.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        self.mlx.mlx_destroy_window.restype = ctypes.c_int
        self.mlx.mlx_destroy_window(self.mlx_ptr, window)

    def create_image(self, width: int, height: int):
        self.mlx.mlx_new_image.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]

        self.mlx.mlx_new_image.restype = ctypes.c_void_p
        return self.mlx.mlx_new_image(self.mlx_ptr, width, height)

    def mlx_hook(self, window, event: int, callback):
        CALLBACK = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)
        c_callback = CALLBACK(callback)
        self.mlx.mlx_hook.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int,
            CALLBACK,
            ctypes.c_void_p,
        ]
        self.mlx.mlx_hook.restype = ctypes.c_int
        self._callbacks.append(c_callback)
        self.mlx.mlx_hook(window, event, 0, c_callback, None)

    def get_image_data(self, image_ptr):
        self.mlx.mlx_get_data_addr.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int),
        ]
        self.mlx.mlx_get_data_addr.restype = ctypes.POINTER(ctypes.c_char)

        bits_per_pixel = ctypes.c_int()
        size_line = ctypes.c_int()
        endian = ctypes.c_int()
        adr = self.mlx.mlx_get_data_addr(
            image_ptr,
            ctypes.byref(bits_per_pixel),
            ctypes.byref(size_line),
            ctypes.byref(endian),
        )

        return self.img_data(adr, bits_per_pixel.value, size_line.value, endian.value)

    def put_image_to_window(self, win_ptr, image_ptr, x: int, y: int):
        self.mlx.mlx_put_image_to_window.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int,
        ]
        self.mlx.mlx_put_image_to_window.restype = ctypes.c_int
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, win_ptr, image_ptr, x, y)

    def load_file_to_image(self, imageName: str):
        self.mlx.mlx_xpm_file_to_image.argtypes=[
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int)
        ]
        self.mlx.mlx_xpm_file_to_image.restype = ctypes.c_void_p
        width = ctypes.c_int()
        height = ctypes.c_int()
        imageName_bytes = imageName.encode("utf-8")
        img_ptr = self.mlx.mlx_xpm_file_to_image(
            self.mlx_ptr, imageName_bytes, ctypes.byref(width), ctypes.byref(height)
        )
        return img_ptr, width.value, height.value

    def loop(self):
        self.mlx.mlx_loop.argtypes = [ctypes.c_void_p]
        self.mlx.mlx_loop.restype = ctypes.c_int
        self.mlx.mlx_loop(self.mlx_ptr)

    class img_data:
        def __init__(self, addr, bits_per_pixel, size_line, endian):
            self.addr = addr
            self.bits_per_pixel = bits_per_pixel
            self.size_line = size_line
            self.endian = endian

        def set_color_to_image(self, rows, colums, color: int):
            for i in range(colums):
                for j in range(rows):
                    self.put_pixel_fast(j, i, color)

        def put_pixel_fast(self, x: int, y: int, color: int):
            bytes_per_pixel = self.bits_per_pixel // 8
            pixel_index = y * self.size_line + x * bytes_per_pixel
            self.addr[pixel_index + 0] = color & 0xFF  # Blue
            self.addr[pixel_index + 1] = (color >> 8) & 0xFF  # Green
            self.addr[pixel_index + 2] = (color >> 16) & 0xFF  # Red
            self.addr[pixel_index + 3] = (color >> 24) & 0xFF  # Alpha


def maze_draw(maze):
    win_x_dimention = 1000
    win_y_dimention = 1000

    def on_destroy(param):
        mlx.destroy_window(window)
        exit(0)
        return 0

    mlx = Minilibx("./libmlx.so")
    window = mlx.create_window(win_x_dimention, win_y_dimention, "hillow")
    mlx.mlx_hook(window, 17, on_destroy)

    imagex = maze.width * maze.cell_size
    imagey = maze.height * maze.cell_size
    img_ptr = mlx.create_image(imagex, imagey)
    image_addr = mlx.get_image_data(img_ptr)
    image_addr.set_color_to_image(imagex, imagey, 0x000000)

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
                        image_addr.put_pixel_fast(i, y + j, color)
    for x in range(0, maze.width):
        if maze.cells[maze.height- 1][x].walls["S"] is True:
            print(f"{maze.cells[maze.height- 1][x]}")
            for i in range(x * maze.cell_size, (x * maze.cell_size) + maze.cell_size):
                for j in range(2):
                    image_addr.put_pixel_fast(
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
                        image_addr.put_pixel_fast(x + j, i, color)
    for y in range(0, maze.height):
        if maze.cells[y][maze.width - 1].walls["E"] is True:
            for i in range(y * maze.cell_size, (y * maze.cell_size) + maze.cell_size):
                for j in range(2):
                    image_addr.put_pixel_fast(
                        (maze.width * maze.cell_size) + j, i, color
                    )
    startx = int((win_x_dimention - (imagex)) / 2)
    starty = int((win_x_dimention - (imagey)) / 2)
    mlx.put_image_to_window(window, img_ptr, startx, starty)
    mouse_img, w, h = mlx.load_file_to_image("mouse.xpm")
    cheese_img, w2, h2 = mlx.load_file_to_image("cheese.xpm")
    mlx.put_image_to_window(window, mouse_img, (maze.entry[0] * maze.cell_size)+( maze.cell_size+2), (maze.entry[1]*maze.cell_size)+( maze.cell_size+2))
    mlx.put_image_to_window(window, cheese_img, (maze.exit[0] * maze.cell_size)+( maze.cell_size+2), (maze.exit[1] * maze.cell_size)+( maze.cell_size+2))


    mlx.loop()
