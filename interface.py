font = {
    "A": ["  X  ", " X X ", "XXXXX", "X   X", "X   X"],
    "B": ["XXXX ", "X   X", "XXXX ", "X   X", "XXXX "],
    "C": [" XXX ", "X   X", "X    ", "X   X", " XXX "],
    "D": ["XXXX ", "X   X", "X   X", "X   X", "XXXX "],
    "E": ["XXXXX", "X    ", "XXXX ", "X    ", "XXXXX"],
    "F": ["XXXXX", "X    ", "XXXX ", "X    ", "X    "],
    "G": [" XXX ", "X    ", "X XXX", "X   X", " XXX "],
    "H": ["X   X", "X   X", "XXXXX", "X   X", "X   X"],
    "I": [" XXX ", "  X  ", "  X  ", "  X  ", " XXX "],
    "J": ["  XXX", "   X ", "   X ", "X  X ", " XX  "],
    "K": ["X   X", "X  X ", "XXX  ", "X  X ", "X   X"],
    "L": ["X    ", "X    ", "X    ", "X    ", "XXXXX"],
    "M": ["X   X", "XX XX", "X X X", "X   X", "X   X"],
    "N": ["X   X", "XX  X", "X X X", "X  XX", "X   X"],
    "O": [" XXX ", "X   X", "X   X", "X   X", " XXX "],
    "P": ["XXXX ", "X   X", "XXXX ", "X    ", "X    "],
    "Q": [" XXX ", "X   X", "X   X", "X  XX", " XXXX"],
    "R": ["XXXX ", "X   X", "XXXX ", "X  X ", "X   X"],
    "S": [" XXXX", "X    ", " XXX ", "    X", "XXXX "],
    "T": ["XXXXX", "  X  ", "  X  ", "  X  ", "  X  "],
    "U": ["X   X", "X   X", "X   X", "X   X", " XXX "],
    "V": ["X   X", "X   X", "X   X", " X X ", "  X  "],
    "W": ["X   X", "X   X", "X X X", "XX XX", "X   X"],
    "X": ["X   X", " X X ", "  X  ", " X X ", "X   X"],
    "Y": ["X   X", " X X ", "  X  ", "  X  ", "  X  "],
    "Z": ["XXXXX", "   X ", "  X  ", " X   ", "XXXXX"],
    "0": [" XXX ", "X  XX", "X X X", "XX  X", " XXX "],
    "1": ["  X  ", " XX  ", "  X  ", "  X  ", " XXX "],
    "2": [" XXX ", "X   X", "   X ", "  X  ", "XXXXX"],
    "3": ["XXXXX", "   X ", " XXX ", "   X ", "XXXXX"],
    "4": ["X   X", "X   X", "XXXXX", "    X", "    X"],
    "5": ["XXXXX", "X    ", "XXXX ", "    X", "XXXX "],
    "6": [" XXX ", "X    ", "XXXX ", "X   X", " XXX "],
    "7": ["XXXXX", "   X ", "  X  ", " X   ", "X    "],
    "8": [" XXX ", "X   X", " XXX ", "X   X", " XXX "],
    "9": [" XXX ", "X   X", " XXXX", "    X", " XXX "],
    " ": ["     ", "     ", "     ", "     ", "     "],
}

window = 800
buttons = [
    {
        "text": "regenerate maze",
        "start_x": window + 70,
        "end_x": window + 330,
        "start_y": 225,
        "end_y": 295,
    },
    {
        "text": "show or hide path",
        "start_x": window + 70,
        "end_x": window + 330,
        "start_y": 335,
        "end_y": 405,
    },
    {
        "text": "change color",
        "start_x": window + 70,
        "end_x": window + 330,
        "start_y": 445,
        "end_y": 515,
    },
]

colors = [
    {"background": 0x0f0f0f},      # Almost black
    {"walls": 0xe5e5e5},           # Light gray
    {"button_bg": 0x2a2a2a},       # Dark gray
    {"base_wall_color": 0x00ff00}, # White
    {
        "wall_colors": [
          0x00ff00,  # 1. Neon green (Matrix style)
          0xff00ff,  # 2. Magenta (electric)
          0x00ffff,  # 3. Cyan (bright aqua)
          0xff1493,  # 4. Deep pink (hot!)
          0xffff00,  # 5. Yellow (super bright)
          0xff4500,  # 6. Orange red (fiery)
          0x7fff00,  # 7. Chartreuse (lime punch)
          0x00e5ff,  # 8. Bright cyan (laser blue)
          0xb537f2,  # 9. Electric purple
          0xff6600,  # 10. Bright orange (sunset)
    ]
    },
]

"""

# Warm sunset theme
colors = [
    {"background": 0x2b1b17},      # Dark brown
    {"walls": 0xff6b35},           # Orange
    {"button_bg": 0x4a2c2a},       # Dark burgundy
    {"base_wall_color": 0xffeaa7}, # Light yellow
    {
        "wall_colors": [
            0xff6b35,  # Orange
            0xf7b731,  # Yellow
            0xee5a6f,  # Pink
            0xc44569,  # Rose
            0xf8b500,  # Gold
        ]
    },
]

# Forest/nature theme
colors = [
    {"background": 0x1b2e23},      # Dark forest green
    {"walls": 0x52796f},           # Sage green
    {"button_bg": 0x2f3e46},       # Dark teal
    {"base_wall_color": 0xcad2c5}, # Light sage
    {
        "wall_colors": [
            0x52796f,  # Sage
            0x84a98c,  # Light green
            0x6b9080,  # Teal green
            0xa7c957,  # Lime
            0x588157,  # Forest green
        ]
    },
]

# Purple/pink aesthetic
colors = [
    {"background": 0x2d1b3d},      # Deep purple
    {"walls": 0x8e44ad},           # Purple
    {"button_bg": 0x512b58},       # Dark purple
    {"base_wall_color": 0xe8daef}, # Light lavender
    {
        "wall_colors": [
            0x8e44ad,  # Purple
            0xe056fd,  # Bright purple
            0xbe29ec,  # Magenta
            0xff6bcb,  # Pink
            0xc471ed,  # Lavender
        ]
    },
]

# Retro/vaporwave theme
colors = [
    {"background": 0x120136},      # Deep purple-black
    {"walls": 0xff71ce},           # Hot pink
    {"button_bg": 0x2e0249},       # Dark purple
    {"base_wall_color": 0xb967ff}, # Light purple
    {
        "wall_colors": [
            0xff71ce,  # Hot pink
            0x01cdfe,  # Cyan
            0xb967ff,  # Purple
            0x05ffa1,  # Mint
            0xfffb96,  # Pale yellow
        ]
    },
]

# Minimalist grayscale
colors = [
    {"background": 0x0f0f0f},      # Almost black
    {"walls": 0xe5e5e5},           # Light gray
    {"button_bg": 0x2a2a2a},       # Dark gray
    {"base_wall_color": 0xffffff}, # White
    {
        "wall_colors": [
            0xffffff,  # White
            0xe5e5e5,  # Light gray
            0xb3b3b3,  # Medium gray
            0x808080,  # Gray
            0x4d4d4d,  # Dark gray
        ]
    },
]
"""
