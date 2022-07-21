import ast
import os
from datetime import date
import shutil
import difflib

user = False

def Fix(path):
    end = ''
    project = path.split('/')[0]
    new = path.split('/')
    for i in new[1:]:
        end += i+'/'
    return project,end[:-1]

def Info(project):
    info_file = 'Projects/'+project+'/info'
    with open(info_file, 'r') as f:
        data = ast.literal_eval(f.read())
    return data

def Top(path,css='main.css',style='',view=False,login=False):
    ### generate top part of page to make easier to program
    end = '''
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="/CSS/'''+css+'''">
    <div class="top-bar">
      <input class="search-bar" type="text" placeholder="Search..">
    '''
    if(user):
        end += UserPic()
    end += '''
    </div>
  </head>
  <body>
    <div class="project-top">
      <a href="/">
        <img class="title-folder" src="/pics/title-folder.png">
      </a>
      <span class="title">'''+path+'''</span>
    </div>

    <div class="options-bar">'''
    if(login):
        end += '''</div>
        <div class="container">'''
        return end
    home = path
    try:
        home = path.split('/')[0]
    except:
        pass
    n = len(os.listdir('Projects/'+home+'/Issues'))

    end += '<a href="/project/'+path+'" style="text-decoration:none;color:black;">\n'
    if(style == 'data'):
        end += '<span class="option-selected">Data</span>\n</a>'
    else:
        end += '<span class="option">Data</span>\n</a>'
    if(not view):
        end += '<a href="/issues/'+path+'" style="text-decoration:none;color:black;">\n'
        if(style == 'issues'):
            end += '<span class="option-selected">Issues ('+str(n)+')</span>\n</a>'
        else:
            end += '<span class="option">Issues ('+str(n)+')</span>\n</a>'

        end += '<a href="/settings/'+path+'" style="text-decoration:none;color:black;">\n'
        if(style == 'settings'):
            end += '<span class="option-selected">Settings</span>\n</a>'
        else:
            end += '<span class="option">Settings</span>\n</a>'

        end += '<a href="/trash/'+path+'" style="text-decoration:none;color:black;">\n'
        if(style == 'trash'):
            end += '<span class="option-selected">Trash</span>\n</a>'
        else:
            end += '<span class="option">Trash</span>\n</a>'

    end += '''</div>
    <div class="container">'''
    return end

def Wrap(path,data,css='main.css',style='data',view=False,login=False):
    return Top(path,css,style,view=view,login=login)+data+End()

def End():
    return '''
</div>
  </body>
</html>'''

### UPLOAD #####

def Upload(path):
    end = '''
<form action="/upload/'''+path+'''" method="POST" enctype="multipart/form-data">
  <input type="file" name="data" multiple="">
  <input class="button" type="submit" value="Upload">
<form>'''

    return Wrap(path,end)

def Backup(path):
    project = 'Projects/'+path
    file = 'Projects/'+path+'/info'
    with open(file,'r') as f:
        data = ast.literal_eval(f.read())
    if(data['backup'] == 'backup'):
        shutil.make_archive('Backup/'+path,'zip',project)

def Settings(path):
    project,path = Fix(path)
    name = path.split('/')[-1]
    file = 'Projects/'+project+'/info'
    with open(file,'r') as f:
        data = ast.literal_eval(f.read())
    try:
        data['public']
    except:
        data['public'] = ''
        data['backup'] = ''
    backup = ''
    public = ''
    if(data['public'] == 'public'):
        public = 'checked'
    if(data['backup'] == 'backup'):
        backup = 'checked'

    variables = {'PROJECT_NAME':project,
    'DESC':data['desc'],
    'DATE':data['created'],
    'DEL_LINK':'/deleteproject/'+project,
    'PCHKD':public,
    'BCHKD':backup
    }

    end = ParseFile('settings.html',variables)

    return Wrap(project,end,css='settings.css',style='settings')


def NewFolder(path):
    end = '''
<form action="/addfolder/'''+path+'''" method="POST">
  <input type="text" name="name" placeholder="Name">
  <input class="button" type="submit" value="Create">
<form>
'''
    return Wrap(path,end)

