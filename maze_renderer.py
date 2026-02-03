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

    def initalize(self):
        self.mlx.mlx_init.restype = ctypes.c_void_p
        return self.mlx.mlx_init()

    def create_window(self, size_x: int, size_y: int, title: str):
        self.mlx.mlx_new_window.argtypes = [ctypes.c_void_p,
                                            ctypes.c_int,
                                            ctypes.c_int,
                                            ctypes.c_char_p]
        self.mlx.mlx_new_window.restype = ctypes.c_void_p
        return self.mlx.mlx_new_window(self.mlx_ptr,
                                       size_x,
                                       size_y,
                                       title.encode())

    def create_image(self, width: int, height: int):
        self.mlx.mlx_new_image.argtypes = [ctypes.c_void_p,
                                           ctypes.c_int,
                                           ctypes.c_int]

        self.mlx.mlx_new_image.restype = ctypes.c_void_p
        return self.mlx.mlx_new_image(self.mlx_ptr, width, height)

    def get_image_data(self, image_ptr):
        self.mlx.mlx_get_data_addr.argtypes = [ctypes.c_void_p,
                                          ctypes.POINTER(ctypes.c_int),
                                          ctypes.POINTER(ctypes.c_int),
                                          ctypes.POINTER(ctypes.c_int)]
        self.mlx.mlx_get_data_addr.restype = ctypes.POINTER(ctypes.c_char)

        bits_per_pixel = ctypes.c_int()
        size_line = ctypes.c_int()
        endian = ctypes.c_int()
        adr = self.mlx.mlx_get_data_addr(
            image_ptr,
            ctypes.byref(bits_per_pixel),
            ctypes.byref(size_line),
            ctypes.byref(endian))

        return self.img_data(adr,
                             bits_per_pixel.value,
                             size_line.value,
                             endian.value)

    def put_image_to_window(self, win_ptr, image_ptr, x: int, y: int):
        self.mlx.mlx_put_image_to_window.argtypes = [ctypes.c_void_p,
                                                     ctypes.c_void_p,
                                                     ctypes.c_void_p,
                                                     ctypes.c_int,
                                                     ctypes.c_int]
        self.mlx.mlx_put_image_to_window .restype = ctypes.c_int
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, win_ptr, image_ptr, x, y)
         
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

        def put_pixel_fast(self, x: int, y: int, color: int):
            bytes_per_pixel = self.bits_per_pixel // 8
            pixel_index = y * self.size_line + x * bytes_per_pixel
            self.addr[pixel_index + 0] = color & 0xFF           # Blue
            self.addr[pixel_index + 1] = (color >> 8) & 0xFF    # Green
            self.addr[pixel_index + 2] = (color >> 16) & 0xFF   # Red
            self.addr[pixel_index + 3] = (color >> 24) & 0xFF   # Alpha


def maze_draw(data):
    win_x_dimention = 800
    win_y_dimention = 800
    cell_size_p = 30

    mlx = Minilibx("./libmlx.so")
    window = mlx.create_window(win_x_dimention, win_y_dimention, "hillow")
    img_ptr = mlx.create_image(win_x_dimention, win_y_dimention)
    image_addr = mlx.get_image_data(img_ptr)

    startx = int(( win_x_dimention - (data['WIDTH'] * cell_size_p)) / 2)
    starty = int(( win_y_dimention - (data['HEIGHT'] * cell_size_p)) / 2)

    endx = int(startx + 1 + (data['WIDTH'] * cell_size_p))
    endy = int(starty + 1 + (data['HEIGHT'] * cell_size_p))
    color = 0xFFFFFF
    for y in range(starty, endy, cell_size_p):
        for x in range(startx, endx):
            image_addr.put_pixel_fast(x, y, color)

    for x in range(startx, endx, cell_size_p):
        for y in range(starty, endy):
            image_addr.put_pixel_fast(x, y, color)
    mlx.put_image_to_window(window, img_ptr, 0, 0)
    mlx.loop()
# print(image_addr)
# print(type(image))

