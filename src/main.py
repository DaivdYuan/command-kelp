from .shells import shell
from .systems import Path

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


        

