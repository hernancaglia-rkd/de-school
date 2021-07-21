#importo las librerias
import requests
import json
import os

# obtener la key que tengo guardada
token = os.environ['CURRENCY_KEY']
apikey="?access_key="+token
#base="&base=USD"
conversiones="&symbols=EUR,AUD,CAD,USD,ARS"
url ="http://api.exchangeratesapi.io/v1/latest"+apikey+conversiones 
#url ="http://api.exchangeratesapi.io/v1/latest"+apikey
print(url)
resultado=requests.get(url)
data = resultado.text
print(data)