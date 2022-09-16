import json
import requests as rq


def set_geolocation():

    ip = rq.get('https://api.ipify.org?format=json')
    json_ip = json.loads(ip.text)
    location = rq.get(f"http://ip-api.com/json/{json_ip['ip']}")
    json_location = json.loads(location.text)

    return json_location

def get_or_set_geolocation(request):

    if 'country' and 'city' and 'state' in request.session: #Si las kyes no estan en la sesion
        pass
    else:
        if request.user.is_authenticated:

            if request.user.has_shipping_address():
                shipping_address = request.user.shipping_address
                request.session['country'] = str(shipping_address.country)
                request.session['city'] = shipping_address.city
                request.session['state'] = shipping_address.state

        else:

            shipping_address = set_geolocation()
            request.session['country'] = shipping_address['country']
            request.session['city'] = shipping_address['city']
            request.session['state'] = shipping_address['regionName']
