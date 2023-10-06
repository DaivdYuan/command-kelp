from .shells import shell
from .systems import Path
from .logs import *

def get_alias():
    print(shell.app_alias("kelp"))

def configure():
    configuration_details = shell.how_to_configure()
    #print(configuration_details)

    try:
        path = Path(configuration_details.path).expanduser()
        with path.open('r') as shell_config:
            if configuration_details.content in shell_config.read():
                print("Already configured")
                print(f"Run `{configuration_details.reload}` to use kelp")
                return

        with path.open('a') as shell_config:
            shell_config.write("\n")
            shell_config.write(configuration_details.content)
            shell_config.write("\n")
            print("Configured")
            print(f"Run `{configuration_details.reload}` to use kelp")
        
    except Exception as e:
        print(e)
        print("Could not write to file. Please check permissions.")

def api_key_setup_wizard():
    configuration_details = shell.how_to_configure()
    explain_print("\nAPI key setup wizard")
    info_print("Please enter your OpenAI API key below. Visit https://platform.openai.com/account/api-keys to get your API key. \n (Press CTRL+C or enter to exit)")
    api_key = input("Your API key: ")
    if api_key == "":
        warning_print("No API key entered. Exiting.")
        return
    if api_key[:3] != "sk-":
        warning_print("Invalid API key. Should start with `sk-`. Exiting.")
        return
    info_print("Writing to config file...")
    try:
        path = Path(configuration_details.path).expanduser()
        with path.open('r') as shell_config:
            content = shell_config.read()
            added = False
            # check if any line starts with "export OPENAI_API_KEY="
            for line in content.split("\n"):
                if line.startswith("export OPENAI_API_KEY="):
                    # replace the line with the new API key
                    content = content.replace(line, f"export OPENAI_API_KEY={api_key}")
                    added = True
                    break

            if not added:
                # add the line to the end of the file
                content += f"\nexport OPENAI_API_KEY={api_key}\n"
            
        with path.open('w') as shell_config:
            shell_config.write(content)

        info_print("\nAPI Key Setup Done.")
        info_print(f"Run `{configuration_details.reload}` to use kelp")
        
    except Exception as e:
        print(e)
        warning_print("Could not write to file. Please check permissions.")

