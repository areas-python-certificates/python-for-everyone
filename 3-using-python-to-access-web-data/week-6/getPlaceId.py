# Dependencies.
import urllib.request, urllib.parse, urllib.error
import json

# Endpoint.
endpoint = "http://py4e-data.dr-chuck.net/json?"

# Prompt the user for a location.
location = input("Enter location: ")

# Create a dictionary with the location and API key.
queryParametersDictionary = {
  "address": location,
  "key": 42
}

# URL encode the query parameters.
queryParameters = urllib.parse.urlencode(queryParametersDictionary)

# Create the API call URL.
apiCall = endpoint + queryParameters

# Call the API.
apiCallHandle = urllib.request.urlopen(apiCall)
apiResponse = apiCallHandle.read().decode()

# Convert the API response to a JSON object.
apiResponseJson = json.loads(apiResponse)

# Get the place ID and print it.
placeId = apiResponseJson["results"][0]["place_id"]
print(placeId)
