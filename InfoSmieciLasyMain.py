from flask import Flask, jsonify, abort, make_response, request
import sqlite3
import hashlib

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
    zapytanie = "INSERT INTO wspolrzedne (lat,lng,android_id,nazwaZdjecia) VALUES ('"+lat+"','"+lng+"','"+android_id+"','"+nazwaZdjecia+"')"
    
    c = conn.cursor()
    c.execute(zapytanie)
    conn.commit()
    conn.close()
    print('dodane wspolrzedne: '+lat+' '+lng+' '+android_id+' '+nazwaZdjecia)
    return jsonify({"wynik:":"ok"})
  #else:
    #return jsonify({"sieczkaMoja: ":sieczkaMoja})
	

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)




if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
