from creds import my
import paytmchecksum
import requests
import time
import json


def LinkGen(linkname, description, amount):
    eot = str(time.time())
    paytmParams = dict()
    paytmParams["body"] = {
        "mid": my.MID,
        "linkType": "GENERIC",
        "linkDescription": "Test Payment",
        "linkName": "Test",
    }
    checksum = paytmchecksum.generateSignature(
        json.dumps(paytmParams["body"]),
        my.KEY
        )

    paytmParams["head"] = {
        "tokenType": "AES",
        "signature": checksum
    }
    post_data = json.dumps(paytmParams)
    response = requests.post(
        my.LINK,
        data=post_data,
        headers={"Content-type": "application/json"})
    # print (json.dumps(response.json(), indent=4, sort_keys=True))
    json_response = response.json()
    print(json.dumps(json_response, indent=2))
    r2json = json_response["body"]
    if r2json["resultInfo"]["resultStatus"] == "SUCCESS":
        return (r2json["shortUrl"], r2json["expiryDate"], r2json["linkId"])
    else:
        return "Server Unavailable"


def deletelink(linkid):
    paytmParams = dict()
    paytmParams["body"] = {
        "mid": my.MID,
        "linkId": linkid,
    }
    checksum = paytmchecksum.generateSignature(
        json.dumps(paytmParams["body"]),
        my.KEY
        )

    paytmParams["head"] = {
        "tokenType": "AES",
        "signature": checksum
    }
    post_data = json.dumps(paytmParams)
    requests.post(
        my.LINK,
        data=post_data,
        headers={"Content-type": "application/json"})


def checker(linkid,):
    paytmParams = dict()
    paytmParams["body"] = {
        "mid": my.MID,
        "linkId": linkid,
    }
    checksum = paytmchecksum.generateSignature(
        json.dumps(paytmParams["body"]),
        my.KEY
        )
    paytmParams["head"] = {
        "tokenType": "AES",
        "signature": checksum
    }
    post_data = json.dumps(paytmParams)
    response = requests.post(
        my.LINK,
        data=post_data,
        headers={"Content-type": "application/json"}
        )
    json_response = response.json()
    r2d2 = json_response["body"]
    if r2d2["orders"]["orderStatus"] == "SUCCESS":
        return True
    else:
        return False
