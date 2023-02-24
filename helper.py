import os
import openai
import sys
import json

CONFIG_PATH = "/usr/local/lib/command_helper/config.json"

# read config file
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

openai.api_key = config["api_key"]
mode = config["mode"]
small_model = config["small_model"]
big_model = config["big_model"]

def get_command(text):
    # get number of words in the text
    num_words = len(text.split())
    
    if num_words > 30:
        # too big, print warning
        colored_print("red", "Warning: The text is too long. Using the first 30 words.")
        text = " ".join(text.split()[:30])
    model = big_model
    
    prompt = f"Translate text to a {mode} programmatic command:\nInstruction:\n{text}\n\nCommand:\n$"
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0
    )
    return response.choices[0].text

def explain_command(text):
    prompt = f"Explain this {mode} command:\n{text}\n\nExplanation:\n$"
    response = openai.Completion.create(
        model=big_model,
        prompt=prompt,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0
    )
    return response.choices[0].text

def check_dangerous_command(text):
    prompt = f"Check if {mode} command is dangerous:\n{text}\n\nDangerous:\n$"
    response = openai.Completion.create(
        model=small_model,
        prompt=prompt,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0
    )
    return response.choices[0].text

def change_terminal_color(color):
    if color == "red":
        print("\033[91m", end="")
    elif color == "green":
        print("\033[92m", end="")
    elif color == "yellow":
        print("\033[93m", end="")
    elif color == "blue":
        print("\033[94m", end="")
    elif color == "purple":
        print("\033[95m", end="")
    elif color == "cyan":
        print("\033[96m", end="")
    elif color == "white":
        print("\033[97m", end="")
    else:
        print("\033[97m", end="")

def colored_print(color, *args):
    change_terminal_color(color)
    print(*args)
    change_terminal_color("white")

def get_options(args):
    options = []
    st = 0
    while st < len(args):
        if args[st].startswith("-"):
            # get the option without "-"
            options.append(args[st].replace("-", ""))
        else:
            break
        st += 1
    return options, st


if __name__ == "__main__":

    # get options starting with "-"
    options, st = get_options(sys.argv[1:])

    COPY = False
    EXPLAIN = False
    FORCE = False

    if "h" in options or "help" in options:
        pass
    if "b" in options or "batch" in options:
        pass
    if "c" in options or "copy" in options:
        COPY = True
    if "e" in options or "explain" in options:
        EXPLAIN = True
    if "s" in options or "safe" in options:
        pass
    if "f" in options or "force" in options:
        FORCE = True

    #get arguments for the command
    args = sys.argv[1 + st:]
    #get the text to convert
    text = " ".join(args)
    #get the command
    command = get_command(text)
    #print the command in purple
    colored_print("purple", "\n>", command, "\n")

    if EXPLAIN:
        explanation = explain_command(command)
        colored_print("cyan", "#", command)
        print(explanation)
        print("")

    input_cmd = ""
    while input_cmd != "y" and input_cmd != "n":
        if not FORCE:
            input_cmd = input("Execute command? (y/n/\033[4me\033[0mxplain/\033[4mc\033[0maution]): ")
        else:
            input_cmd = input()

        if FORCE or input_cmd == "y":
            colored_print("yellow", "$", command)
            os.system(command)
            print("")
            break
        elif input_cmd == "c":
            colored_print("red", "?", command)
            response = check_dangerous_command(command)
            print(response)
        elif input_cmd == "e":
            explanation = explain_command(command)
            colored_print("cyan", command)
            print(explanation)
        print("")

    # whether copy the command to clipboard or not
    if not COPY:
        input_cmd = input("Copy command to clipboard? (y/[n]): ")
    if COPY or input_cmd == "y":
        colored_print("green", "Command copied to clipboard.\n")
        os.system(f"echo '{command}' | pbcopy")