def Trash(path):
    end = '<a style="text-decoration:none;" href="/cleartrash/'+path+'"><div class="clear">Clear Trash</div></a><br><br>'

    for i in os.listdir('Projects/'+path+'/Trash'):
        #end += '<a href="/downloadtrash/'+path+'/'+str(i)+'">'+str(i)+'</a><br>'
        end += '<div style="display:inline-flex">'
        end += '  <a href="/downloadtrash/'+path+'/'+str(i)+'">'
        end += '    <div class="trash">'+str(i)+'</div>'
        end += '  </a>'
        end += '  <a style="text-decoration:none;" href="/deletetrash/'+path+'/'+str(i)+'"><div class="erase">Erase</div></a>'
        end += '</div><br>'


    return Wrap(path,end,css='trash.css',style='trash')

def Date():
    return date.today().strftime("%B %d, %Y")

def dif(code_1,code_2):

    def show_diff(seqm):
        old_new = ''
        output= []
        for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
            if opcode == 'equal':
                old_new += str(seqm.a[a0:a1]).replace(' ','&nbsp;').replace('<','&lt;').replace('>','&gt;').replace('\n','<br>')
                output.append(str(seqm.a[a0:a1]).replace(' ','&nbsp;').replace('<','&lt;').replace('>','&gt;').replace('\n','<br>'))
            elif opcode == 'insert':
                old_new += '<span class="green">'
                old_new += str(seqm.b[b0:b1]).replace(' ','&nbsp;').replace('<','&lt;').replace('>','&gt;').replace('\n','<br>')
                old_new += '</span>'
                #output.append('<span class="green">' + str(seqm.b[b0:b1]).replace(' ','&nbsp;').replace('<','&lt;').replace('>','&gt;').replace('\n','<br>') + '</span>')
            elif opcode == 'delete':
                output.append('<span class="red">' + str(seqm.a[a0:a1]).replace(' ','&nbsp;').replace('<','&lt;').replace('>','&gt;').replace('\n','<br>') + '</span>')
        return ''.join(output),old_new

    end,old_new = show_diff(difflib.SequenceMatcher(None, code_1, code_2))
    #old_end = show_diff(difflib.SequenceMatcher(None, "lorem foo ipsum dolor amet", "lorem ipsum dolor sit amet"))
    #return old_end.replace('  ','&ensp;'),new_end.replace('  ','&ensp;')
    return old_new,end

def Issue(path):
    project,issue = Fix(path)
    file_path = 'Projects/'+project+'/Issues/'+issue
    with open(file_path,'r') as f:
        data = ast.literal_eval(f.read())
    variables = {'TITLE':issue,
    'DESC':data['desc'],
    'DATA':data['data'],
    'FILE':data['file'],
    'CODE1':data['code1'],
    'CODE2':data['code2'],
    'PROJECT':project
    }
    end = ParseFile('issue.html',variables)
    return Wrap(project,end,css='issue.css',style='issues')

def CreateIssue(path,title,desc):
    file = 'Projects/'+path+'/Issues/'+title
    data = {'desc':desc,'start_date':Date(),
    'data':'',
    'file':'',
    'end_date':'',
    'start_files':str(os.listdir('Projects/'+path+'/Data')),
    'end_files':'',
    'line1':'','line2':'',
    'code1':'','code2':''}
    with open(file,'w') as f:
        f.write(str(data))

def ComIssue(path):
    project,issue = Fix(path)
    file_path = 'Projects/'+project+'/ComIssues/'+issue
    with open(file_path,'r') as f:
        data = ast.literal_eval(f.read())
    end_files = ast.literal_eval(data['end_files'])
    start_files = ast.literal_eval(data['start_files'])
    new_files = []
    for i in end_files:
        if(i not in start_files):
            new_files.append('<span class="green">'+str(i)+'</span>')
        else:
            new_files.append(str(i))
    new,old = dif(data['code1'],data['code2'])
    variables = {'TITLE':issue,
            'DESC':data['desc'],
            'DATA':data['data'],
            'FILE':data['file'],
            'PROJECT':project,
            'NEW_FILS':str(new_files),
            'START_DATE':data['start_date'],
            'END_DATE':data['end_date'],
            'CODE1':old,
            'CODE2':new}
    end = ParseFile('com-issue.html',variables)
    return Wrap(project,end,css='com-issue.css',style='issues')

def CreateIssues(path):
    end = ParseFile('create-issue.html',variables=[])
    return Wrap(path,end,css='create-issue.css')

