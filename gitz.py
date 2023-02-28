import os
import sys
import pyfiglet
import git.handle.git as user_git
import command_lines.arguments.args as arg

if __name__=="__main__":
    user_git.load_config()
    
    if user_git.state != None:
        state_print = pyfiglet.figlet_format(f"Git{user_git.state[3:].capitalize()}")
    else:
        state_print = pyfiglet.figlet_format(f"GitZ")
    print(state_print)
    
    
    if not os.path.exists(os.path.expanduser('~/gitz/.data.json')):
        user_git.gitz_init()
    
    elif len(sys.argv)>1:
        arg.proccess_command(sys.argv[1])
    
    else:
        print(f"You're currently using Git{user_git.state[3:].capitalize()}")
        