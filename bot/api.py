import requests

BASE_URL = 'http://127.0.0.1:8000'

import json

###### ~~~~ User All Info ~~~~ ######

def all_info(telegram_id):
    response = requests.post(BASE_URL + '/en/api/user/', data={
        'telegram_id': telegram_id
    })
    data = json.loads(response.text)
    return data

###### ~~~~ Language Info ~~~~ ######
def language_info(telegram_id):
    response = requests.post(BASE_URL + '/en/api/user/', data={
        'telegram_id': telegram_id
    })
    data = json.loads(response.text)
    return data['language']

###### ~~~~ Get All Categories ~~~~ ######
def get_categories(language):
    response = requests.get(BASE_URL + language + '/api/category/')
    data = json.loads(response.text)
    categories = [i['name'] for i in data]
    return categories

###### ~~~~ Get All russian english and uzbek Categories ~~~~ ######
def get_all_categories():
    response = requests.get(BASE_URL + '/api/category/')
    data = json.loads(response.text)
    category_uz = [i['name_uz'] for i in data]
    category_ru = [i['name_ru'] for i in data]
    category_en = [i['name_en'] for i in data]
    return category_uz + category_ru + category_en

###### ~~~~ Get Search Category ~~~~ ######
def category_info(language, category):
    response = requests.get(BASE_URL + language + '/api/category/?search=' + category)
    data = json.loads(response.text)
    data = data[0]
    if data['subcategory'] == []:
        categories = []
        for i in data['products']:
            data = {}
            data['id'] = i['id']
            data['name'] = i['name']
            data['price'] = i['price']
            data['image'] = i['imaage']
            categories.append(data)
        info = {'products': categories}
    else:
        categories = [i['name'] for i in data['subcategory']]
        info = {'subcategory': categories}
    return info

#################### SubCategory ##################
def subcategory_info(language, subcategory):
    response = requests.get(BASE_URL + language + '/api/subcategory/?search=' + subcategory)
    data = json.loads(response.text)
    return data[0]['products']

#################### Get Product ##################
def get_product(id, language):
    response = requests.get(BASE_URL + language + '/api/product/' + str(id) + '/')
    data = json.loads(response.text)
    return data

#################### Create User ##################
def create(name, telegram_id, telegram_username):
    response = requests.post(BASE_URL + '/en/api/botuser/', data={
        'name': name,
        'telegram_id': telegram_id,
        'telegram_username': telegram_username
    })
    return response.status_code

#################### Change Language ##################
def change_language(telegram_id, language):
    response = requests.post(BASE_URL + '/en/api/change/', data={
        'telegram_id': telegram_id,
        'language': language,
    })
    return response.status_code

#################### Change Phone Number ##################
def change_phone(telegram_id, phone):
    response = requests.post(BASE_URL + '/en/api/phone/', data={
        'telegram_id': telegram_id,
        'phone': phone
    })
    return response.status_code

#################### Shop Info ##################
def shop_info(language):
    response = requests.get(BASE_URL + language + '/api/shop/')
    data = json.loads(response.text)
    return data[0]

#################### Set Order ##################
def set_order(telegram_id, product, quantity):
    response = requests.post(BASE_URL + '/en/api/set_order/', data={
        'telegram_id': telegram_id,
        'product': product,
        'quantity': quantity
    })
    data = json.loads(response.text)
    return data

#################### Delete Basket ##################
def delete_basket(telegram_id):
    response = requests.post(BASE_URL + '/en/api/delete_basket/', data={
        'telegram_id': telegram_id
    })
    data = json.loads(response.text)
    return data

#################### Delete Item ##################
def delete_item(telegram_id, product):
    response = requests.post(BASE_URL + '/en/api/delete_item/', data={
        'telegram_id': telegram_id,
        'product': product
    })
    data = json.loads(response.text)
    return data
