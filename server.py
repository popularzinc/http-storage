from flask import *
import Create
import os
import shutil
import ast
import Accounts

app = Flask(__name__)

allowed = ['192.168.1.14','192.168.1.11']

@app.before_request
def bfr():
    try:
        session['user']
        Create.user = session['user']
    except:
        session['user'] = False
    if(str(request.remote_addr) not in allowed):
        print(str(request.remote_addr)+' Blocked')
        return str(request.remote_addr)+' <b>Blocked</b>'

def NotAllowed():
    return '<b>Not Allowed</b>'

def LoggedIn():
    if(session['user'] != None):
        return True
    return False
def Allowed(project):
    info = Create.Info(project)
    if(not LoggedIn()):
        return False
    if(info['creator'] == session['user']):
        return True
    return False

def Public(project):
    if(Create.Info(project)['public'] == 'public'):
        return True
    return False

@app.route('/user/<user>')
def login_(user=None):
    session['user'] = user
    Create.user = user
    Accounts.Create(user,'password')
    return redirect('/')

@app.route('/login',methods=['POST','GET'])
def login():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        if(Accounts.Login(username,password)):
            session['user'] = username
            Create.user = username
            return redirect('/')
        else:
            return 'Login Failed'

    return Create.Login()

@app.route('/ca',methods=['POST','GET'])
def ca():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        Accounts.Create(username,password)
        session['user'] = username
        return redirect('/')

    return Create.CreateAccount()

@app.route('/')
def main():
    return Create.Main()

@app.route('/projects')
def projects():
    return Create.Projects()

@app.route('/project/<path>')
def project(path=None):
    if(Allowed(path)):
        return Create.Project(path)
    elif(Public(path)):
        return Create.ProjectView(path)
    else:
        return NotAllowed()

@app.route('/project/view/<path:path>')
def project_paths_view(path=None):
    return Create.View(path)

@app.route('/project/<path:path>')
def project_paths(path=None):
    project,path = Create.Fix(path)
    if(Allowed(project)):
        if(os.path.isfile(path)):
            return send_file('Projects/'+path, as_attachment=True)
        else:
            return Create.Project(project+'/'+path,dir=True)
    elif(Public(project)):
        if(os.path.isfile(path)):
            return send_file('Projects/'+path, as_attachment=True)
        else:
            return Create.ProjectView(project+'/'+path,dir=True)
    else:
        return NotAllowed()

@app.route('/releases/<path:path>')
def release(path=None):
    project,path = path.split('/')
    if not (Allowed(project) or Public(project)):
        return NotAllowed()
    zip = 'Projects/'+project+'/Releases/'+path+'/'+path+'.zip'
    return send_file(zip, as_attachment=True)

@app.route('/createrelease/<path>',methods=['POST','GET'])
def createrelease(path=None):
    if(not Allowed(path)):
        return NotAllowed()
    if request.method == 'POST':
        info = str(Create.Date())
        title = request.form['title']
        folder = 'Projects/'+path
        release_folder = folder+'/Releases'
        release = release_folder+'/'+title
        os.mkdir(release)
        create_file = release+'/create'
        with open(create_file,'w') as f:
            f.write(str(info))
        shutil.make_archive(release+'/'+title, 'zip', folder+'/Data')
        return redirect('/project/'+path)
    else:
        return Create.NewRelease()

@app.route('/create',methods=['POST','GET'])
def create():
    if(not LoggedIn()):
        return 'Must Be Logged In'
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        info = {'created':str(Create.Date()),'desc':desc,'public':'','backup':'backup','creator':session['user']}
        folder = 'Projects/'+title
        data_folder = folder+'/Data'
        release_folder = folder+'/Releases'
        info_file = folder+'/info'
        readme_file = data_folder+'/README.md'
        trash = folder+'/Trash'
        issue_folder = folder+'/Issues'
        comissue_folder = folder+'/ComIssues'
        os.mkdir(folder)
        os.mkdir(trash)
        os.mkdir(data_folder)
        os.mkdir(issue_folder)
        os.mkdir(comissue_folder)
        os.mkdir(release_folder)
        with open(info_file,'w') as f:
            f.write(str(info))
        with open(readme_file,'w') as f:
            f.write('Read Me')
        ## add to user
        user = session['user']
        add = str(title)
        with open('Accounts/'+user+'/info', 'r') as f:
            info = ast.literal_eval(f.read())
        old_projects = info['projects']
        old_projects.append(add)
        info['projects'] = old_projects
        with open('Accounts/'+user+'/info', 'w') as f:
            f.write(str(info))
        return redirect('/project/'+title)
    else:
        return Create.NewProject()

