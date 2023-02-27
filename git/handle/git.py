import os
import json
import time
import getpass

responses = ['y','n','no','yes']
git_responses = ['l','lab','h','hub']
state = None
gitlab = None
github = None
change = False

def git_store(git_name,git_email,git_type,info):
    with open(os.path.expanduser('~/gitz/.data.json'),'w') as git_file:
        git = {'name':git_name,'email':git_email}
        info[git_type] = git
        json.dump(info,git_file)

def git_load():
    with open(os.path.expanduser('~/gitz/.data.json'),'r') as git_file:
        return json.load(git_file)

def get_username(git_type):
     return input(f'Enter your {git_type} username: ')

def get_email(git_type):
    return input(f'Enter your {git_type} email: ')

def ssh(git_type):
    if not os.path.exists(os.path.expanduser('~/.ssh/id_rsa.pub')) or not os.path.exists(os.path.expanduser('~/.ssh/id_rsa')):
        ssh_key = input("This PC doesn't have an SSH Key, want to generate one?(Y/n): ")
        if ssh_key.lower() == 'y' or ssh_key == 'yes':
            os.system("ssh-keygen")
            with open(os.path.expanduser('~/.ssh/id_rsa.pub'),'r') as pub_ssh:
                lines = pub_ssh.read()
                print(f'Copy the following key and configure it as your ssh key on the {git_type} website:\n')
                time.sleep(3)
                print(lines+'\n')
                getpass.getpass('Press enter to continue...\n')
    
        
    x = ''
    while x not in responses:
        x = input(f'Do you have the ssh on this pc on your {git_type}?(Y/n): ').lower()
    if x == 'n' or x == 'no':
        with open(os.path.expanduser('~/.ssh/id_rsa.pub'),'r') as pub_ssh:
            lines = pub_ssh.read()
            print(f'Copy the following key and configure it as your ssh key on the {git_type} website:\n')
            time.sleep(3)
            print(lines+'\n')
            getpass.getpass('Press enter to continue...\n')
    

def gitz_init():

    info = {}
    if os.path.exists(os.path.expanduser('~/gitz/.data.json')) and os.path.getsize(os.path.expanduser('~/gitz/.data.json'))>0:
        info = git_load()
    data_init(info)

    if os.path.exists(os.path.expanduser('~/gitz/.config.json')) and os.path.getsize(os.path.expanduser('~/gitz/.config.json'))>0:
        with open(os.path.expanduser('~/gitz/.config.json'),'r') as config_file:
            config_info = json.load(config_file)
            if 'state' in config_info:
                if config_info['state'] == 'github' or config_info['state'] == 'gitlab':
                    print(f"You're currently using Git{config_info['state'][3:].capitalize()} ")
    
    else:
        config_data(info)

def data_init(info):
    global responses

    if 'github' not in info:
        git_exist = ''
        while git_exist not in responses: 
            git_exist = input("Do you have a GitHub account?(Y/n): ").lower()
        if git_exist == 'y' or git_exist == 'yes':
            git_store(get_username('GitHub'),get_email('GitHub'),'github',info)
            ssh('GitHub')
    
    if 'gitlab' not in info:
        git_exist = ''
        while git_exist not in responses: 
            git_exist = input("Do you have a GitLab account?(Y/n): ").lower()
        if git_exist == 'y' or git_exist == 'yes':
            git_store(get_username('GitLab'),get_email('GitLab'),'gitlab',info)
            ssh('GitLab')

def config_data(info):
    global git_responses
    git = ''
    if len(info) == 2:
        print('Choose Git to use:\n • H or Hub for GitHub\n • L or Lab for GitLab')
        while git not in git_responses:
            git = input(' > ').lower()
        if git == 'hub' or git == 'h':
            git = 'github'
        else:
            git = 'gitlab'
    elif len(info) == 1:
        if 'gitlab' in info:
            git = 'gitlab'
        else:
            git = 'github'
    
    config_info = {}
    if os.path.exists(os.path.expanduser('~/gitz/.config.json')):
        with open(os.path.expanduser('~/gitz/.config.json'),'r') as config_file:
            config_info = json.load(config_file)
    config_info['state'] = git
    config_info['configured_user'] = info[git]['name']
    config_info['configured_email'] = info[git]['email']
    with open(os.path.expanduser('~/gitz/.config.json'),'w') as config_file:
        json.dump(config_info,config_file)

def config_git(git_type):
    info = {}
    if os.path.exists(os.path.expanduser('~/gitz/.data.json')) and os.path.getsize(os.path.expanduser('~/gitz/.data.json'))>0:
        info = git_load()
    git_store(get_username(git_type),get_email(git_type),git_type.lower(),info)

def switch():
    global github,gitlab,change,state
    if github == None:
        print("You don't have a GitHub account")
        x = input('You want to config a GitHub account?(Y/n): ')
        if x.lower() == 'y' or x.lower() == 'yes':
            config_git('GitHub')
        else:return 
    elif gitlab == None:
        print("You don't have a GitLab account")
        x = input('You want to config a GitLab account?(Y/n): ')
        if x.lower() == 'y' or x.lower() == 'yes':
            config_git('GitLab')
        else:return 
    
    if state == 'gitlab': state = 'github'
    else:                 state = 'gitlab'
    change = True

def load_config():
    global state,github,gitlab

    if os.path.exists(os.path.expanduser('~/gitz/.config.json')):
        with open(os.path.expanduser('~/gitz/.config.json'),'r') as config_file:
            config_info = json.load(config_file)
            state = config_info['state']
    if os.path.exists(os.path.expanduser('~/gitz/.data.json')):
        with open(os.path.expanduser('~/gitz/.data.json'),'r') as data_file:
            data_info = json.load(data_file)
            if 'gitlab' in data_info:
                gitlab = data_info['gitlab']
            if 'github' in data_info:
                github = data_info['github']

def get_git():
    global state
    if state == 'gitlab':
        return github
    else:
        return gitlab


def get_git_type():
    git = ''
    print('Choose Git to use:\n • H or Hub for GitHub\n • L or Lab for GitLab')
    while git not in git_responses:
            git = input(' > ').lower()
    if git.lower() == 'h' or git.lower() == 'hub':
        return 'GitHub'
    else:
        return 'GitLab'



def reconfig(git_type):
    config_git(git_type)
