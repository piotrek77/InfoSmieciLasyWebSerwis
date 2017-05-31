from flask import Flask, jsonify, abort, make_response, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import sqlite3
import hashlib
import os


UPLOAD_FOLDER = '/home/piotrek/py'
ALLOWED_EXTENSIONS  =set(['txt','pdf','png','jpg','jpeg','gif'])

conn = sqlite3.connect('InfoSmieciLasyDB.db')
app = Flask(__name__)

tasks = [
{'id':1, 'imie':'Jan', 'nazwisko':'Kowalski'},
{'id':2, 'imie':'Alicja','nazwisko':'Nowak'}
]



@app.route('/')
def index():
  return 'Hello, World!'

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
  task = [task for task in tasks if task['id'] == task_id]
  if len(task) == 0:
    abort(404)
  return jsonify({'task':task[0]})

@app.route('/dodaj', methods=['GET'])
def get_dodaj():
#http://stackoverflow.com/questions/24892035/python-flask-how-to-get-parameters-from-a-url
  lat = request.args.get('lat')
  lng = request.args.get('lng')
  android_id = request.args.get('android_id')
  nazwaZdjecia = request.args.get('nazwaZdjecia')
  sieczka = request.args.get('sieczka')
  dokladnosc = request.args.get('dokladnosc')
  #sprawdzamy czy sieczka gra
  conn = sqlite3.connect('InfoSmieciLasyDB.db')
  #zapytanie = "SELECT token FROM tokeny WHERE urzadzenie_id ='"+urzadzenie_id+"'"
  #c = conn.cursor()
  #c.execute(zapytanie)
  #try:
  #  token = c.fetchone()[0] #executesccalar
  #except:
  #  token = ''
  
  #if len(token)==0:
  #  abort(404)
  
  #zlepek = urzadzenie_id+telefon+kierunek+klient+token
  
  #sieczkaMoja = hashlib.md5( zlepek.encode('UTF-8')).hexdigest()
  
  
  #if sieczka gra
  if 1==1:#sieczka==sieczkaMoja:
    zapytanie = "INSERT INTO wspolrzedne (lat,lng,android_id,nazwaZdjecia, dokladnosc) VALUES ('"+lat+"','"+lng+"','"+android_id+"','"+nazwaZdjecia+"','"+dokladnosc+"')"
    
    c = conn.cursor()
    c.execute(zapytanie)
    conn.commit()
    conn.close()
    print('dodane wspolrzedne: '+lat+' '+lng+' '+android_id+' '+nazwaZdjecia)
    return jsonify({"wynik:":"ok"})
  #else:
    #return jsonify({"sieczkaMoja: ":sieczkaMoja})


@app.route('/file')
def getfile():
  print('Hello file')
  return send_file('README.md')

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/fileput', methods=['GET','POST'])
def upload_file():
  if request.method == 'POST':
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save( os.path.join(app.config['UPLOAD_FOLDER'], filename))
#      return redirect(url_for('uploaded_file', filename = filename))
      print('ok')
  return '''
  <!doctype html>
  <title>test</title>
  <h1>Upload new file</h1>
  <form method=post enctype=multipart/form-data>
  <p><input type=file name=file>
  <input type=submit value=Upload>
  </form>
  '''



@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)







#app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
