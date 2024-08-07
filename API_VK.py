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
    
    def get_all_photo(self):
        params = self.params
        params.update({"owner_id": self.id, "extended": 1})
        response = requests.get(f'{self.API_base_url}photos.getAll', params=params)
        return response.json()


if __name__ == "__main__":
    access_token = config.access_token
    user_id = 237808807
    vk_client = VK(access_token, user_id)
    pprint(vk_client.get_all_photo())