@app.route('/trash/<path>')
def trash(path=None):
    if(not Allowed(path)):
        return NotAllowed()
    return Create.Trash(path)

@app.route('/addfolder/<path:path>',methods=['POST','GET'])
def addfolder(path=None):
    project,path = Create.Fix(path)
    if(not Allowed(project)):
        return NotAllowed()
    if request.method == 'POST':
        link = '/project/'+project+'/'+path
        if(link.endswith('/')):
            link = link[:-1]
        folder = 'Projects/'+project+'/Data/'+path
        if(folder.endswith('/')):
            folder = folder[:-1]
        n = 0
        title = request.form['name']
        name = folder+'/'+title
        os.mkdir(name)
        Create.Backup(project)
        return redirect(link)
    else:
        project,path = Create.Fix(path)
        title = project+'/'+path
        if(title.endswith('/')):
            title = title[:-1]
        return Create.NewFolder(title)

@app.route('/upload/<path:path>',methods=['POST','GET'])
def upload(path=None):
    project,folder = Create.Fix(path)
    if(not Allowed(project)):
        return NotAllowed()
    if request.method == 'POST':
        back = '/project/'+path
        project,folder = Create.Fix(path)
        path = 'Projects/'+project+'/Data/'+folder
        if(path.endswith('/')):
            path = path[:-1]
        files = request.files.getlist("data")
        for file in files:
            file.save(os.path.join(path, file.filename))
        Create.Backup(project)
        return redirect(back)
    else:
        return Create.Upload(path)

@app.route('/createissue/<path>',methods=['POST','GET'])
def create_issue(path=None):
    if(not Allowed(path)):
        return NotAllowed()
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        Create.CreateIssue(path,title,desc)
        return redirect('/issue/'+path+'/'+title)
    return Create.CreateIssues(path)

@app.route('/deleteissue/<path:path>',methods=['POST','GET'])
def deleteissue(path=None):
    project,path = Create.Fix(path)
    if(not Allowed(project)):
        return NotAllowed()
    if request.method == 'POST':
        name = request.form['name']
        if(name == path):
            os.remove('Projects/'+project+'/Issues/'+path)
            return redirect('/project/'+project)
        else:
            return redirect('/issue/'+project+'/'+path)
    else:
        return redirect('/issue/'+project+'/'+path)

@app.route('/deletecomissue/<path:path>',methods=['POST','GET'])
def comdeleteissue(path=None):
    project,path = Create.Fix(path)
    if(not Allowed(project)):
        return NotAllowed()
    if request.method == 'POST':
        name = request.form['name']
        if(name == path):
            os.remove('Projects/'+project+'/ComIssues/'+path)
            return redirect('/project/'+project)
        else:
            return redirect('/comissue/'+project+'/'+path)
    else:
        return redirect('/comissue/'+project+'/'+path)

@app.route('/issues/<path:path>',methods=['POST','GET'])
def issues(path=None):
    project,path = Create.Fix(path)
    if(not Allowed(project)):
        return NotAllowed()
    return Create.Issues(project)

