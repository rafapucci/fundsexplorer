import requests
import json
import csv
from bs4 import BeautifulSoup
from datetime import datetime
from classes.url import *
from classes.user import User
from classes.fund import Fund

def GetFundId(fund):
   with open('config/funds.csv') as f:
      return dict(csv.reader(f)).get(fund)

def GetUserCsrfToken(page):
   soup = BeautifulSoup(page, 'lxml')
   return soup.select_one('meta[name="csrf-token"]')['content']

def ReadUserFile(path):
   js = json.loads(open(path).read())
   user = User(js['user'],js['password'],js['wallet'])
   return user

def Login(user):
   session = requests.Session()
   request = session.get(URL_BASE+URL_LOGIN)

   headers = {
      'authority': 'www.fundsexplorer.com.br',
      'accept': '*/*',
      'x-csrf-token': GetUserCsrfToken(request.text),
      'x-requested-with': 'XMLHttpRequest',
      'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'origin': URL_BASE,
      'sec-fetch-site': 'same-origin',
      'sec-fetch-mode': 'cors',
      'sec-fetch-dest': 'empty',
      'referer': URL_BASE,
      'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
   }

   data = {
      'user[email]': user.user,
      'user[password]': user.password
   }

   response = session.post(URL_BASE+URL_LOGIN, headers=headers, data=data)
   if json.loads(response.text)['success']:
      return session

def AddNewFund(session, wallet, fund):
   request = session.get('https://www.fundsexplorer.com.br/carteiras/{}'.format(wallet))
   headers = {
      'authority': 'www.fundsexplorer.com.br',
      'accept': '*/*',
      'x-csrf-token': GetUserCsrfToken(request.text),
      'x-requested-with': 'XMLHttpRequest',
      'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'origin': URL_BASE,
      'sec-fetch-site': 'same-origin',
      'sec-fetch-mode': 'cors',
      'sec-fetch-dest': 'empty',
      'referer': URL_BASE,
      'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
   }
   
   data = {
      'fund_id': GetFundId(fund.fund),
      'operation_type': fund.operation_type,
      'quantity': fund.quantity,
      'price': fund.price,
      'taxes': fund.taxes,
      'date': fund.date
   }

   if session.post('https://www.fundsexplorer.com.br/carteiras/{}/add-operation'.format(wallet),headers=headers, data=data).status_code == 200:
      return True

def ReadFileFund(path):
   with open(path, mode='r',encoding='utf-8') as csv_file:
      csv_reader = csv.DictReader(csv_file, delimiter=';',
         fieldnames=("codigo","ativo","tipo","natureza","status","preco","stop","gain","quantidade","qtd.executada","precomedio","criadoem","modulo","estrategia","criadopor","validade","canceladaem","canceladapor","atualizadoem"))
      next(csv_reader)
      line_count = 0
      
      for row in csv_reader:
         
         #only for debug
         print(
            row['ativo'] + ' - ' +
            row['natureza'] + ' - ' + 
            row['quantidade'] + ' - ' + 
            row['precomedio'] + ' - ' + 
            str(datetime.strptime(row['criadoem'], '%d/%m/%Y %H:%M:%S').date())
            #row['criadoem']
         )
         
         fund = Fund(
         row['ativo'],
         row['natureza'],
         row['quantidade'],
         row['precomedio'],0,
         str(datetime.strptime(row['criadoem'], '%d/%m/%Y %H:%M:%S').date()))
         print(AddNewFund(session, user.wallet,fund))
         line_count += 1
      print('Processed {} funds.'.format(line_count))

if __name__ == "__main__":
   user = ReadUserFile('config/user.json')
   session = Login(user)
   ReadFileFund('orders/orders.csv')