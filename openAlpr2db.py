import beanstalkc
import json
import base64
from pprint import pprint
from datetime import datetime
import os
import sqlite3
import requests

#connecting to beanstalkd 
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

#path to local database, where the number plate informations will be stored
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'vehicles.db')

# method to connect to our database
def db_connect(db_path=DEFAULT_PATH):
    connection = sqlite3.connect(db_path)
    return connection
# method to create table
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
# method to insert data
def insert_data(number,Coordinates,Color,Vehicle,TimeDate):
	con = db_connect()
	cur = con.cursor()
	cur.execute("INSERT INTO vehicles (NumberPlate, Coordinates, \
		Color, Vehicle, Image, TimeDate) VALUES (?, ?, ?, ?, ?, ?)",
		(number,Coordinates,Color,Vehicle,TimeDate+'.jpg',TimeDate))
	con.commit()
	cur.close()
	con.close()
# method to fetch all data
def fetch_all():
	con = db_connect()
	cur = con.cursor()
	cur.execute("SELECT * FROM vehicles")
	result = cur.fetchall()
	for r in result:
		print(r)
	cur.close()
	con.close()
# method to upload a data to our database
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
	job = beanstalkc.reserve() # it will be waiting infinitely, till a job
								# is posted by the openalpr agent
	if job is None:
		# print("No number plate found")
		pass
	else:
		# print("A number plate found")
		pass
		plates_info = json.loads(job.body) # getting the detected plates info as a json

		if 'data_type' not in plates_info:
			#print('All openAlpr data should have data type. Some error occured!')
			pass
		elif plates_info['data_type'] == 'alpr_results':
			pass
		elif plates_info['data_type'] == 'alpr_group':
			pNumber = plates_info['best_plate_number'] # plate number
			pCoordinates = plates_info['best_plate']['coordinates'] #coordinate of plate in the frame
			pColor = plates_info['vehicle']['color'][0]['name'] # vehicle color
			pVehicleType = plates_info['vehicle']['body_type'][0]['name'] # vehicle type
			timeDate = datetime.now().isoformat()
			now = datetime.now()
			img_name = now.strftime("%d-%m-%Y_%H:%M:%S")+'.jpg'
			img_path = os.path.join(os.path.dirname(__file__),'Images',img_name) # store the images of the vehicles

			with open(img_path,'wb') as f:
				f.write(base64.b64decode(plates_info['vehicle_crop_jpeg'])) # openalpr gives vehicle images as string, so converting to jpg
				f.close()

			# print(pNumber,'\n',pCoordinates,'\n',pColor,'\n',pVehicleType)
			insert_data(json.dumps(pNumber),json.dumps(pCoordinates),pColor,pVehicleType,timeDate)
			upload_data()
			# fetch_all()


		elif plates_info['data_type'] == 'heartbeat':
			# print('Heartbeat')
			pass

		job.delete()
