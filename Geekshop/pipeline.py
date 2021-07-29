from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from authapp.models import UserProfile

def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return
    api_url = urlunparse(('httsp',
                          'api.vk.com',
                          '/methods/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join('bdate', 'sex', 'about')),
                          access_token=response['access_token'], v='5.131'),
                          None
                          ))
    resp = requests.get(api_url)
    if resp != 200:
        return
    data = resp.json()['response'][0]
    if data['sex']:
        user.userprofile.ChoseGender = UserProfile.Male if data['sex'] == 2 else UserProfile.FEMALE

    if data['about']:
        user.userprofile.about_me = data['about']
        user.save()

    if data['bdate']:
        bdate = datetime.strftime(data['bdate'],'%d.%m.%Y').date()
        age = timezone.now().date().year-bdate.year

