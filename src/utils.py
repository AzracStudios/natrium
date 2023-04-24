#############
### UTILS ###
#############


def check_type(object, _type):
    return type(object).__name__ == _type.__name__


## COLORS
# REF: https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html


# Generates python code for standard ANSI color codes along with a basic test
# PS: I am too lazy to write the functions out myself :)
def color_generator():
    colors = [
        "black",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
    ]

    code = ""
    for i, color in enumerate(colors):
        code += f"""
def {color}(string: str):
    return f"\\u001b[{30 + i}m{"{string}"}\\u001b[0m"

def bright_{color}(string: str):
    return f"\\u001b[{30 + i};1m{"{string}"}\\u001b[0m"
        """

    code += "\ndef test_colors(string: str):\n"
    for color in colors:
        code += f"""
    print({color}(string))
    print(bright_{color}(string))
        """

    return code


def black(string: str):
    return f"\u001b[30m{string}\u001b[0m"


def bright_black(string: str):
    return f"\u001b[30;1m{string}\u001b[0m"


def red(string: str):
    return f"\u001b[31m{string}\u001b[0m"


def bright_red(string: str):
    return f"\u001b[31;1m{string}\u001b[0m"


def green(string: str):
    return f"\u001b[32m{string}\u001b[0m"


def bright_green(string: str):
    return f"\u001b[32;1m{string}\u001b[0m"


def yellow(string: str):
    return f"\u001b[33m{string}\u001b[0m"


def bright_yellow(string: str):
    return f"\u001b[33;1m{string}\u001b[0m"


def blue(string: str):
    return f"\u001b[34m{string}\u001b[0m"


def bright_blue(string: str):
    return f"\u001b[34;1m{string}\u001b[0m"


def magenta(string: str):
    return f"\u001b[35m{string}\u001b[0m"


def bright_magenta(string: str):
    return f"\u001b[35;1m{string}\u001b[0m"


def cyan(string: str):
    return f"\u001b[36m{string}\u001b[0m"


def bright_cyan(string: str):
    return f"\u001b[36;1m{string}\u001b[0m"


def white(string: str):
    return f"\u001b[37m{string}\u001b[0m"


def bright_white(string: str):
    return f"\u001b[37;1m{string}\u001b[0m"


def test_colors(string: str):

    print(black(string))
    print(bright_black(string))

    print(red(string))
    print(bright_red(string))

    print(green(string))
    print(bright_green(string))

    print(yellow(string))
    print(bright_yellow(string))

    print(blue(string))
    print(bright_blue(string))
