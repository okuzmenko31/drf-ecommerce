import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('NOVA_POSHTA_API_KEY', 'your_api_key')


def get_nova_poshta_city_list():
    """
    This function is for getting Ukrainian
    Nova Poshta cities.

    Returns:
        city_list(list): List with cities where have Nova Poshta.
    """
    url = 'https://api.novaposhta.ua/v2.0/json/'
    data = {
        "apiKey": api_key,
        "modelName": "Address",
        "calledMethod": "getCities",
        "methodProperties": {}
    }

    response = requests.post(url, json=data)
    cities = response.json()['data']
    city_list = [city['Description'] for city in cities]
    return city_list


def get_city_choices():
    """
    This function returns Nova Poshta cities choices,
    you can use result of this function in serializer,
    model or form.

    Returns:
        cities(tuple): Tuple with city choices.
    """
    cities_list = get_nova_poshta_city_list()
    cities = [city for city in cities_list]
    return tuple(cities)


def get_nova_poshta_post_offices():
    """
    This function is for getting Nova Poshata
    post offices.

    Returns:
        warehouse(Generator): The generator of warehouses.
    """
    url = "https://api.novaposhta.ua/v2.0/json/"
    payload = {
        "apiKey": api_key,
        "modelName": "AddressGeneral",
        "calledMethod": "getWarehouses",
        "methodProperties": {},
    }
    response = requests.post(url, json=payload)
    data = response.json()

    if data["success"]:
        warehouses = data["data"]
        for warehouse in warehouses:
            yield warehouse


def get_nova_poshta_post_offices_choices():
    """
    This function is for getting Nova Poshta
    Post Offices choices.

    Returns:
        warehouses(tuple): Tuple with post offices choices.
    """
    warehouses_list = []
    for item in get_nova_poshta_post_offices():
        if item['CategoryOfWarehouse'] == 'Branch':
            warehouses_list.append(item['Description'])
    warehouses = [warehouse for warehouse in warehouses_list]
    return warehouses
