import requests
import xlrd, xlwt

import requests
import json
import time
import random


def get_const_headers_and_cookies(city_name):
    cookies = {
        "ig_did": "351AF891-DB32-4F9C-A781-EE272A150F1A",
        "ig_nrcb": "1",
        "mid": "XzE8yAAEAAH6IBazQPnYExrAwZPK",
        "fbm_124024574287414": "base_domain=.instagram.com",
        "shbid": "1157",
        "shbts": "1610388353.4120233",
        "rur": "FTW",
        "csrftoken": "ERGTu7VnO9xOUTQ9JOs09QG7WSkgtte6	",
        "ds_user_id": "45397981507",
        "sessionid": "45397981507%3A9BggaW7TD6UQ2d%3A20",
        "fbsr_124024574287414": "9UdO6JPTVIYW1EDT4v2rbrK3SEgt3qWA7KT8M94HTdQ.eyJ1c2VyX2lkIjoiMTAwMDYxOTYyNDI2NTM2IiwiY29kZSI6IkFRQ0lNeTRqMzZUcVdrMjVHNjV3RlFPcFUzYm9zV1Vsei14emZZTFYtcEVEb2t3dm8zeExwSUxkRElfcmV5bVV0emI2U1pDSVRMTXdLRkNEcl9TOUl4QUhFODA1X0NxVGo1MFZqeDRIdGtwMkRJem4tMVM0WXBfbjk1dGJERnY5RXVpMVlCUnlBSlJRa0xqX3VOTkU3S1Q1eWJEUmRJMUZxRHZpZ3ZIeHoweWo5LXlRVms1c0JuUDlYMTdDRjJfZE55amZreXlNSklvSjg0REFmZlpCRWpRSGpsWjFmeUxYS2xVNFJrQURHeXRqajVZclhFbjVxNGtuZGRQSE9iSFZWQk93LVIyazc4ejBvTGc2MlUyZm1LUU5qV1hYTDAtSU9JM3JWeHdTRW5iQkgxLU9kYm5kU1BiMGt2UkFYcUE1Vnc0a2FGbmgwYjRqNXZTSjhhOVhNQlJEIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQU5FUFM0N3FKQnpFSlF3SEdGYWg4eWpnR2RIcWt6WkNtVDFjSXlpMzlMdUFWbDE2dWd3WkNGcE1OTFBNSjBDV005TjlmWkIwUzJRSE5lQ21tYVVOTG9rS2hXRXNUVmg3djltTE5aQVN2ZGN1UlI4RVA0c1NITnJpNHBaQU8zRm04VGV3TVpBMHlwRjhlN0FSS3hTWkFvdWlyWkM4dVpDUnVsRzlaQWJuV21ock1CY25NZEx4ejZtSVVaRCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNjEwNDAwNTM1fQ",
        "urlgen": "{\"5.18.211.157\": 41733}:1kz4kI:i5aDAkX4uNoWAQ-DGp9qUjFFW28"
    }


    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
        # "cache-control": "no-cache",
        "referer": "https://www.instagram.com/explore/tags/" + city_name + "/",
        # "connection": "keep-alive",
        # "host": "www.facebook.com",
        # "origin": "https://www.instagram.com",
        # "pragma": "no-cache",
        # "referer": "https://www.instagram.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "x-csrftoken": "cRRi7ftNSOwKr7xArzTwR0GXJEG7nyXS",
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "hmac.AR2WVjdIULriX6eobHPBuB5XPBARPvX8MNkrKTItM46VSQU7",
        "x-requested-with": "XMLHttpRequest"
        # "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
    }
    return cookies, headers


def request_with_cursor(cookies, headers, city_name, cursor=0):
    URL = 'https://www.instagram.com/graphql/query/'
    VARIABLES = "{" + '\"tag_name\":' + '\"' + city_name + '\",'
    PARAMS = {}
    if cursor == 0:
        VARIABLES += '\"include_reel\":true, \"include_logged_out\":\"false\"}'
        PARAMS['query_hash'] = "845e0309ad78bd16fc862c04ff9d8939"
    else:
        cnt = 12
        VARIABLES += '\"first\":' + str(cnt) + ', \"after\":' + '\"' + cursor + '\"' + "}"
        PARAMS['query_hash'] = "9b498c08113f1e09617a1703c22b2f32"
    PARAMS['variables'] = VARIABLES
    r = requests.get(url=URL, params=PARAMS, headers=headers, cookies=cookies)
    return r.content


def request(city_name):
    list_of_res = []
    list_of_posts = []
    try:
        # https://www.facebook.com/x/oauth/status?client_id=124024574287414&input_token&origin=1&redirect_uri=https%3A%2F%2Fwww.instagram.com%2Fexplore%2Ftags%2Ftomskgram%2F&sdk=joey&wants_cookie_data=true
        id = '45061470565'
        # URL = "https://www.instagram.com/web/search/topsearch/"
        URL = "https://www.instagram.com/explore/tags/" + city_name + "/?__a=1"
    # PARAMS = {
    #    'query_hash': "845e0309ad78bd16fc862c04ff9d8939",
    #    'variables': VARIABLES
    # 'user_id': id,
    # 'context': 'blended',
    # }
        cookies, headers = get_const_headers_and_cookies(city_name)
        r = requests.get(url=URL, headers=headers, cookies=cookies)

        content = r.content
        endCursor = json.loads(content)["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["end_cursor"]
        request_with_cursor(cookies, headers, city_name)#first call with spec params
        num_of_lists = 150
        f = open("Data/Res" + str(num_of_lists) + "_" + city_name, 'w')
        for i in range(num_of_lists):
            time.sleep(int(random.random() * 3) + 2)
            content = request_with_cursor(cookies, headers, city_name, endCursor)  # first call with spec params
            loaded = json.loads(content)
            if "graphql" in loaded:
                data = loaded["graphql"]
            else:
                data = loaded["data"]
            endCursor = data["hashtag"]["edge_hashtag_to_media"]["page_info"]["end_cursor"]
            for edges in data["hashtag"]["edge_hashtag_to_media"]["edges"]:
                if edges["node"]:
                    list_of_res.append(edges["node"]["shortcode"])
                    for text in edges["node"]["edge_media_to_caption"]["edges"]:
                        if text["node"]:
                            list_of_posts.append(text["node"]["text"])
            f = open("Data/Res" + str(num_of_lists) + "_" + city_name, 'w')
            print("Cur output:" + str(i) + "\n")
            f.write(str(list_of_res) + "\n")
        f.close()
        return list_of_res, list_of_posts
    except:
        return list_of_res, list_of_posts


if __name__ == '__main__':
    city = 'kazan'
    wb = xlwt.Workbook()
    ws = wb.add_sheet("List 1")

    _, posts = request(city)
    # print(posts)
    i = 0
    for post in posts:
        ws.write(i, 0, post)
        i += 1

    wb.save('Data/' + city + '_Dataset.xls')

