import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
engine = create_engine('mysql+mysqlconnector://usertest:12345678@localhost/PRACTICAS3', echo=False)

# Dataset https://www.kaggle.com/zynicide/wine-reviews
#pip install mysql-connector-python

def ejecutar():
	'''
	Funcion para leer excel y cargar la data
	https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
	'''
	datos=pd.read_csv("Datos/winemag-data-130k-v2.csv")
	print(datos.shape)
	print(datos.head())
	datos.to_sql("tabla_demostracion",con=engine)
	#cnx.close()
	filas=datos.shape[0]
	return filas

if __name__ == "__main__":
	"""
	Aca ejecuta el proceso principal
	"""
	print(ejecutar())