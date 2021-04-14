import requests
import json

URL = "https://rickandmortyapi.com/api"


class DownloadError(Exception):
    pass


def download(endpoint, start_at = 1):
    while True:
        resp = requests.get(endpoint, params={'page': start_at})
        if resp.status_code == 200:
            yield (start_at, resp.json().get('results', {}))
            start_at += 1
        if resp.status_code == 404 and "There is nothing here" in resp.text:
            break
        elif 299 < resp.status_code < 600:
            raise DownloadError(resp.json())

def raw_data_writer(raw_data_dir, entity):
    def write_json_payload(response):
        page, payload = response
        with open(f"{raw_data_dir}/{entity}/raw.{page}.json", "w") as json_file:
            json_file.write(json.dumps(payload, indent=4, sort_keys=True))
    return write_json_payload


def main():
    entities = ["character", "location", "episode"]
    for entity in entities:
        data_writer = raw_data_writer("./raw/", f"{entity}s") 
        for data in download(f"{URL}/{entity}", 1):
            data_writer(data)
