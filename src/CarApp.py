import requests

##
## PLAN
## 1. Create class functions for APIs
##		1. GoogleDistance
##			Functions:
##			- GetDistance(city a, city b) - returns distance in miles
##			- CreateURL
##		2. FuelEconomy
##			Functions:
## 			- GetCarID(make, model, year)
##			- GetAverageMPG(car id)
##			- GetFuelType(car id)
##			- GetFuelPrice(fuel type)
##			- CreateURL
## 2. Use data from API to calculate estimate gas price
## 		- Need Distance from Google, mpg and fuel price from Fuel Economy
##		- Print summary in terminal


class GoogleDistance:

	def __init__(self):
		self.key = "AIzaSyBC3pRZztlHawOAlqrqPex-UxWfbqP4Dhg"
		self.payload = {}
		self.headers = {"Accept":"application/json"}
		self.getUserTripPath()
		

	def getUserTripPath(self):
		self.origin = input("Enter starting location (city or address): ")
		self.destination = input("Enter destination location (city or address): ")

	## MakeGetRequest: Returns response of GET request for given URL
	def MakeGetRequest(self,URL):
		return requests.request("GET", URL, headers=self.headers, data=self.payload)

	##
	## CreateURL: Returns the Google Distance URL for http get request given origin and destination
	##
	def CreateURL(self, origin, destination):

		base = "https://maps.googleapis.com/maps/api/distancematrix/json?"
		directions = "origins=" + origin + "&destinations=" + destination
		end = "&units=imperial&key=" + self.key
		
		return base + directions + end
		
	## GetDistance: Does http request and returns distance from origin to destination
	##
	def GetDistance(self, origin, destination):
		url = self.CreateURL(origin, destination)

		response = self.MakeGetRequest(url)
		distanceInMeters = response.json()['rows'][0]['elements'][0]['distance']['value']

		return distanceInMeters/1609


class FuelEconomy:

	def __init__(self):
		self.payload = {}
		self.headers = {"Accept":"application/json"}
		self.getUserCarModel()

	def getUserCarModel(self):
		self.make = input("Enter the make of your car (Example: Honda): ")
		self.model = input("Enter the model of your car (Example: Fit): ")
		self.year = input("Enter the year of your car: ")

	## MakeGetRequest: Returns response of GET request for given URL
	def MakeGetRequest(self,URL):
		return requests.request("GET", URL, headers=self.headers, data=self.payload)

	##
	## GetCarID: Returns carID of a make, model, and year for user to choose from
	##
	def GetCarID(self, make, model, year):

		carDescription = "year=" + year + "&make=" + make + "&model=" + model
		URL = "https://www.fueleconomy.gov/ws/rest/vehicle/menu/options?" + carDescription
		
		response = self.MakeGetRequest(URL)

		return response.json()['menuItem'][0]['value']

	##
	## GetFuelType: Returns the fuel type of the given carID
	##
	def GetFuelType(self, carID):

		URL = "https://www.fueleconomy.gov/ws/rest/vehicle/" + carID

		response = self.MakeGetRequest(URL)
		return response.json()['fuelType']

	##
	## GetFuelPrice: Returns the Fuel price given type
	##
	def GetFuelPrice(self, fuelType):

		URL = "https://www.fueleconomy.gov/ws/rest/fuelprices"

		response = self.MakeGetRequest(URL)

		return response.json()[fuelType]

	##
	## GetAverageMPG: Returns the average MPG given a car's ID
	##
	def GetAverageMPG(self, carID):
		URL = "https://www.fueleconomy.gov/ws/rest/ympg/shared/ympgVehicle/" + carID
		response = self.MakeGetRequest(URL)
		
		return response.json()['avgMpg']

def getAPIData():

	googleDistance = GoogleDistance()

	# Get the origin and destination from the user, and make sure it is valid
	while True:
		try:
			distance = googleDistance.GetDistance(googleDistance.origin, googleDistance.destination)
			break
		except:
			print("Your origin or destination could not be found")
		
		googleDistance.getUserTripPath()
	
	fuelEconomy = FuelEconomy()

	# Get the car type from the user, making sure it is valid
	while True:
		try:
			carID = fuelEconomy.GetCarID(fuelEconomy.make, fuelEconomy.model, fuelEconomy.year)
			break
		except:
			print("Your car model was not found")
		
		fuelEconomy.getUserCarModel()

	avgMPG = fuelEconomy.GetAverageMPG(carID)
	fuelType = fuelEconomy.GetFuelType(carID)
	fuelPrice = fuelEconomy.GetFuelPrice(fuelType.lower())

	return distance, float(avgMPG), float(fuelPrice)

def calculatePrice(distance, avgMPG, fuelPrice):

	gallons = distance/avgMPG
	price = gallons * fuelPrice

	return price


def main(): 

	distance, avgMPG, fuelPrice = getAPIData()
	print("The total price of your trip is: $" + "{:.2f}".format(calculatePrice(distance, avgMPG, fuelPrice)))




main()
