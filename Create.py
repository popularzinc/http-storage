import ast
import os
from datetime import date

def Fix(path):
    end = ''
    project = path.split('/')[0]
    new = path.split('/')
    for i in new[1:]:
        end += i+'/'
    return project,end[:-1]


### UPLOAD #####

def Upload(path):
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
      <img class="title-folder" src="/pics/title-folder.png">
      <span class="title">'''+path+'''</span>
    </div>
    <div class="options-bar">
      <span class="option-selected">Data</span>
      <span class="option">Settings</span>
    </div>
    <div class="container">
      <form action="/upload/'''+path+'''" method="POST" enctype="multipart/form-data">
        <input type="file" name="data" multiple="">
        <input class="button" type="submit" value="Upload">
      <form>
    </div>
  </body>
</html>
'''
    return end

def Date():
    return date.today().strftime("%B %d, %Y")

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
      <img class="title-folder" src="/pics/title-folder.png">
      <span class="title">Create New Project</span>
    </div>
    <div class="options-bar">
      <span class="option-selected">Data</span>
      <span class="option">Settings</span>
    </div>
    <div class="container">
      <form action="/create" method="POST">
        <input type="text" name="title" placeholder="Title">
        <input class="button" type="submit" value="Create">
      <form>
    </div>
  </body>
</html>
'''
    return end

def NewRelease():
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
      <img class="title-folder" src="/pics/title-folder.png">
      <span class="title">Create New Release</span>
    </div>
    <div class="options-bar">
      <span class="option-selected">Data</span>
      <span class="option">Settings</span>
    </div>
    <div class="container">
      <form method="POST">
        <input type="text" name="title" placeholder="Title">
        <input class="button" type="submit" value="Create">
      <form>
    </div>
  </body>
</html>
'''
    return end

#####################



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
    end = '''<!DOCTYPE html>
    <html>
      <head>
        <link rel="stylesheet" href="/CSS/edit.css">
        <div class="top-bar">
          <input class="search-bar" type="text" placeholder="Search..">
        </div>
      </head>
      <body>
        <div class="project-top">
          <img class="title-folder" src="/pics/title-folder.png">
          <span class="title">'''+project+'''</span>
        </div>
        <div class="options-bar">
          <span class="option-selected">Data</span>
          <span class="option">Settings</span>
        </div>
        <div class="container">
          <a href="/delete/'''+project+'/'+path+'''" style="text-decoration:none;">
            <div class="delete-button">Delete</div><br>
          </a>
          <form method="POST">
            <div class="msg">Editing, '''+name+'''</div><br>
            <input class="button" type=submit value="Save"><br><br>
            <input name="title" class="title-input" type="text" placeholder="'''+name+'''"><br><br>'''
    if(binary):
        end += '''<img class="image" src="/downloadfile/'''+project+'/'+path+'''">'''
    else:
        end += '''<textarea name="data" class="desc-input" type="text" placeholder="Data in file..">'''+data+'''</textarea><br><br>'''

    end += '''</form>
        </div>
      </body>
    </html>'''
    return end



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

    end = '''
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="/CSS/main.css">
    <div class="top-bar">
      <input class="search-bar" type="text" placeholder="Search..">
    </div>
  </head>
  <body>
    <div class="project-top">
      <img class="title-folder" src="/pics/title-folder.png">
      <span class="title">'''+title+'''</span>
    </div>
    <div class="options-bar">
      <span class="option-selected">Data</span>
      <a href="/settings/'''+project+'''" style="text-decoration:none;">
        <span class="option">Settings</span>
      </a>
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
        <br><br>
        <div class="top-slide">'''+title+'</div>'

    for i in os.listdir(data_folder):
        if(os.path.isdir(data_folder+'/'+i)):
            end += AddFolder(i,title)
        else:
            end += AddFile(i,title)

    data = ''
    try:
        with open(data_folder+'/README.md', 'r') as f:             # open and read info file
            data = f.read()
    except:
        pass
    end += '''<br><br>
        <div class="top-slide">README</div>
        <div class="readme">'''+data+'''</div>
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

def AddFile(name,project):
    end = '''
    <a href="/project/edit/'''+project+'/'+name+'''" style="text-decoration:none;">
      <div class="slide">
        <img class="icon" src="/pics/file.png">
        '''+name+'''
      </div>
    </a>'''
    return end

########################

### Result/Main page ###

def Main():
    end = '''
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="/CSS/search.css">
    <div class="top-bar">
      <input class="search-bar" type="text" placeholder="Search..">
    </div>
  </head>
  <div class="container">'''

    for title in os.listdir('Projects'): # Going through projects folder to find projects to list
        info_file = 'Projects/'+title+'/info'
        with open(info_file, 'r') as f:             # open and read info file
            output = ast.literal_eval(f.read())     # convert to dictionary
        date = output['created']
        desc = output['desc']
        end += AddResult(title,desc,date)

    end += '''
    <br>
    <a href="/create">Create New Project</a>
  </div>
</html>
'''
    return end


def AddResult(title,desc,date):  # add a result for search page
    end = '''
    <a href="/project/'''+title+'''" style="text-decoration: none;">
      <div class="result">
        <div class="top">
          <img class="icon" src="/pics/title-folder.png">
          <div class="title">'''+title+'''</div>
        </div>
        <div class="desc">'''+desc+'''</div>
        <div class="date">'''+date+'''</div>
      </div>
    </a><br>
    '''
    return end

 ####################################
