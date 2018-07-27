import requests

def retrain():
    requests.post("http://10.63.201.94:6969", data={"retrain":True})


retrain()