def Issues(path):
    end = '<div style="padding:20px;">\n<a style="text-decoration:none;" href="/createissue/'+path+'"><div class="create">Create New Issue</div></a><br>'

    if(len(os.listdir('Projects/'+path+'/Issues')) != 0):
        end += '<div class="issue-top">Current Issues</div>'

    for i in os.listdir('Projects/'+path+'/Issues'):
        info_file = 'Projects/'+path+'/Issues/'+i
        with open(info_file,'r') as f:
            info = ast.literal_eval(f.read())
        title = i
        desc = info['desc']
        start_date = info['start_date']
        end += '<a href="/issue/'+path+'/'+title+'" style="text-decoration: none;">'
        end += '<div class="issue">'
        end += '  <div class="icon"><img class="image" src="/pics/info.png"></div>'
        end += '  <div class="issue-title">'+title+'</div>'
        end += '  <div class="issue-desc">'+start_date+' | '+desc+'</div>'
        end += '</div>'
        end += '</a>'

    end += '<br><br><br><br><br><br><br>'

    if(len(os.listdir('Projects/'+path+'/ComIssues')) != 0):
        end += '<div class="issue-top">Completed Issues</div>'

    for i in os.listdir('Projects/'+path+'/ComIssues'):
        info_file = 'Projects/'+path+'/ComIssues/'+i
        with open(info_file,'r') as f:
            info = ast.literal_eval(f.read())
        title = i
        desc = info['desc']
        end_date = info['end_date']
        end += '<a href="/comissue/'+path+'/'+title+'" style="text-decoration: none;">'
        end += '<div class="com-issue">'
        end += '  <div class="icon"><img class="image" src="/pics/checkmark.png"></div>'
        end += '  <div class="com-issue-title">'+title+'</div>'
        end += '  <div class="com-issue-desc">'+end_date+' | '+desc+'</div>'
        end += '</div>'
        end += '</a>'

    return Wrap(path,end,css='issues.css',style='issues')

def NewProject():
    end = '''
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="/CSS/upload.css">
    <div class="top-bar">
      <input class="search-bar" type="text" placeholder="Search..">
    </div>
  </head>
  <body>
    <div class="project-top">
      <a href="/">
        <img class="title-folder" src="/pics/title-folder.png">
      </a>
      <span class="title">Create New Project</span>
    </div>
    <div class="options-bar">
      <span class="option-selected">Data</span>
      <span class="option">Settings</span>
    </div>
    <div class="container">
      <form action="/create" method="POST">
        <input type="text" name="title" placeholder="Title">
        <input type="text" name="desc" placeholder="Description">
        <input class="button" type="submit" value="Create">
      <form>
    </div>
  </body>
</html>
'''
    return end

def NewRelease():
    end = '''
      <form method="POST">
        <input type="text" name="title" placeholder="Title">
        <input class="button" type="submit" value="Create">
      <form>
'''
    return Wrap('Create New Release',end)

#####################

def ParseFile(file,variables):

    f = open('Pages/'+file,'r')
    data = f.read()
    f.close()

    root = data.split('<!---->')[1]
    end = root
    for i in variables:
        end = end.replace(i,variables[i])
    return end

#### EDIT FILE #####


def Edit(title):
    binary = False
    project,path = Fix(title)
    name = path.split('/')[-1]
    file = 'Projects/'+project+'/Data/'+path
    print(name,file)
    try:
        with open(file, 'r') as f:
            data = f.read()
    except:
        binary = True
        with open(file, 'rb') as f:
            data = f.read()

    if(binary):
        variables = {'FILE_NAME':name,
                'DOWN_LINK':'/downloadfile/'+project+'/'+path,
                'BACK_LINK':'/',
                'DEL_LINK':'/delete/'+project+'/'+path,
                'FILE_DATA':str(data),
                'IMAGE_SRC':'/downloadfile/'+project+'/'+path}
        end = ParseFile('edit-image.html',variables)
        #end += '''\n<img class="image" src="/downloadfile/'''+project+'/'+path+'''">'''
    else:
        variables = {'FILE_NAME':name,
                'DOWN_LINK':'/downloadfile/'+project+'/'+path,
                'BACK_LINK':'/project/'+project,
                'DEL_LINK':'/delete/'+project+'/'+path,
                'FILE_DATA':str(data)}

        end = ParseFile('edit.html',variables)
        #end += '''\n<textarea name="data" class="desc-input" type="text" placeholder="Data in file..">'''+data+'''</textarea><br><br>'''

    return Wrap(project,end,css='edit.css')

