import ctypes
import struct
from math import sqrt

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
	
	def loop_hook(self, function):
		FUNCTION = ctypes.CFUNCTYPE(ctypes.c_int)
		a_function = FUNCTION(function)
		self.mlx.mlx_loop_hook=[
			ctypes.c_void_p,
			FUNCTION,
			ctypes.c_void_p,
		]
		self.mlx.mlx_loop_hook = ctypes.c_int
		self.mlx.mlx_loop_hook(self.mlx_ptr, a_function, None)

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

def drawing_image(position:tuple):
	x,y = tuple
		for _ in range(x):
			 image_addr.put_pixel_fast(x, y, 0xFFFFFF)

def animation():
	mlx = Minilibx("./libmlx.so")
	window = mlx.create_window(1000, 1000, "animation")
	image = mlx.create_image(1000, 1000)
	image_addr = mlx.get_image_data(image)
	position = (0,0)
	image_width = (1000,1000)

	#image_addr.set_color_to_image(1000, 1000, 0xFFFFFF)



	mlx.put_image_to_window(window, image , 10, 10)
	mlx.loop()

animation()