@app.route('/issue/<path:path>',methods=['POST','GET'])
def issue(path=None):
    project,path = Create.Fix(path)
    if(not Allowed(project)):
        return NotAllowed()
    if request.method == 'POST':
        done = False
        done = request.form.getlist('done')
        if(done == 'done'):
            done = True
        old_file = 'Projects/'+path.split('/')[0]+'/Issues/'+path.split('/')[1]
        end_files = os.listdir('Projects/'+path.split('/')[0]+'/Data')
        with open(old_file,'r') as f:
            data = ast.literal_eval(f.read())
            start_date = data['start_date']
            start_files = ast.literal_eval(data['start_files'])
        os.remove(old_file)
        title = request.form['title']
        file_path = 'Projects/'+path.split('/')[0]+'/Issues/'+title
        desc = request.form['desc']
        data = request.form['data']
        file = request.form['file']
        code1 = request.form['code1']
        code2 = request.form['code2']
        variables = {
        'desc':desc,
        'data':data,
        'start_date':start_date,
        'end_date':Create.Date(),
        'start_files':str(start_files),
        'end_files':str(end_files),
        'file':file,
        'code1':code1,
        'code2':code2
        }
        with open(file_path,'w') as f:
            f.write(str(variables))
        if(done):
            shutil.move(file_path,'Projects/'+path.split('/')[0]+'/ComIssues/'+title)
            return redirect('/comissue/'+path)
        else:
            return redirect('/issue/'+path)
    return Create.Issue(path)

@app.route('/comissue/<path:path>',methods=['POST','GET'])
def comissue(path=None):
    project,path = Create.Fix(path)
    if(not Allowed(project)):
        return NotAllowed()
    return Create.ComIssue(path)

@app.route('/settings/<path>',methods=['POST','GET'])
def settings(path=None):
    if(not Allowed(path)):
        return NotAllowed()
    if request.method == 'POST':
        b = False
        new_name = path
        new_name = request.form['name']
        new_desc = request.form['desc']
        public = request.form.getlist('public')
        backup = request.form.getlist('backup')
        if('backup' in backup):
            backup = 'backup'
        else:
            backup = ''
        if('public' in public):
            public = 'public'
        else:
            public = ''
        file = 'Projects/'+path+'/info'
        with open(file,'r') as f:
            data = ast.literal_eval(f.read())
        if(backup == 'backup'):
            b = True
        data['desc'] = new_desc
        data['public'] = public
        data['backup'] = backup

        with open(file,'w') as f:
            f.write(str(data))
        os.rename('Projects/'+path, 'Projects/'+new_name)
        if(b):
            Create.Backup(new_name)
        return redirect('/settings/'+new_name)
    return Create.Settings(path)


@app.route('/addfile/<path:path>')
def addfile(path=None):
    project,path = Create.Fix(path)
    if(not Allowed(project)):
        return NotAllowed()
    link = '/project/'+project+'/'+path
    if(link.endswith('/')):
        link = link[:-1]
    folder = 'Projects/'+project+'/Data/'+path
    if(folder.endswith('/')):
        folder = folder[:-1]
    n = 0
    name = folder+'/New File '+str(n)
    while(os.path.isfile(name)):
        name = folder+'/New File '+str(n)
        n += 1
    with open(name, 'w') as f:
        f.write('')
    Create.Backup(project)
    return redirect(link)

@app.route('/delete/<path:path>',methods=['POST','GET'])
def delete(path=None):
    project,path = Create.Fix(path)
    if(not Allowed(project)):
        return NotAllowed()
    back = ''
    n = 0
    for i in path.split('/'):
        n += 1
        if(n == len(path.split('/'))):
            break
        back += i+'/'
    file_name = back[:-1]
    back = '/project/'+project+'/'+back[:-1]
    if(back.endswith('/')):
        back = back[:-1]
    file = 'Projects/'+project+'/Data/'+path
    if(file.endswith('/')):
        file = file[:-1]
    if(os.path.isdir(file)):
        if(len(file.split('/')) < 4):
            pass
        else:
            try:
                shutil.make_archive('Projects/'+project+'/Trash/'+path,'zip',file)
                shutil.rmtree(file)
            except:
                pass
    else:
        os.rename(file,'Projects/'+project+'/Trash/'+path)
    return redirect(back)


