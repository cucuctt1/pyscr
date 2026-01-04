import string
def hex_decode(r,g,b):
    r = int(r)
    g = int(g)
    b = int(b)
    hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
    return hex_color
def rgb_decode(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def border_color(hex_color,darkness_value = 5):
    r,g,b = rgb_decode(hex_color)
    r = max(0,r-darkness_value)
    g = max(0, g - darkness_value)
    b = max(0, b - darkness_value)

    return hex_decode(r,g,b)

def generate_contrasting_color(hex_color, brightness_threshold=128):
    hex_color = hex_color.lstrip("#")
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    brightness = sum(rgb_color) / 3
    target_brightness = 255 if brightness < brightness_threshold else 0
    ratio = target_brightness / brightness if brightness != 0 else 1
    adjusted_color = tuple(min(max(int(value * ratio), 0), 255) for value in rgb_color)
    hex_contrasting_color = "#{:02X}{:02X}{:02X}".format(*adjusted_color)
    return hex_contrasting_color