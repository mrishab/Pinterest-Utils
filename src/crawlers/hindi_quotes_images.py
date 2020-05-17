import requests
import json
import os


def fetch_resource(payload):
    url = "https://www.pinterest.ca/resource/BaseSearchResource/get/"

    headers = {
        'x-csrftoken': '{CSRF_TOKEN}',
        'cookie': '{COOKIE}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text.encode('utf8')).get('resource_response')


def download_images(results, dir):
    for i in range(0, len(results)):
        url = results[i].get('images').get('orig').get('url')
        if (results[i].get('is_promoted') == True):
            print("Skipped Promoted: {}".format(url))
            continue
        filename = os.path.join(dir, url_to_filename(url))
        download_image(url, filename)


def download_image(url, filename):
    res = requests.get(url)
    with open(filename, 'wb') as file:
        for chunk in res:
            file.write(chunk)


def url_to_filename(url):
    i = url.rfind("/") + 1
    return url[i:]


def update_bookmark_in_payload(payload, bookmark):
    import re
    pre = 'bookmarks%22%3A%5B%22'
    suff = '%22%5D%2C%22isPre'

    pattern = pre + '(.*)' + suff
    desired = pre + bookmark + suff

    return re.sub(pattern=pattern, repl=desired, string=payload)

###########
# RUNNING #
###########


if __name__ == "__main__":
    payload = 'source_url=%2Fsearch%2Fpins%2F%3Frs%3Dac%26len%3D2%26q%3Dhindi%2520motivational%2520quotes%26eq%3Dhindi%2520motivationa%26etslf%3D7277%26term_meta%5B%5D%3Dhindi%257Cautocomplete%257C0%26term_meta%5B%5D%3Dmotivational%257Cautocomplete%257C0%26term_meta%5B%5D%3Dquotes%257Cautocomplete%257C0&data=%7B%22options%22%3A%7B%22bookmarks%22%3A%5B%22Y2JVSG81V2sxcmNHRlpWM1J5VFVaU2MxWlVWbFJXTVVreVZWZDRkMkZIU2xoVVdHUlhUVmRvTTFaSGN6RlNhelZaVW14U1YxSlVWbEZXUm1SNlpVVTFWMXBJVWs1V2EzQnpWV3hTVjFkV1ZYbE5WRkpXVW14c00xWnNVa2RXVm1SSlVXeE9WVll6VGpSYVJWcFBWMWRLUms5WGFHbFhSVEV6Vm10YVlWVXhaSEpPVlZwUFZteGFVMVl3WkRSVU1WWnhVV3hrVGsxWFVqQlpNRlpoWWtkR05sSnNXbFppUmtwVVZrUkdTMUpzWkhWVmJGWk9VakZLYUZaR1dtRmpNVnBYVlc1U2ExSXdXbGhWYkZaWFRURmFSMkZJWkdsaGVrWkhWR3hXVjFsWFZuSlhibEpXWWtaS1dGVnFSbUZqVmxKeFZHeEdWbFpFUVRWYWExcFhVMWRLTmxWck5WTk5XRUpIVmpKd1QySXhiRmRYYTJSVFYwZFNWbFpzV2t0WFJteFdWbGhvYWxacldqQmFSVnBEVlRGS2NsWnFWbGROYm1oeVZsUktSMUl5U2tkaFJsWllVakpvVVZadGRHdGhiVkY0Vld4b2FsSnNjSEpVVlZKWFYxWmFSMVZyWkZoaVJuQkhXVlJPYzFaVk1VZFRia3BhWWtaVk1WWnNXazlXVmtaelkwVTFhRTB3U2pKV2EyUjNVekZWZVZOclpHcFNiV2hYV1d4b2IxUXhWbkphUnpscVlrWktXbGt3VlRGVU1WcDBaVVphV2xaWFVYZFdNbk40WXpKT1NWSnNWbGhUUlVwUVYyeGFZV1F4V2xkU2JrWm9VbXhhYjFSV1duZFhiR1IwWkVWYVVGWnJTbE5WUmxGNFQwVXhObFJZWkU5V1JrVjVWMWN4UjJGck5WVlViWFJQWlcxME5sUXdVbUZpVm13MlVsUk9UMDFyVlRGWGExSldUV3MxUlZkWWNFOVdSMk42VjFod1NrNVZNSGxUYld4UVVrVXdlVmRzVWtKTlZUVlZZa2N4VGxKR2JEWlhiR1JTVGtVMGVWZHRkRkJXUjNRelZHeGtSMkZXYTNwbFJUbFRWbTFSTkdaSFVtaFphbGw1VGxSSmVFOVhTVFJPZWtWM1dtMUplazR5VlhkTmFscHJUbTFGTkUxRWF6Qk9SRVY1V1RKTmVrOVhWbXBhVkdjeVRqSldiRmt5VW1oYVIxRXpXVmRSTTFwRVFYZGFSMUV4V21wV2FFMUhWamhVYTFaWVprRTlQUT09fFVIbzVhbFZGTVhoWGJUVlFaVlpqTVZwNk1XWk5WRUYzV0hwUmVXWkViR2xPVjFFd1dsUnJORnBFU1RKUFIxa3dUa1JCZDA5VVdURk5Na1V3VG0xU2EwNUhTbTFOUkZWNlRucGpOVTFIUm10Wk1scHFUMWRXYTAxVVkzaE5SMWt5VGxkS2FrNXFaekZQVkZKb1drZE5NRTV0VWpoVWExWllaa0U5UFE9PXwxODVmN2VlMDVjNTg4MDViMjFlMmZjNWU5OTA3ZTQ2ODZlNTgxMjMzNWNjZDYyMDhiMmNiOTQ4ZDU4NzI0YmQ1fE5FV3w%3D%22%5D%2C%22isPrefetch%22%3Afalse%2C%22article%22%3Anull%2C%22auto_correction_disabled%22%3Afalse%2C%22corpus%22%3Anull%2C%22customized_rerank_type%22%3Anull%2C%22filters%22%3Anull%2C%22page_size%22%3Anull%2C%22query%22%3A%22hindi%20motivational%20quotes%22%2C%22query_pin_sigs%22%3Anull%2C%22redux_normalize_feed%22%3Atrue%2C%22rs%22%3A%22ac%22%2C%22scope%22%3A%22pins%22%2C%22source_id%22%3Anull%7D%2C%22context%22%3A%7B%7D%7D'

    for i in range(0, 10):
        resource = fetch_resource(payload)
        results = resource.get('data').get('results')

        try:
            download_images(results, './images')
        except:
            pass

        # Next batch
        bookmark = resource.get('bookmark')
        payload = update_bookmark_in_payload(payload, bookmark)
