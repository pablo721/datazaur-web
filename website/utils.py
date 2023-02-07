import country_currencies
from ipwhois import IPWhois
from .models import Account
from monitor.models import Watchlist
from markets.models import Currency


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_location(ip):
    return IPWhois(ip).lookup_whois()['asn_country_code']


def get_currency(country):
    return country_currencies.get_by_country(country)[0]


def setup_account(request, user):
    currency_code = 'USD'
    location = None
    ip = None
    try:
        ip = get_client_ip(request)
        location = get_location(ip)
        currency_code = get_currency(location)
        print(f'Found ip, location and currency')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        account = Account.objects.create(user=user, currency_code=currency_code, signup_ip=ip, signup_location=location)
        if Currency.objects.filter(symbol=currency_code).exists():
            currency = Currency.objects.get(symbol=currency_code)
        else:
            currency = Currency.objects.get(symbol='USD')

        Watchlist.objects.create(owner=account, name='Watchlist', currency=currency)
        print(f'Account: {user.username} has been setup.')


