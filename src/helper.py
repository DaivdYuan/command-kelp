import os
import openai
import sys
import json, sys
from subprocess import Popen, PIPE, STDOUT

from .systems import run_command
from .shells import shell
from .logs import *

if os.environ.get("OPENAI_API_KEY") is None:
    warning_print("Warning: OPENAI_API_KEY environment variable not found. Please set it to your OpenAI API key.")
    exit()

openai.api_key = os.environ.get("OPENAI_API_KEY")
mode = os.environ.get("KELP_SHELL")
small_model = "text-davinci-003"
big_model = "text-curie-001"

#######################

def parse_history_command():
    # get from `KELP_HISTORY` environment variable
    history = os.environ.get("KELP_HISTORY")
    if history is None or history == "":
        # get from `HISTFILE` environment variable
        raise NotImplementedError
    
    #output("History:", history)
    
    # get the last command not starting with "kelp"
    last_command = None
    for command in history.split("\n")[::-1]:
        if not command.startswith("kelp"):
            last_command = command
            break

    return last_command

def sanitize(text):
    # get only the first line, and strip the newline character
    return text.split("\n")[0].strip()

#######################

def get_command(text):
    # get number of words in the text
    num_words = len(text.split())
    
    if num_words > 30:
        # too big, print warning
        warning_print("Warning: The text is too long. Using the first 30 words.")
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
    return sanitize(response.choices[0].text)

def correct_command(text):
    info_print("Correcting:", text)
    prompt = f"This {mode} command is wrong:\n{text}\n\nCorrect and meaningful command:\n$"
    response = openai.Completion.create(
        model=big_model,
        prompt=prompt,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0
    )
    return sanitize(response.choices[0].text)

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


def main():
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

    if args == [] or args == ["fuck"]:
        # enable fuck mode
        hist_command = parse_history_command()
        if hist_command is None:
            info_print("No last command found")
            exit(1)
        else:
            command = correct_command(hist_command)
    else:
        #get the text to convert
        text = " ".join(args)
        #get the command
        command = get_command(text)
    
    #print the command in purple
    suggestion_print("\n>", command, "\n")

    if EXPLAIN:
        explanation = explain_command(command)
        explain_print("#", command)
        info_print(explanation)
        print("")

    input_cmd = ""
    while input_cmd != "y" and input_cmd != "n":
        if not FORCE:
            input_cmd = input("\033[1mExecute command?\033[0m (y/n/\033[4me\033[0mxplain/\033[4mc\033[0maution]): ")
        else:
            input_cmd = input()

        if FORCE or input_cmd == "y":
            running_print("$", command)
            os.system(f"eval \'{command}\' 1>&2")
            output("")
            break
        elif input_cmd == "c":
            warning_print("?", command)
            response = check_dangerous_command(command)
            info_print("Is this dangerous?  ", response)
        elif input_cmd == "e":
            explanation = explain_command(command)
            explain_print("#", command)
            info_print(explanation)
        output("")

    # whether copy the command to clipboard or not
    if not COPY:
        input_cmd = input("\033[1mCopy command to clipboard?\033[0m (y/[n]): ")
    if COPY or input_cmd == "y":
        success_print("Command copied to clipboard.\n")
        os.system(f"echo '{command}' | pbcopy")

