import requests
response = requests.get('http://swapi.dev/api')

# print(response.request.headers)
# print(response.url)


response_json = response.json()
# print(f"{response_json=}")

# print(response_json["starships"])
starships_response = requests.get(response_json["starships"])
# print(f"{starships_response.json()=}")


# i can use json viewer to see the comnpartments
star_ships = starships_response.json()['results']

for ship in star_ships:
    print(f'{ship["name"]}')
