import beanstalkc
import json
import base64
from pprint import pprint
from datetime import datetime
import os
import sqlite3
import base64
import requests

beanstalkc = beanstalkc.Connection(host='localhost',port=11300)
TUBE_NAME='alprd'

print(beanstalkc.tubes())

# try:
# 	pprint(beanstalkc.stats_tube(TUBE_NAME))
# except beanstalkc.CommandFailed:
# 	print("Tube doesn't exist")


beanstalkc.watch(TUBE_NAME)

pNumber = None
pCoordinates = None
pColor = None
pVehicleType = None

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'vehicles.db')

def db_connect(db_path=DEFAULT_PATH):
    connection = sqlite3.connect(db_path)
    return connection

def create_table():
	con = db_connect()
	cur = con.cursor()
	vehicles_sql = """
	CREATE TABLE IF NOT EXISTS vehicles (
		ID INTEGER PRIMARY KEY AUTOINCREMENT,
		NumberPlate text NOT NULL,
		Coordinates text NOT NULL,
		Color text NOT NULL,
		Vehicle text NOT NULL,
		Image text NOT NULL,
		TimeDate text NOT NULL)"""
	cur.execute(vehicles_sql)

def insert_data(number,Coordinates,Color,Vehicle,TimeDate):
	con = db_connect()
	cur = con.cursor()
	cur.execute("INSERT INTO vehicles (NumberPlate, Coordinates, \
		Color, Vehicle, Image, TimeDate) VALUES (?, ?, ?, ?, ?, ?)",
		(number,Coordinates,Color,Vehicle,TimeDate+'.jpg',TimeDate))
	con.commit()
	cur.close()
	con.close()

def fetch_all():
	con = db_connect()
	cur = con.cursor()
	cur.execute("SELECT * FROM vehicles")
	result = cur.fetchall()
	for r in result:
		print(r)
	cur.close()
	con.close()

def upload_data():
	con = db_connect()
	cur = con.cursor()
	cur.execute("SELECT * FROM vehicles ORDER BY ID DESC LIMIT 1")
	result = cur.fetchone()
	cur.close()
	con.close()
	url = 'https://cement.avikki.me/alpr/gate_entry/'
	number = result[1].replace('"','')
	time = result[6]
	payload = {"in_time": str(time),"number_plate": str(number)}
	r = requests.post(url,auth=('nilansh','ballen@512'),json=payload)
	print(r.status_code)

create_table()


while True:
	job = beanstalkc.reserve()

	if job is None:
		# print("No number plate found")
		pass
	else:
		# print("A number plate found")
		pass
		plates_info = json.loads(job.body)

		if 'data_type' not in plates_info:
			#print('All openAlpr data should have data type. Some error occured!')
			pass
		elif plates_info['data_type'] == 'alpr_results':
			pass
		elif plates_info['data_type'] == 'alpr_group':
			pNumber = plates_info['best_plate_number']
			pCoordinates = plates_info['best_plate']['coordinates']
			pColor = plates_info['vehicle']['color'][0]['name']
			pVehicleType = plates_info['vehicle']['body_type'][0]['name']
			timeDate = datetime.now().isoformat()
			now = datetime.now()
			img_name = now.strftime("%d-%m-%Y_%H:%M:%S")+'.jpg'
			img_path = os.path.join(os.path.dirname(__file__),'Images',img_name)

			with open(img_path,'wb') as f:
				f.write(base64.b64decode(plates_info['vehicle_crop_jpeg']))
				f.close()

			# print(pNumber,'\n',pCoordinates,'\n',pColor,'\n',pVehicleType)
			insert_data(json.dumps(pNumber),json.dumps(pCoordinates),pColor,pVehicleType,timeDate)
			upload_data()
			# fetch_all()


		elif plates_info['data_type'] == 'heartbeat':
			# print('Heartbeat')
			pass

		job.delete()
