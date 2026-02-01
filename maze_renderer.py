import ctypes

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
		self.mlx.mlx_new_window.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
		self.mlx.mlx_new_window.restype = ctypes.c_void_p
		return self.mlx.mlx_new_window(self.mlx_ptr, size_x, size_y, title.encode())
	
	def create_image(self, width: int, height: int):
		self.mlx.mlx_new_image.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
		self.mlx.mlx_new_image.restype = ctypes.c_void_p
		return self.mlx.mlx_new_image(self.mlx_ptr, width, height)

	def loop(self):
		self.mlx.mlx_loop.argtypes = [ctypes.c_void_p]
		self.mlx.mlx_loop.restype = ctypes.c_int
		self.mlx.mlx_loop(self.mlx_ptr)

mlx = Minilibx("./libmlx.so")

# mlx.mlx_get_data_addr.argtypes = [ctypes.c_void_p,
# 									ctypes.POINTER(ctypes.c_int),
# 									ctypes.POINTER(ctypes.c_int),
# 									ctypes_POINTER(ctypes.c_int)]
# mlx.mlx_get_data_addr.restype = ctypes.c_char_p

window = mlx.create_window(800, 800, "hillow")
image = mlx.create_image(150,150)
#print(type(image))
mlx.loop()

