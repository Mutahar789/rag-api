import requests

HOST = 'http://localhost:16000'

def upload(user_id, filepaths):
    files = [ ('files', open(path, 'rb')) for path in filepaths] 

    req_data = {
        "user_id": user_id
    }

    response = requests.post(url=HOST+"/upload/", params=req_data, files=files)

    if response.status_code == 200:
        print("POST Request: /upload/: Successful")

    else:
        print("POST Request: /upload/: Failed:", response.status_code)


def search(user_id, question, top_k):
    req_data = {
        "user_id": user_id,
        "question": question,
        "top_k": top_k,
    }

    response = requests.post(url=HOST+"/search/", params=req_data)

    if response.status_code == 200:
        data = response.json()
        print("POST Request: /search/: Successful")
        print("Response:", data)

    else:
        print("POST Request: /search/: Failed:", response.status_code)


def clear_docs(user_id):
    req_data = {
        "user_id": user_id
    }

    response = requests.post(url=HOST+"/clear_docs/", params=req_data)

    if response.status_code == 200:
        print("POST Request: /clear_docs/: Successful")

    else:
        print("POST Request: /search/: Failed:", response.status_code)


def get_text(user_id, filepath):

    fd = {"file": open(filepath, 'rb')}
    req_data = {
        "user_id": user_id
    }
    response = requests.post(url=HOST+"/get_text/", params=req_data, files=fd)

    if response.status_code == 200:
        data = response.json()
        print("POST Request: /upload/: Successful")
        print("Response:", data)

    else:
        print("POST Request: /upload/: Failed:", response.status_code)