def View(title):
    binary = False
    project,path = Fix(title)
    name = path.split('/')[-1]
    file = 'Projects/'+project+'/Data/'+path
    try:
        with open(file, 'r') as f:
            data = f.read()
    except:
        binary = True
        with open(file, 'rb') as f:
            data = f.read()

    if(binary):
        variables = {'FILE_NAME':name,
                'DOWN_LINK':'/downloadfile/'+project+'/'+path,
                'BACK_LINK':'/',
                'DEL_LINK':'/delete/'+project+'/'+path,
                'FILE_DATA':str(data),
                'IMAGE_SRC':'/downloadfile/'+project+'/'+path}
        end = ParseFile('edit-image.html',variables)
        #end += '''\n<img class="image" src="/downloadfile/'''+project+'/'+path+'''">'''
    else:
        variables = {'FILE_NAME':name,
                'DOWN_LINK':'/downloadfile/'+project+'/'+path,
                'BACK_LINK':'/project/'+project,
                'FILE_DATA':str(data)}

        end = ParseFile('view.html',variables)
        #end += '''\n<textarea name="data" class="desc-input" type="text" placeholder="Data in file..">'''+data+'''</textarea><br><br>'''

    return Wrap(project,end,css='view.css',view=True)


def Login():
    variables = {}
    end = ParseFile('login.html',variables)
    return Wrap('Login',end,css='ca.css',view=True,login=True)

def CreateAccount():
    variables = {}
    end = ParseFile('ca.html',variables)
    return Wrap('Create Account',end,css='ca.css',view=True,login=True)

#####################

def SaveFile(file,data):
    try:
        f = open(file,'w')
        f.write(data)
        f.close()
    except:
        f = open(file,'wb')
        f.write(data)
        f.close()


#### OPEN PROJECT ####

def Project(title,dir=False):
    project,x = Fix(title)
    if(dir):
        root,path = Fix(title)
        folder = 'Projects/'+root
        data_folder = folder+'/Data/'+path
    else:
        folder = 'Projects/'+title
        data_folder = folder+'/Data'
    data = os.listdir(data_folder)
    releases = os.listdir(folder+'/Releases')
    info_file = folder+'/info'
    with open(info_file, 'r') as f:             # open and read info file
        info = ast.literal_eval(f.read())     # convert to dictionary
    n = len(os.listdir('Projects/'+project+'/Issues'))

    end = '''
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="/CSS/main.css">
    <div class="top-bar">
      <input class="search-bar" type="text" placeholder="Search..">
    '''
    if(user):
        end += UserPic()
    end += '''
    </div>
  </head>
  <body>
    <div class="project-top">
      <a href="/">
        <img class="title-folder" src="/pics/title-folder.png">
      </a>
      <span class="title">'''+title+'''</span>
    </div>
    <div class="options-bar">
        <span class="option-selected">Data</span>\n
        <a href="/issues/'''+title+'''" style="text-decoration:none;color:black;">
        <span class="option">Issues ('''+str(n)+''')</span></a>
        <a href="/settings/'''+title+'''" style="text-decoration:none;color:black;">
        <span class="option">Settings</span></a>
        <a href="/trash/'''+title+'''" style="text-decoration:none;color:black;">
        <span class="option">Trash</span></a>
    </div>

    <div class="main-container">

      <div class="data-container">
        <div class="button-container">
          <a href="/delete/'''+title+'''" style="text-decoration: none;">
            <div class="buttons">
              <img class="icon" src="/pics/delete-folder.png">
              Delete Folder
            </div>
          </a>
          <a href="/addfolder/'''+title+'''" style="text-decoration: none;">
            <div class="buttons">
              <img class="icon" src="/pics/add-folder.png">
              Add Folder
            </div>
          </a>
          <a href="/addfile/'''+title+'''" style="text-decoration: none;">
            <div class="buttons">
              <img class="icon" src="/pics/add-file.png">
              Add File
            </div>
          </a>
          <a href="/upload/'''+title+'''" style="text-decoration: none;">
            <div class="buttons">
              <img class="icon" src="/pics/upload.png">
              Upload
            </div>
          </a>
          <a href="/download/'''+title+'''" style="text-decoration: none;">
            <div class="buttons">
              <img class="icon" src="/pics/download.png">
              Download
            </div>
          </a>
        </div>
        <div class="top-slide">'''+title+'</div>'
    n = 1
    content = os.listdir(data_folder)
    for i in content:
        if(os.path.isdir(data_folder+'/'+i)):
            if(n == len(content)):
                end += AddFolderLast(i,title)
            else:
                end += AddFolder(i,title)
        else:
            if(n == len(content)):
                end += AddFileLast(i,title)
            else:
                end += AddFile(i,title)
        n += 1

    data = ''
    try:
        with open(data_folder+'/README.md', 'r') as f:             # open and read info file
            data = f.read()
        end += '''<br><br>
            <div class="top-slide">README</div>
            <div class="readme">'''+data+'''</div>
          </div>
        </div>'''
    except:
        end += '''<br><br>
            <div class="readme-clear"></div>
            </div>
        </div>'''


    end += '''<div class="side">
      <b>About</b>
      <div class="description">
        '''+info['desc']+'''
      </div>
      <div class="line">
      </div>
      <br>
      <div class="side-title">Releases</div>'''

    for i in releases:
        with open(folder+'/Releases/'+i+'/create', 'r') as f:             # open and read info file
            date = f.read()     # convert to dictionary
        end += AddRelease(i,date,title)
    end += '''<br>
      <a class="create-r" href="/createrelease/'''+project+'''">
        Create Release +
      </a>
      <div class="line">
      </div>

    </div>
  </body>
</html>

'''
    return end

