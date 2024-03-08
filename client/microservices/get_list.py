import requests

def get_file_list(server_url):
    response = requests.get(f"{server_url}/files")
    file_list = response.text.split("\n")
    return file_list
