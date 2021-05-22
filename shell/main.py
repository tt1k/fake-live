import json
import re
import time
from urllib.parse import urlparse

import pandas as pd
import requests

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
        "continent": "",
        "country": "",
        "url": url.split(",")[1].rstrip()
    } for url in ls_urls_list]

    ls_success = {}
    ls_failed = {
        "failed": []
    }

    for idx, url_data in enumerate(ls_urls_data_list):
        url = url_data["url"]
        print("[{}]---[process]: {}/{} {}".format(time.ctime(), idx + 1, len(ls_urls_data_list), url))
        ip = find_ip(url)
        if ip and len(ip):
            ip_continent, ip_country = find_ip_country_info(ip)
            url_data["continent"] = ip_continent
            url_data["country"] = ip_country

            if ip_continent in ls_success.keys():
                if ip_country in ls_success[ip_continent].keys():
                    ls_success[ip_continent][ip_country] += [url_data]
                else:
                    ls_success[ip_continent][ip_country] = [url_data]
            else:
                ls_success[ip_continent] = {ip_country: [url_data]}
        else:
            ls_failed["failed"] += [url_data]

    success_file = open("build/fake_live_success.json", "w")
    success_file.write(json.dumps(ls_success, indent=4))
    success_file.close()

    failed_file = open("build/fake_live_failed.json", "w")
    failed_file.write(json.dumps(ls_failed, indent=4))
    failed_file.close()


main()
