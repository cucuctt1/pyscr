import random
import string


def generate_random_string(length):
    characters = string.ascii_letters
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
def generate_random_color():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    hex_color = "#{:02X}{:02X}{:02X}".format(red, green, blue)
    return hex_color

def generate_contrasting_color(hex_color, brightness_threshold=128):
    hex_color = hex_color.lstrip("#")
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    brightness = sum(rgb_color) / 3
    target_brightness = 255 if brightness < brightness_threshold else 0
    ratio = target_brightness / brightness if brightness != 0 else 1
    adjusted_color = tuple(min(max(int(value * ratio), 0), 255) for value in rgb_color)
    hex_contrasting_color = "#{:02X}{:02X}{:02X}".format(*adjusted_color)
    return hex_contrasting_color

print(generate_contrasting_color("#FF6A00"))