def ProjectView(title,dir=False):
    project,x = Fix(title)
    if(dir):
        root,path = Fix(title)
        folder = 'Projects/'+root
        data_folder = folder+'/Data/'+path
    else:
        folder = 'Projects/'+title
        data_folder = folder+'/Data'
    data = os.listdir(data_folder)
    releases = os.listdir(folder+'/Releases')
    info_file = folder+'/info'
    with open(info_file, 'r') as f:             # open and read info file
        info = ast.literal_eval(f.read())     # convert to dictionary
    n = len(os.listdir('Projects/'+project+'/Issues'))

    end = '''
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="/CSS/main.css">
    <div class="top-bar">
      <input class="search-bar" type="text" placeholder="Search..">
    '''
    if(user):
        end += UserPic()
    end += '''
    </div>
  </head>
  <body>
    <div class="project-top">
      <a href="/">
        <img class="title-folder" src="/pics/title-folder.png">
      </a>
      <span class="title">'''+title+'''</span>
    </div>
    <div class="options-bar">
        <span class="option-selected">Data</span>\n
    </div>

    <div class="main-container">

      <div class="data-container">
        <div class="button-container">
          </a>
          <a href="/download/'''+title+'''" style="text-decoration: none;">
            <div class="buttons">
              <img class="icon" src="/pics/download.png">
              Download
            </div>
          </a>
        </div>
        <div class="top-slide">'''+title+'</div>'
    n = 1
    content = os.listdir(data_folder)
    for i in content:
        if(os.path.isdir(data_folder+'/'+i)):
            if(n == len(content)):
                end += AddFolderLast(i,title)
            else:
                end += AddFolder(i,title)
        else:
            if(n == len(content)):
                end += AddViewFileLast(i,title)
            else:
                end += AddViewFile(i,title)
        n += 1

    data = ''
    try:
        with open(data_folder+'/README.md', 'r') as f:             # open and read info file
            data = f.read()
        end += '''<br><br>
            <div class="top-slide">README</div>
            <div class="readme">'''+data+'''</div>
          </div>
        </div>'''
    except:
        end += '''<br><br>
            <div class="readme-clear"></div>
            </div>
        </div>'''


    end += '''<div class="side">
      <b>About</b>
      <div class="description">
        '''+info['desc']+'''
      </div>
      <div class="line">
      </div>
      <br>
      <div class="side-title">Releases</div>'''

    for i in releases:
        with open(folder+'/Releases/'+i+'/create', 'r') as f:             # open and read info file
            date = f.read()     # convert to dictionary
        end += AddRelease(i,date,title)
    end += '''<br>
      <div class="line">
      </div>

    </div>
  </body>
</html>

'''
    return end

def AddRelease(name,date,project):
    end = '''
    <br>
    <a href="/releases/'''+project+'/'+name+'''" class="link">
      <img class="image" src="/pics/package.png">
      <span class="versions">'''+name+'''</span>
      <div class="version-desc">'''+date+'''</div>
    </a>'''
    return end

def AddFolder(name,project):
    end = '''
    <a href="/project/'''+project+'/'+name+'''" style="text-decoration:none;">
      <div class="slide">
        <img class="icon" src="/pics/folder.png">
        '''+name+'''
      </div>
    </a>'''
    return end

def AddFolderLast(name,project):
    end = '''
    <a href="/project/'''+project+'/'+name+'''" style="text-decoration:none;">
      <div class="last-slide">
        <img class="icon" src="/pics/folder.png">
        '''+name+'''
      </div>
    </a>'''
    return end

