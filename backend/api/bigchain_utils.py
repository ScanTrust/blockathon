# -*- coding: utf-8 -*
from __future__ import print_function, absolute_import, unicode_literals

import json
import pprint
import time
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

import conf
PUB_KEY = conf.BIGCHAIN_PUB
PRIV_KEY = conf.BIGCHAIN_PRIV
TOKEN = "f94e7a2af781da96ea398c23cf676d0403ca90f233a336d31ed5d2a67414d084"  # Pre generated token asset


def get_bigchain_db():
    bdb_root_url = conf.BIGCHAIN_DB
    return BigchainDB(bdb_root_url)


def get_keypair():
    key = generate_keypair()
    return key.public_key, key.private_key


def onboard_user(pub_key):
    asset = {
        "data": {
            "name": "user",
            "ns": "scantrust:userdata",
            "pub_key": pub_key,
        }
    }
    txid = create_st_asset(asset=asset, meta={})

    return dict(
        name="user_onboarding",
        pub_key=pub_key,
        txid=txid
    )


def insert_cause(name, pub_key):
    asset = {
        "data": {
            "name": name,
            "description": "This is the cause description",
            "ns": "scantrust:causes",
            "pub_key": pub_key,
        }
    }
    txid = create_st_asset(asset=asset, meta={})

    return dict(
        name=name,
        pub_key=pub_key,
        txid=txid
    )


def insert_scan(scan, code_asset):
    message = scan.pop('message')
    uuid = scan.get('uuid')
    scan_asset = find_scan_asset(uuid)

    if scan_asset:
        return scan_asset['id'], False

    asset = {
        "data": {
            "name": "scan",
            "fk_code": code_asset,
            "uuid": uuid,
            "lat": scan.get('lat', ''),
            "lng": scan.get('lng', ''),
            "timestamp": int(time.time())
        }
    }

    metadata = {}

    txid = create_st_asset(asset=asset, meta=metadata)

    return txid, True


def create_st_asset(asset, meta=None):
    if not meta:
        meta = {}
    bdb = get_bigchain_db()
    meta['timestamp'] = int(time.time())
    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=PUB_KEY,
        asset=asset,
        metadata=meta
    )
    fulfilled_creation_tx = bdb.transactions.fulfill(prepared_creation_tx, private_keys=PRIV_KEY)
    bdb.transactions.send(fulfilled_creation_tx)

    return fulfilled_creation_tx['id']


def transfer_asset_to_self(txid, meta):
    """
    Used to edit metadata on a code
    """
    transfer_st_asset(txid, PUB_KEY, meta)


def transfer_st_asset(txid, to_pub_key, meta):
    bdb = get_bigchain_db()
    signed_tx = get_transaction(txid)
    output_index = 0
    output = signed_tx['outputs'][output_index]
    meta.update({"timestamp": "%s" % time.time()})
    input_ = {
        'fulfillment': output['condition']['details'],
        'fulfills': {
            'output_index': output_index,
            'transaction_id': signed_tx['id'],
        },
        'owners_before': output['public_keys'],
    }
    transfer_asset_id = signed_tx['id']
    transfer_asset = {
        'id': transfer_asset_id,
    }
    tx_transfer = bdb.transactions.prepare(
        operation='TRANSFER',
        inputs=input_,
        asset=transfer_asset,
        recipients=to_pub_key,
        metadata=meta
    )
    signed_tx_transfer = bdb.transactions.fulfill(
        tx_transfer,
        private_keys=PRIV_KEY,
    )
    sent_tx_transfer = bdb.transactions.send_commit(signed_tx_transfer)
    return sent_tx_transfer["id"]

def transfer_divisible_asset(to_public_key, amount):
    bdb = get_bigchain_db()
    tx_id = ""
    tx_outputs = bdb.outputs.get(PUB_KEY, spent=False)
    tx_list = bdb.transactions.get(asset_id=TOKEN)
    for tx in tx_list:
        for tx_output in tx_outputs:
            if tx["id"] == tx_output["transaction_id"]:
                if tx["operation"] == 'CREATE':
                    tx_id = tx["id"]
                if tx["operation"] == 'TRANSFER':
                    tx_id = tx["asset"]["id"]
                available = int(tx["outputs"][tx_output["output_index"]]["amount"])
                output = tx['outputs'][tx_output["output_index"]]
                transfer_input = {
                   'fulfillment': output['condition']['details'],
                   'fulfills': {
                       'output_index': tx_output["output_index"],
                       'transaction_id': tx["id"],
                   },
                   'owners_before': output['public_keys'],
                }
                transfer_asset = {
                   'id': tx_id,
                }
                recipients = [([to_public_key], amount)]
                if available - amount > 0:
                    recipients.append(([PUB_KEY], available-amount))
                prepared_transfer_tx = bdb.transactions.prepare(
                    operation='TRANSFER',
                    asset=transfer_asset,
                    inputs=transfer_input,
                    recipients=recipients
                )
                fulfilled_transfer_tx = bdb.transactions.fulfill(
                    prepared_transfer_tx,
                    private_keys=PRIV_KEY
                )

                return bdb.transactions.send_commit(fulfilled_transfer_tx)


def find_code_asset_id(message):
    bdb = get_bigchain_db()
    result = bdb.assets.get(search="\"" + message + "\"")
    if result:
        for r in result:
            data = r.get('data', {})
            if data.get('message', '') == message and data.get('name', '') == 'code':
                return r['id']

    return None


def find_asset_id(message):
    bdb = get_bigchain_db()
    result = bdb.assets.get(search="\"" + message + "\"")
    if result:
        return result[0]['id']


def find_asset(string, multiple=False):
    bdb = get_bigchain_db()
    result = bdb.assets.get(search=string)
    if result:
        return result if multiple else result[0]
    return {}


def find_scan_asset(string):
    bdb = get_bigchain_db()
    result = bdb.assets.get(search="\"" + string + "\"")
    if result:
        for r in result:
            if r.get('data', {}).get('name', '') == 'scan':
                return r
    return {}


def get_transaction(asset_id):
    bdb = get_bigchain_db()
    result = bdb.transactions.retrieve(asset_id)
    return result


def get_transactions(asset_id):
    bdb = get_bigchain_db()
    result = bdb.transactions.get(asset_id=asset_id)
    return result


def get_points(pub_key):
    bdb = get_bigchain_db()
    tokens = 0
    tx_list = bdb.transactions.get(asset_id=TOKEN)
    tx_outputs = bdb.outputs.get(pub_key, spent=False)

    for tx in tx_list:
        for tx_output in tx_outputs:
            if tx["id"] == tx_output["transaction_id"]:
                tokens += int(tx["outputs"][tx_output['output_index']]["amount"])
    return tokens


def get_history(pub_key):
    bdb = get_bigchain_db()
    tx_list = bdb.transactions.get(asset_id=TOKEN)
    tx_outputs = bdb.outputs.get(pub_key, spent=False)

    for tx in tx_list:
        for tx_output in tx_outputs:
            if tx["id"] == tx_output["transaction_id"]:
                print(json.dumps(tx, indent=4, sort_keys=True))
                print('===============')
    return {}


def format_cause_response(causes):
    response = []
    if causes:
        print(causes)
        for c in causes:
            response.append(
                {
                    "name": c['data']['name'],
                    "pub_key": c['data']['pub_key'],
                    "points": get_points(c['data']['pub_key']),
                    "url": c['data']['url'],
                    "description": c['data']['description'],
                    "image_url": c['data']['image_url']
                }
            )
    return response
