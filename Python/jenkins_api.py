import requests


def job_create(url: str, name: str, proxy_list: list = None, auth: tuple = None):
    url_final = url + ""
    requests.post(url=url_final, proxies=proxy_list, auth=auth)


def get_jobs(url: str):
    requests.get()