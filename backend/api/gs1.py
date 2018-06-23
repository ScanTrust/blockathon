import requests

MESSAGES = {
    "E001": "Integrity failed: The length of this GTIN is invalid.",
    "E002": "Integrity failed: Incorrect check digit.",
    "E003": "Integrity failed: String contains alphanumerical characters.",
    "E004": "Incorrect number.That GS1 prefix (3 - digit country code) does not exist.",
    "E005": "Incorrect number based on GS1 Prefix reserved for special use.",
    "S001": "Unknown number, no information can be returned.",
    "S002": "Unknown GTIN from a license issued to: ",
    "S003": "Active GTIN from a license issued to: ",
    "S004": "Inactive GTIN from a license issued to: ",
    "S005": "Active GTIN from a license issued to:"
}

FIELD_MAP = {
    'gcpCompanyName': 'company',
}

URL = "https://cloud.gs1.org/api/v1/products/{gtin}/check"
EMAIL = "loek.boortman@gs1.nl"
KEY = "6e0bfa1bcbcd4b458cb90fd378aa9fce"


def map_fields(data):
    return {
        out_key: data.get(in_key)
        for in_key, out_key in FIELD_MAP.items() if in_key in data
    }


def get_gtin(gtin):
    resp = requests.get(URL.format(gtin=gtin), auth=(EMAIL, KEY))
    if resp.status_code in (200, 400):
        data = resp.json()
        if 'exception' in data:
            return {
                "status": "error",
                "message": MESSAGES[data.get('messageId')]
            }
        else:
            return {
                "status": "ok",
                "message": MESSAGES[data.get('reason')[0].get('messageId')],
                "fields": map_fields(data)
            }
    else:
        return {
            "status": "error",
            "message": resp.text[0:500]
        }