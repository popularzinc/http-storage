from flask import *
import Create
import os
import shutil

app = Flask(__name__)

@app.route('/')
def main():
    return Create.Main()

@app.route('/project/<path>')
def project(path=None):
    return Create.Project(path)

@app.route('/project/<path:path>')
def project_paths(path=None):
    project,path = Create.Fix(path)
    print(project,path)
    if(os.path.isfile(path)):
        return send_file('Projects/'+path, as_attachment=True)
    else:
        return Create.Project(project+'/'+path,dir=True)

@app.route('/releases/<path:path>')
def release(path=None):
    project,path = path.split('/')
    zip = 'Projects/'+project+'/Releases/'+path+'/'+path+'.zip'
    print(zip)
    return send_file(zip, as_attachment=True)

@app.route('/createrelease/<path>',methods=['POST','GET'])
def createrelease(path=None):
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
    if request.method == 'POST':
        info = {'created':str(Create.Date()),'desc':'No Description'}
        title = request.form['title']
        folder = 'Projects/'+title
        data_folder = folder+'/Data'
        release_folder = folder+'/Releases'
        info_file = folder+'/info'
        os.mkdir(folder)
        os.mkdir(data_folder)
        os.mkdir(release_folder)
        with open(info_file,'w') as f:
            f.write(str(info))
        return redirect('/project/'+title)
    else:
        return Create.NewProject()


@app.route('/addfolder/<path:path>')
def addfolder(path=None):
    print(path)
    project,path = Create.Fix(path)
    link = '/project/'+project+'/'+path
    if(link.endswith('/')):
        link = link[:-1]
    folder = 'Projects/'+project+'/Data/'+path
    if(folder.endswith('/')):
        folder = folder[:-1]
    n = 0
    name = folder+'/New Folder '+str(n)
    while(os.path.isdir(name)):
        name = folder+'/New Folder '+str(n)
        n += 1
    print(name)
    os.mkdir(name)
    return redirect(link)

@app.route('/upload/<path:path>',methods=['POST','GET'])
def upload(path=None):
    if request.method == 'POST':
        back = '/project/'+path
        project,folder = Create.Fix(path)
        path = 'Projects/'+project+'/Data/'+folder
        if(path.endswith('/')):
            path = path[:-1]
        files = request.files.getlist("data")
        print(files)
        for file in files:
            file.save(os.path.join(path, file.filename))
        return redirect(back)
    else:
        return Create.Upload(path)


@app.route('/addfile/<path:path>')
def addfile(path=None):
    project,path = Create.Fix(path)
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
    return redirect(link)

@app.route('/delete/<path:path>',methods=['POST','GET'])
def delete(path=None):
    project,path = Create.Fix(path)
    back = ''
    n = 0
    for i in path.split('/'):
        n += 1
        if(n == len(path.split('/'))):
            break
        back += i+'/'
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
                os.rmdir(file)
            except:
                pass
    else:
        os.remove(file)
    return redirect(back)


@app.route('/project/edit/<path:path>',methods=['POST','GET'])
def edit(path):
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
        print('L : '+link)
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
        return redirect(link)
    else:
        return Create.Edit(path)

@app.route('/downloadfile/<path:path>')
def downloadfile(path=None):
    #Solar Charger/folder1/folder2
    project,file = Create.Fix(path)
    file_path = 'Projects/'+project+'/Data/'+file
    if(file_path.endswith('/')):
        file_path = file_path[:-1]
    print(file_path)
    return send_file(file_path,as_attachment=True)

@app.route('/download/<path:path>')
def downloadfolder(path=None):
    #Solar Charger/folder1/folder2
    name = path.split('/')[-1]
    project,folder = Create.Fix(path)
    zip_folder = 'Projects/'+project
    path = 'Projects/'+project+'/Data/'+folder
    if(path.endswith('/')):
        path = path[:-1]
    shutil.make_archive(zip_folder+'/'+name, 'zip', path)
    return send_file(zip_folder+'/'+name+'.zip',as_attachment=True)

@app.route('/CSS/<path>')
def CSS(path=None):
    return send_file('CSS/'+path, as_attachment=True)

@app.route('/pics/<path>')
def pics(path=None):
    return send_file('Pics/'+path, as_attachment=True)

app.run(host='0.0.0.0',port=5555)
