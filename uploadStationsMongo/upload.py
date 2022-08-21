import csv
import pymongo
import pandas as pd

"""
Example station Object 
object = {
	"name": "Cierro Prieto", String
	"lat" : 37.0902, Float
	"lng" : 37.0902, Float
	"dataSet" : [34,23,], Array with SPI values
	"stationNumber" : 1004, Int
	"state": "Nuevo Leon", String
	"beginning" : "1970-03", String
}

"""
stations = {}

def uploadObjectToMongo(stationObject):
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["DroughTracker"]
	mycol = mydb["stations"]
	x = mycol.insert_one(stationObject)


#Index {0: LAT, 1:LON, 2:ALT, 3:CLAVE, 4:EDO, 5:ESTACION, 6:INICIO}

def getStationObject(filename):
	file = open(filename)
	csvreader = csv.reader(file)
	header = []
	header = next(csvreader)
	stationObjects = []
	
	for row in csvreader:
		formatedRow = row[0].split()
		stationObject = obtainValuesFromList(formatedRow)
		stationObjects.append(stationObject)

	return stationObjects

def obtainValuesFromList(array):
	lenArr = len(array)
	for x in range(lenArr):
		name = ''
		for x in range(5,lenArr-1):
			stringToAppend = (array[x] + " ")
			name += stringToAppend
		stationObject = {"name": name,"lat": array[0], "lng": array[1], "stationNumber": array[3], "state":array[4], "beginning":array[-1]}
		return stationObject

def validateData(spi):
	if spi == -999.99:
		return False
	return True

def obtainHeaders(filename):
	file = open(filename)
	csvreader = csv.reader(file)
	stationNumber = []
	lat = []
	lon = []
	stationNumber = next(csvreader)
	del stationNumber[:2]
	
	#stationNumber = list(map(int, stationNumber))
	return stationNumber

def getDatSet(filename):
	stationObjects = getStationObject('stations.csv')
	headers = obtainHeaders(filename)
	file = pd.read_csv(filename, usecols=headers)
	#Ignore first two indexes (Lat, lon)
	#To access stationNumber from dict stationObjects[n]['stationNumber']
	for n in range(len(stationObjects)):
		for x in range(len(headers)):
			if stationObjects[n]['stationNumber'] == headers[x]:
				dataSet = []
				for number in file[stationObjects[n]['stationNumber']]:
					if (validateData(number)):
						dataSet.append(number)
				stationObjects[n]['dataSet'] = dataSet
	return stationObjects

objects = getDatSet('spi_01.csv')
for station in objects:
	uploadObjectToMongo(station)