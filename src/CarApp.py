import requests


# class GoogleDistanceMatrix(self):

# 	def __init__():
	

# 	def buildGoogleDistanceURL():

# class FuelEconomy(self):
	
# 	def __init():

	

def main(): 
	url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=Washington, DC&destinations=New York City, NY&units=imperial&key=AIzaSyBC3pRZztlHawOAlqrqPex-UxWfbqP4Dhg"

	#url = "https://www.fueleconomy.gov/ws/rest/ympg/shared/ympgVehicle/26425"
	payload = {}
	headers = {"Accept":"application/json"}

	response = requests.request("GET", url, headers=headers, data=payload)

	print(response.text)

	test = response.json()['rows'][0]['elements'][0]['distance']['text']
	print(test)

main()
