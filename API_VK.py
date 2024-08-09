from pprint import pprint
import requests
import json
import config
from datetime import date


class VK:

    API_base_url = "https://api.vk.ru/method/"

    def __init__(self, access_token, user_id, version='5.199'):

        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self, param):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id, 'fields': [param]}
        params.update(self.params)
        response = requests.get(url, params=params)
        return response.json()['response'][0]
    
    def get_all_photo(self):
        params = self.params
        params.update({"owner_id": self.id, "extended": 1, 'album_id': 'profile'})
        response = requests.get(f'{self.API_base_url}photos.get', params=params)
        return response.json()
    

    def users_get(self, val):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': val}
        params.update(self.params)
        response = requests.get(url, params=params)
        return response.json()['response'][0]

if __name__ == "__main__":
    access_token = config.TOKEN
    user_id = 1
    vk_client = VK(access_token, user_id)
    """photo_album = []
    for photo in vk_client.get_all_photo():
        photo_album.append((photo['likes']['count'], photo['orig_photo']['url']))
    photo_album = sorted(photo_album, key=lambda x: x[0], reverse=True)
    print(photo_album[:3])"""
