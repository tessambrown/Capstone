# this file contains helper functions that I can use in other files
import random
# For local deployment
# from backend.errors import appError

# For Render deployment
from errors import appError

def checkChar(text):
    return isinstance(text, str) and len(text.strip()) > 0

def getRatio(width, height):
    if height == 0:
        raise appError("Failed to find height of canvas", 404)
    
    # find the gcd
    a, b = width, height
    while b != 0:
        a, b = b, a % b
    
    gcd_value = a

    reduced_width = width // gcd_value
    reduced_height = height // gcd_value

    return f"{reduced_width}:{reduced_height}"

def formatLyrics(sections):
    lines = []
    for section, lyrics in sections.items():
        lines.append(f"{section}:")
        lines.extend(lyrics)
        lines.append("")
    return "\n".join(lines)

def formatColor(name, colors):
    return f"{name}: {', '.join(colors)}"

# helper functions for calculating contrast between colors
# STEP 1: convert hex -> rgb
def hexToRGB(hex_color):
    hex_color = hex_color.lstrip("#")

    #split the hex code into pairs
    # ex: e6a43f -> "e6" = red, "a4" = green, "3f" = blue
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) 

# STEP 2: convert rgb -> relative luminance (the perceived brightness of color or light source)
def channelLuminance(c):
    c = c / 255 #normalize c
    return c / 12.92 if c<= 0.03928 else ((c+0.055) / 1.055) ** 2.4

# STEP 3: calculate the relative luminance of an RGB value
def relativeLuminance(rgb):
    r, g, b = rgb
    r_l = channelLuminance(r)
    g_l = channelLuminance(g)
    b_l = channelLuminance(b)
    return 0.2126 * r_l + 0.7152 * g_l + 0.0722 * b_l

# STEP 4: calculate the contrast ratio between two values
def contrastRatio(color1, color2):
    lum1 = relativeLuminance(hexToRGB(color1))
    lum2 = relativeLuminance(hexToRGB(color2))

    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)

    return (lighter + 0.05) / (darker + 0.05)

# return random colors from an array of color
def randColor(color_palette, num_colors):

    unique_palette = list(set(color_palette))

    if num_colors > len(unique_palette):
        return None
    
    return random.sample(unique_palette, num_colors)

def validateInputs(artist, song, canvas_choice):
    # validate the name of the artist
    if not isinstance(artist, str) or not artist.strip():
        raise appError("Invalid artist", 404)
    
    # validate the song title
    if not isinstance(song, str) or not artist.strip():
        raise appError("Invalid song title", 404)
    
    # change if new canvas sizes are added
    valid_choices = ["phone_screen", "phone", "poster"]

    # validate canvas choice
    if canvas_choice not in valid_choices:
        raise appError("Invalid canvas choice", 404)
    
    return artist, song, canvas_choice