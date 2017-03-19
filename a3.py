from flask import Flask
from boto3.session import Session
from flask import render_template, request, make_response
import os
import boto3

import requests

app= Flask(__name__)

aws_key='<your_key>'
aws_secret='<secret_key>'


session = Session(aws_access_key_id=aws_key,
                  aws_secret_access_key=aws_secret,
                  region_name='<region_name2>')

ec2 = session.resource('ec2')
s3=session.resource('s3')

my_bucket = '<bucket_name>'
#obj = s3.Bucket(my_bucket)
print('success')

itemname='login.txt'
dir_path = os.path.dirname(os.path.realpath(__file__)) + '/tmp'
print(dir_path)

fullpath=os.path.join(dir_path, itemname)
print(fullpath)

print('success')


@app.route('/')
def index():
    return render_template('a3.html')


@app.route('/login', methods=['POST'])
def login():
    loginname = request.form.get('login')
    print(loginname)
    s3.Bucket(my_bucket).download_file('login.txt', fullpath)
    print('dlood')
    with open(fullpath, 'r') as example_file:
        users = example_file.read().splitlines()
    for user in users:
        if user == loginname:
            return render_template('a3.html')
        else:
            return "<h1>User name is not valid</h1>"


port = os.getenv('VCAP_APP_PORT', '4000')



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    list_of_files = request.files.getlist('file')
    # list of files
    #print(dir2)
    tmppath = dir_path + '/'
    for f in list_of_files:
        f.save(tmppath +f.filename)
        print(f)
        print(dir_path)
        s3.Bucket(my_bucket).upload_file(tmppath+f.filename, f.filename)
        return '<h1>Upload Successful</h1>'

@app.route('/download', methods=['POST'])
def download_file():
    file_name = request.form.get('filename')
    dir_path = os.path.dirname(os.path.realpath(__file__))+'/download'
    downpath=dir_path+'/'+file_name
    s3.Bucket(my_bucket).download_file(file_name, downpath)
    return '<h1>Download Successful</h1>'

@app.route('/delete', methods=['POST'])
def delete():
    file_name = request.form['filename']
    for key in s3.Bucket(my_bucket).objects.all():
        print(key.key)
        if file_name==key.key:
            key.delete()
            return '<h1>Deleted Successfully</h1>'
        else:
            return '<h1>No key found</h1>'

@app.route('/list_files', methods=['GET', 'POST'])
def list_file():
    #bucket=s3.Bucket(my_bucket)
    for bucket in s3.buckets.all():
        for key in bucket.objects.all():
            print(key)
            #print('<h1>'+str(key)+'</h1>')
    return render_template('table.html', my_bucket=my_bucket, allbucket=s3.buckets.all(), allobj=bucket.objects.all())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port))

