import sqlite3
import random
import string

conn = sqlite3.connect('InfoSmieciLasyDB.db')



def LosujToken(size = 6, chars = string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))


def help():
  print('exit - wyjście z programu')
  print('u - lista uzytkownikow')
  print('u+ - dodaj uzytkownika')
  print('t - lista tokenow')
  print('t+ - dodaj token')
  print('w - wspolrzedne')

def tokeny():
  u = input('Podaj id uzytkownika: ')
  try:
    uint = int(u)
  except:
    print('Trzeba bylo liczbe podac')
    return;
  zapytanie = 'SELECT t.id, t.token, t.urzadzenie_nazwa from tokeny as t join uzytkownicy as u on t.uzytkownicy_id = u.id WHERE u.id=' +str(uint)+' order by t.id'
  c = conn.cursor()  
  for rowek in c.execute(zapytanie):
    print(rowek)
  c.close()


def dodajToken():
  u = input('Podaj id uzytkownika: ')
  try:
    uint = int(u)
  except:
    print('Trzeba bylo podac liczbe')
    return;
  tel = input('Podaj nr telefonu: ')
  token = LosujToken(size=30)
  zapytanie = "INSERT INTO tokeny (uzytkownicy_id, token, urzadzenie_nazwa) VALUES( "+str(uint)+", '"+token+"','"+tel+"' )"
  c = conn.cursor()
  c.execute(zapytanie)
  c.close()


def uzytkownicy():
  zapytanie = 'select * from uzytkownicy order by nazwa'
  c = conn.cursor()
  for rowek in c.execute(zapytanie):
    print(rowek)
  c.close()

def dodajUzytkownika():
  nazwa = input('Nazwa nowego uzytkownika: ')
  haslo = input('Haslo nowego uzytkownika: ')
  print('Czy na pewno dodac nowego uzytkownika? ')
  odp = input('T/N ')
  if odp == 'T' or odp == 't':
    c = conn.cursor()
    params = (nazwa, haslo)
    c.execute('INSERT INTO uzytkownicy (nazwa, haslo) VALUES (?,?)', params)
    c.close()


def wspolrzedne():
 zapytanie = "select * from wspolrzedne"
 c = conn.cursor()
 for rowek in c.execute(zapytanie):
   print(rowek)
 c.close()
 
opcje = {
'help' : help,
'u' : uzytkownicy,
'u+' : dodajUzytkownika,
't' : tokeny,
't+' : dodajToken,
'w' : wspolrzedne
}


def main():
  polecenie = '';
  

  while True:
    
    polecenie = input('>>')

    if polecenie in opcje:
      opcje[polecenie]()
    else:
      help()

  
    if polecenie == 'exit':
      conn.commit()
      conn.close()
      break












main()
