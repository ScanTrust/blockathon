import api.bigchain_utils as utils


def format_cause_response(causes):
    response = []
    if causes:
        for c in causes:
            response.append(
                {
                    "name": c['data']['name'],
                    "pub_key": c['data']['pub_key'],
                    "points": utils.get_points(c['data']['pub_key']),
                    "url": c['data']['url'],
                    "description": c['data']['description'],
                    "image_url": c['data']['image_url'],
                    "donation_value": c['data']['donation_value'],
                    "goal": c['data']['goal']
                }
            )
    return response


def format_history_response(spendings):
    result = {}
    for s in spendings:
        result[s["to"]] = result.get(s["to"], 0) + int(s["amount"])

    return result
