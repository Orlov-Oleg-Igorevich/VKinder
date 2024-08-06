from pprint import pprint
import requests
import json
import config


class VK:

    API_base_url = "https://api.vk.ru/method/"

    def __init__(self, access_token, user_id, version='5.199'):

        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()['response'][0]
    
    def get_profile_photo(self):
        params = self.params
        params.update({"owner_id": self.id, "album_id": "profile", "extended": 1})
        response = requests.get(f'{self.API_base_url}photos.get', params=params)
        return response.json()['response']['items']


if __name__ == "__main__":
    access_token = config.TOKEN
    user_id = int(input("Введите ваш user_id ВК"))
    vk_client = VK(access_token, user_id)
    pprint(vk_client.users_info())
