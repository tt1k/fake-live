import json
import re
import time
from urllib.parse import urlparse
from numpy import add

import pandas as pd
import requests
from requests.sessions import should_bypass_proxies

maximum_try_count = 3


def find_ip(url: str, times: int = 1):
    origin_url = url
    origin_times = times
    netloc = urlparse(url).netloc

    ip_ll = netloc.split(":")
    if len(ip_ll) == 2 or len(ip_ll) == 1:
        ip = ip_ll[0]
        if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip):
            return ip
        netloc = ip

    url_body = netloc.split(".")
    if len(url_body) == 2:
        url = "https://" + netloc + ".ipaddress.com"
    else:
        url = "https://" + url_body[len(url_body) - 2] + "." + url_body[len(url_body) - 1] + ".ipaddress.com/" + netloc

    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_tables_data = pd.read_html(response.text)
            ip_table_data = []

            for table_data in html_tables_data:
                if list(table_data.head()) == ['Name', 'Type', 'Data']:
                    ip_table_data = table_data
                    break

            ip_type_data = list(ip_table_data.iloc[:, 1])
            ip_address_data = list(ip_table_data.iloc[:, 2])
            for idx, item in enumerate(ip_type_data):
                if item == "A":
                    return ip_address_data[idx]
            return None
        else:
            return None
    except AttributeError:
        print("[{}]---[error  ]: request {} failed, waiting 10 seconds to try again".format(time.ctime(), url))
        time.sleep(10)
        print("[{}]---[info   ]: start retry {} times".format(time.ctime(), origin_times))
        return None if origin_times == maximum_try_count else find_ip(origin_url, origin_times + 1)


def find_ip_country_info(ip: str):
    # get request will be reject if no headers provided
    url = "https://www.ipaddress.com/ipv4/{}".format(ip)
    headers = {'User-Agent': 'PostmanRuntime/7.26.8'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_tables_data = pd.read_html(response.text)
        ip_table_data = html_tables_data[0]

        ip_table_keys = list(ip_table_data.iloc[:, 0])
        ip_table_values = list(ip_table_data.iloc[:, 1])

        ip_continent = None
        ip_country = None

        for idx, item in enumerate(ip_table_keys):
            if item == "IP Continent":
                ip_continent = ip_table_values[idx]
            if item == "IP Country":
                ip_country = ip_table_values[idx]

        return ip_continent, ip_country
    else:
        return None, None


def main():
    # ls_urls_file = open("source/livestream_urls.txt", "r")
    ls_urls_file = open("source/demo.txt", "r")
    ls_urls_list = ls_urls_file.readlines()

    ls_urls_data_list = [{
        "name": url.split(",")[0],
        "url": url.split(",")[1].rstrip()
    } for url in ls_urls_list]

    ls_success = []
    ls_asia = []
    ls_europe = []
    ls_north_america = []
    ls_south_america = []
    ls_africa = []
    ls_oceania = []

    ls_failed = {
        "failed": []
    }

    ls_success.extend([
        {
            "id": 1,
            "name": "Asia",
            "children": ls_asia
        },
        {
            "id": 2,
            "name": "Europe",
            "children": ls_europe
        },
        {
            "id": 3,
            "name": "North America",
            "children": ls_north_america
        },
        {
            "id": 4,
            "name": "South America",
            "children": ls_south_america
        },
        {
            "id": 5,
            "name": "Africa",
            "children": ls_africa
        },
        {
            "id": 6,
            "name": "Oceania",
            "children": ls_oceania
        },
    ])

    id_serial = 7

    for idx, url_data in enumerate(ls_urls_data_list):
        url = url_data["url"]
        print("[{}]---[process]: {}/{} {}".format(time.ctime(), idx + 1, len(ls_urls_data_list), url))
        ip = find_ip(url)
        if ip and len(ip):
            ip_continent, ip_country = find_ip_country_info(ip)

            target_ll = []
            if ip_continent == "Asia":
                target_ll = ls_asia
            elif ip_continent == "Europe":
                target_ll = ls_europe
            elif ip_continent == "North America":
                target_ll = ls_north_america
            elif ip_continent == "South America":
                target_ll = ls_south_america
            elif ip_continent == "Africa":
                target_ll = ls_africa
            elif ip_continent == "Oceania":
                target_ll = ls_oceania
            else:
                continue

            added = False
            ip_data = {
                "id": id_serial,
                "name": url_data["name"],
                "url": url_data["url"]
            }
            id_serial = id_serial + 1
            for item in target_ll:
                if item["name"] == ip_country:
                    list(item["children"]).append(ip_data)
                    added = True
            if not added:
                target_ll.append(
                    {
                        "id": id_serial,
                        "name": ip_country,
                        "children": [ip_data]
                    }
                )
                id_serial = id_serial + 1

        else:
            ls_failed["failed"] += [url_data]

    success_file = open("build/fake_live_success.json", "w")
    success_file.write(json.dumps(ls_success, indent=4))
    success_file.close()

    failed_file = open("build/fake_live_failed.json", "w")
    failed_file.write(json.dumps(ls_failed, indent=4))
    failed_file.close()


main()
