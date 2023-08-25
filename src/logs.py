import sys

def output(*args, end="\n", sep=" "):
    for s in args:
        sys.stderr.write(s + sep)
    sys.stderr.write(end)
    sys.stderr.flush()

def change_terminal_color(color):
    if color == "red":
        output("\033[91m", end="")
    elif color == "green":
        output("\033[92m", end="")
    elif color == "yellow":
        output("\033[93m", end="")
    elif color == "blue":
        output("\033[94m", end="")
    elif color == "purple":
        output("\033[95m", end="")
    elif color == "cyan":
        output("\033[96m", end="")
    elif color == "white":
        output("\033[97m", end="")
    else:
        output("\033[97m", end="")

def colored_print(color, *args):
    change_terminal_color(color)
    output(*args)
    change_terminal_color("white")

def info_print(*args):
    colored_print("white", *args)

def suggestion_print(*args):
    colored_print("purple", *args)

def explain_print(*args):
    colored_print("cyan", *args)

def warning_print(*args):
    colored_print("red", *args)

def success_print(*args):
    colored_print("green", *args)

def running_print(*args):
    colored_print("yellow", *args)

def input(*args):
    output(*args, end="")
    return sys.stdin.readline().strip()