from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile
#from geekshop.settings import BASE_DIR
#import urllib.request



def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
                                                access_token=response['access_token'],
                                                v='5.92')),
                          None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data['sex']:
        if data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        elif data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE

    if data['about']:
        user.shopuserprofile.aboutMe = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    #if data['photo_max']:
        #urllib.request.urlretrieve(data['http://sun9-32.userapi.com/impf/c841629/v841629473/2b733/SlcafPiDFPA.jpg?size=810x1080&quality=96&sign=b06a07ed1d4751087154455a856490d4&type=album'], BASE_DIR / 'media/users_avatars/111.jpg')
        #user.avatar = 'users_avatars/111.jpg'
        #print(data['photo_max'])
    #доступ к фото в ВК так и не получил. Нашел в инете, что это баг (KeyError), но его не решили.

    user.save()



