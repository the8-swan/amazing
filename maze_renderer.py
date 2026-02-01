import ctypes
import struct


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


mlx = Minilibx("./libmlx.so")
window = mlx.create_window(800, 800, "hillow")
img_ptr = mlx.create_image(150, 150)
image_addr = mlx.get_image_data(img_ptr)
image_addr.put_pixel_fast(100, 100, 0xFF0000)
mlx.put_image_to_window(window, img_ptr, 50, 50)
# print(image_addr)
# print(type(image))
mlx.loop()