def AddFile(name,project):
    end = '''
    <a href="/project/edit/'''+project+'/'+name+'''" style="text-decoration:none;">
      <div class="slide">
        <img class="icon" src="/pics/file.png">
        '''+name+'''
      </div>
    </a>'''
    return end

def AddFileLast(name,project):
    end = '''
    <a href="/project/edit/'''+project+'/'+name+'''" style="text-decoration:none;">
      <div class="last-slide">
        <img class="icon" src="/pics/file.png">
        '''+name+'''
      </div>
    </a>'''
    return end

def AddViewFile(name,project):
    end = '''
    <a href="/project/view/'''+project+'/'+name+'''" style="text-decoration:none;">
      <div class="slide">
        <img class="icon" src="/pics/file.png">
        '''+name+'''
      </div>
    </a>'''
    return end

def AddViewFileLast(name,project):
    end = '''
    <a href="/project/view/'''+project+'/'+name+'''" style="text-decoration:none;">
      <div class="last-slide">
        <img class="icon" src="/pics/file.png">
        '''+name+'''
      </div>
    </a>'''
    return end

########################

def UserPic():
    end = '''
      <div class="dropdown">
        <img class="profilepic" src="/userpic/'''+str(user)+'''/profilepic.png">
        <div class="dropdown-content">
          <div class="spacer"></div>
          <div class="dropdown-box">
            <a style="text-decoration:none;" href="/profile"><div class="section">Your Profile</div></a>
            <a style="text-decoration:none;" href="/projects"><div class="section">Your Projects</div></a>
            <hr>
            <a style="text-decoration:none;" href="/settings"><div class="section">Settings</div></a>
            <a style="text-decoration:none;" href="/signout"><div class="section">Sign out</div></a>
          </div>
        </div>
      </div>'''
    return end

### Result/Main page ###

def Main():
    end = '''
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="/CSS/search.css">
    <div class="top-bar">
      <input class="search-bar" type="text" placeholder="Search..">
    '''
    if(user):
        end += UserPic()
    end += '''
    </div>
  </head>
  <div class="container">
  <a style="text-decoration:none;" href="/create">
    <div class="button">
    Create New Project
    </div>
  </a>
  <br><br>
'''

    for title in os.listdir('Projects'): # Going through projects folder to find projects to list
        info_file = 'Projects/'+title+'/info'
        with open(info_file, 'r') as f:             # open and read info file
            output = ast.literal_eval(f.read())     # convert to dictionary
        if(output['public'] != 'public'):
            continue
        date = output['created']
        desc = output['desc']
        creator = output['creator']
        end += AddResult(title,desc,date,creator)

    end += '''
    <br>
    <a style="text-decoration:none;" href="/login">
     <div class="button">
     Login
     </div>
    </a>
    <br><br>
    <a style="text-decoration:none;" href="/ca">
     <div class="button">
     Create Account
     </div>
    </a>
    <br><br>
  </div>
</html>
'''
    return end


def Projects():
    if(not user):
        return 'Need To Be Signed In'
    end = '''
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="/CSS/search.css">
    <div class="top-bar">
      <input class="search-bar" type="text" placeholder="Search..">
    '''
    if(user):
        end += UserPic()
    end += '''
    </div>
  </head>
  <div class="container">
  Your Projects<br><br>
  <a style="text-decoration:none;" href="/create">
    <div class="button">
    Create New Project
    </div>
  </a>
  <br><br>'''

    with open('Accounts/'+user+'/info','r') as f:
        data = ast.literal_eval(f.read())
    projects = data['projects']

    for title in projects: # Going through projects folder to find projects to list
        if(title == ''):
            continue
        info_file = 'Projects/'+title+'/info'
        with open(info_file, 'r') as f:             # open and read info file
            output = ast.literal_eval(f.read())     # convert to dictionary
        #if(output['public'] != 'public'):
        #    continue
        date = output['created']
        desc = output['desc']
        creator = output['creator']
        end += AddResult(title,desc,date,creator)

    end += '''
    <br>
  </div>
</html>
'''
    return end


def AddResult(title,desc,date,creator):  # add a result for search page
    end = '''
    <a href="/project/'''+title+'''" style="text-decoration: none;">
      <div class="result">
        <div class="top">
          <img class="icon" src="/pics/title-folder.png">
          <div class="title">'''+title+'''</div>
        </div>
        <div class="desc">'''+desc+'''</div>
        <div style="display:inline-flex;">
        <div class="date">'''+date+'''</div>
        <div class="creator">'''+creator+'''</div>
        </div>
      </div>
    </a><br><br>
    '''
    return end

 ####################################
