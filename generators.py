import requests
import json

class GeneratorAPI:

    def __init__(self):
        self.data = []
        self.data = self.formatData(self.getAllDataFromAPI())
        self.google_api_key = os.environ['GOOGLE_API_KEY']


    def getAllDataFromAPI(self):
        r = requests.get("https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/Generating_Units/FeatureServer/0/query?where=STATE=%27VA%27&outFields=*&outSR=4326&f=json")
        #get only VA data for demo purposes
        response = json.loads(r.text)
        return response['features']

    def formatData(self, data):

        def formatEntry(entry):

            return {
                'address': None,
                'operator': entry['attributes']['OPERATOR'],
                'zipcode': entry['attributes']['ZIPCODE'],
                'phonenumber': None,
                'latitude': entry['attributes']['LATITUDE'],
                'longitude': entry['attributes']['LONGITUDE']
            }

        return [formatEntry(entry) for entry in data]


    def registerGenerator(self, operator, zipcode, address, number, latitude=None, longitude=None):
        entry = {
            'address': address,
            'operator': operator,
            'zipcode': zipcode,
            'phonenumber': number,
            'latitude': latitude,
            'longitude': longitude
        }

        self.data.append(entry)

    def zipcodeQuery(self, zip):
        return [entry for entry in self.data if (entry['zipcode'] == zip)]

    def decodeLatLong(self, latitude, longitude):
        r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(latitude) + "," + str(longitude) + "&key=" + self.google_api_key)
        return json.loads(r.text)['results'][0]['formatted_address']

if __name__ == "__main__":
    gen = GeneratorAPI()
    print('registering...')
    gen.registerGenerator('Walter Carlson', '24141', '123 Happy Lane, Radford, VA', '+15712691693')
    print('querying....')
    for entry in gen.zipcodeQuery('24141'):
        if entry['address']:
            print(entry['operator'] + ": " + entry['address'])
        else:
            print(entry['operator'] + ": " + gen.decodeLatLong(entry['latitude'], entry['longitude']))

