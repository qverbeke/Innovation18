import requests

def retrain():
    requests.post("http://10.63.209.11:6969", data={"retrain":True})


retrain()
