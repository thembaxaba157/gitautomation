import os
import json
import pyfiglet
import git.handle.git as ugit


def run_argument(argument):
    arguments = ['switch','reconfig']
    if argument.lower() == 'switch' or argument.lower() == 's':
        ugit.switch()
    elif 'reconfig' in argument.lower() or 'rc' in argument.lower():
        ugit.reconfig(ugit.get_git_type())


def proccess_command(argument):
    run_argument(argument)
    print(ugit.change)
    if ugit.change == True:
        git = ugit.get_git()
        config_info = {}
        with open(os.path.expanduser('~/gitz/.config.json'),'r') as config_file:
            config_info = json.load(config_file)
            config_info['state'] = ugit.state
            config_info['configured_user'] = git['name']
            config_info['configured_email'] = git['email']
        with open(os.path.expanduser('~/gitz/.config.json'),'w') as config_file:
            json.dump(config_info,config_file)
        os.system(f"git config --global user.name {git['name']}")
        os.system(f"git config --global user.email {git['email']}")
        os.system(f'clear')
        state_print = pyfiglet.figlet_format(f"Git{ugit.state[3:].capitalize()}")
        print(state_print)
        print(f'Successfully switched to {ugit.state[:3].capitalize()}{ugit.state[3:].capitalize()}')