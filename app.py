from flask import Flask, render_template, request, Response, redirect, url_for
from models.grayimg import GrayImg
from models.histogram import Histogram
from werkzeug.utils import secure_filename
# from camera import Camera
# import models.imggray as ig
from random import randint
import os
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "daxiong"


@app.route('/')
def index():
    return render_template('index.html')
    #return redirect(url_for('grayimg'))


@app.route('/grayimg', methods=('GET', 'POST'))
def grayimg():
    form = GrayImg()
    org_name = ''
    filename = ''
    if request.args.get('action'):
        filename = request.args.get('name')
        if request.args.get('action') == "gr1":
            org_name = os.path.join('static', 'photos', '_1' + filename)
        elif request.args.get('action') == "gr2":
            org_name = os.path.join('static', 'photos', '_2' + filename)
        elif request.args.get('action') == "orgin":
            org_name = os.path.join('static', 'photos', filename)

    if form.validate_on_submit():
        # delete old file
        for file in os.scandir(os.path.join(app.static_folder, 'photos')):
            os.unlink(file.path)

        f = form.photo.data
        filename = secure_filename(f.filename)
        ext = filename.rsplit(".", 1)[1]
        filename = str(randint(1000000000, 9999999999)) + '.' + ext
        f.save(os.path.join(app.static_folder, 'photos', filename))
        org_name = os.path.join('static', 'photos', filename)

        form.covertogray(os.path.join(app.static_folder, 'photos/'), filename)
    return render_template('grayimg.html', form=form, org_name=org_name, filename=filename)


@app.route('/histogram', methods=('GET', 'POST'))
def histogram():
    org_name = ''
    graph_img = ''
    filename = ''
    covert_name=''
    form = Histogram()
    if request.args.get('action') and request.args.get('name'):
        filename = request.args.get('name')
        action = request.args.get('action')
        org_name =request.args.get('org_name')
        list = request.args.get('list')
        covert_name=filename
        graph_img = form.htg(os.path.join(app.static_folder, 'photos/'), filename, action)
    else:
        action = 3
        list=''
    if request.args.get('list') and request.args.get('org_name'):
        filename = request.args.get('org_name')
        org_name =request.args.get('org_name')
        list = request.args.get('list')
        if list!='3':
            covert_name = form.covertoimg(os.path.join(app.static_folder, 'photos/'), filename, list)
        else:
            covert_name=org_name
        graph_img = form.htg(os.path.join(app.static_folder, 'photos/'), covert_name, action)
    if form.validate_on_submit():
        # delete old file
        for file in os.scandir(os.path.join(app.static_folder, 'photos')):
            os.unlink(file.path)
        f = form.photo.data
        filename = secure_filename(f.filename)
        ext = filename.rsplit(".", 1)[1]
        filename = str(randint(1000000000, 9999999999)) + '.' + ext
        f.save(os.path.join(app.static_folder, 'photos', filename))
        #org_name = os.path.join('static', 'photos', filename)
        org_name=filename
        covert_name=filename
        graph_img = form.htg(os.path.join(app.static_folder, 'photos/'), filename, action=3)

    return render_template('histogram.html',
                           form=form,
                           org_name=org_name,
                           graph_img=graph_img,
                           covert_name=covert_name,
                           list=list,
                           action=action)


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True, threaded=True, host='192.168.159.128', port=2020)
