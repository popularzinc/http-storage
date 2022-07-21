import ast
import os
import shutil

def Create(user,password):
    try:
        account_folder = 'Accounts/'+user
        info_file = account_folder+'/info'
        info = {'password':password,'projects':['']}
        os.mkdir(account_folder)
        with open(info_file,'w') as f:
            f.write(str(info))
        shutil.copy('profilepic.png',account_folder)
        return True
    except:
        return False

def Login(user,password):
    account_folder = 'Accounts/'+user
    info_file = account_folder+'/info'
    with open(info_file,'r') as f:
        data = ast.literal_eval(f.read())
    if(password == data['password']):
        return True
    return False

def Info(account):
    try:
        account_folder = 'Accounts/'+user
        info_file = account_folder+'/info'
        with open(info_file,'r') as f:
            data = ast.literal_eval(f.read())
        return data
    except:
        return {}