@app.route('/deleteproject/<path>',methods=['POST','GET'])
def delproject(path=None):
    if(not Allowed(path)):
        return NotAllowed()
    if(request.method == 'POST'):
        print(request.form['data'])
        if(request.form['data'] == path):
            try:
                #shutil.make_archive('Deleted/deletedproject_'+path,'zip','Projects/'+path)
                shutil.rmtree('Projects/'+path)
                with open('Accounts/'+session['user']+'/info', 'r') as f:
                    info = ast.literal_eval(f.read())
                new = []
                for i in info['projects']:
                    if(i != path):
                        new.append(i)
                info['projects'] = new
                with open('Accounts/'+session['user']+'/info', 'w') as f:
                    f.write(str(info))
                return redirect('/')
            except Exception as e:
                print(e)
                return redirect('/project/'+path)
        else:
            return redirect('/project/'+path)
    else:
        return redirect('/project/'+path)


@app.route('/project/edit/<path:path>',methods=['POST','GET'])
def edit(path=None):
    project,path = Create.Fix(path)
    if(not Allowed(project)):
        return NotAllowed()
    if(request.method == 'POST'):
        link = ''
        n = 0
        for i in path.split('/'):
            n += 1
            if(n == len(path.split('/'))):
                #link += name+'/'
                break
            link += i+'/'
        link = '/project/edit/'+link
        project,path = Create.Fix(path)
        old_name = path.split('/')[-1]
        title = request.form['title']
        if(title.strip() == ''):
            name = old_name
        else:
            name = title
        link = link+name
        path = 'Projects/'+project+'/Data/'+path
        try:
            data = request.form['data']   # if no data or textarea, aka  a photo, then just save title
        except:
            with open(path, 'rb') as f:
                data = f.read()

        os.remove(path)
        file = ''
        n = 0
        for i in path.split('/'):
            n += 1
            if(n == len(path.split('/'))):
                file += name+'/'
                break
            file += i+'/'
        file = file[:-1]
        Create.SaveFile(file,data)
        Create.Backup(project)
        return redirect(link)
    else:
        return Create.Edit(path)

@app.route('/downloadfile/<path:path>')
def downloadfile(path=None):
    #Solar Charger/folder1/folder2
    project,file = Create.Fix(path)
    if not (Allowed(project) or Public(project)):
        return NotAllowed()
    file_path = 'Projects/'+project+'/Data/'+file
    if(file_path.endswith('/')):
        file_path = file_path[:-1]
    return send_file(file_path,as_attachment=True)

@app.route('/userpic/<path:path>')
def userpic(path=None):
    return send_file('Accounts/'+path,as_attachment=True)

@app.route('/cleartrash/<path:path>')
def cleartrash(path=None):
    if(not Allowed(path)):
        return NotAllowed()
    for i in os.listdir('Projects/'+path+'/Trash'):
        file = 'Projects/'+path+'/Trash/'+str(i)
        os.remove(file)
    return redirect('/trash/'+path)

@app.route('/deletetrash/<path:path>')
def deletetrash(path=None):
    project,file = Create.Fix(path)
    if(not Allowed(project)):
        return NotAllowed()
    os.remove('Projects/'+project+'/Trash/'+file)
    return redirect('/trash/'+project)

@app.route('/downloadtrash/<path:path>')
def downloadtrash(path=None):
    #Solar Charger/folder1/folder2
    project,file = Create.Fix(path)
    if(not Allowed(project)):
        return NotAllowed()
    file_path = 'Projects/'+project+'/Trash/'+file
    if(file_path.endswith('/')):
        file_path = file_path[:-1]
    return send_file(file_path,as_attachment=True)

@app.route('/download/<path:path>')
def downloadfolder(path=None):
    #Solar Charger/folder1/folder2
    name = path.split('/')[-1]
    project,folder = Create.Fix(path)
    if not (Allowed(project) or Public(project)):
        return NotAllowed()
    zip_folder = 'Projects/'+project
    path = 'Projects/'+project+'/Data/'+folder
    if(path.endswith('/')):
        path = path[:-1]
    shutil.make_archive(zip_folder+'/'+name, 'zip', path)
    return send_file(zip_folder+'/'+name+'.zip',as_attachment=True)

@app.route('/CSS/<path>')
def CSS(path=None):
    return send_file('Pages/'+path, as_attachment=True)

@app.route('/pics/<path>')
def pics(path=None):
    return send_file('Pics/'+path, as_attachment=True)

app.secret_key = os.urandom(24)
app.run(host='0.0.0.0',port=5555)
