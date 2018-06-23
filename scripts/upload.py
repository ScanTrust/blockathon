#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script is made for the 2018 Blockathon in Brussels
# A JSON format containing code data will be processed and uploaded
# In a realistic situation this would be an integrated part of the ScanTrust decentralised process
# fixtures/fixtures.json holds the example data set for the physical codes and causes we have right now to demo

from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
import argparse
import json

# BigChainDb root url
bdb_root_url = 'http://51.144.103.72:9984/'


def main():
    parser = argparse.ArgumentParser(description="This script uploads codes into BigChainDb.")
    parser.add_argument('--json', type=argparse.FileType('rb'), help='Specify the path to a valid *.json file.', required=True)
    parser.add_argument('--token', help='Upload divisible asset', action='store_true')
    args = parser.parse_args()
    data = json.loads(args.json.read())
    uploader = Uploader()
    if args.token:
        uploader.generate_divisible_asset()
    uploader.upload(data)


class Uploader(object):
    # These fields should contain private and public Keys, generated by ScanTrust
    PUBLIC_KEY = ''
    PRIVATE_KEY = ''

    def __init__(self):
        self.bdb = BigchainDB(bdb_root_url)

    def _send_tx(self, asset, pub_key, priv_key, metadata=None, **kwargs):
        """ Generic method for asset creation"""
        tx = self.bdb.transactions.prepare(operation='CREATE', signers=pub_key, asset=asset,
                                           metadata=metadata, **kwargs)
        signed_tx = self.bdb.transactions.fulfill(tx, private_keys=priv_key)
        sent_tx = self.bdb.transactions.send_commit(signed_tx)
        try:
            asset_name = asset['data']['name']
        except KeyError:
            asset_name = asset['data']
        print("{} {} was successfully uploaded.".format(asset_name, sent_tx['id']))
        return sent_tx

    def upload_code(self, code):
        # Data structure for the "code" asset
        code_asset = {
            "data": {
                "name": "code",
                "ns": "scantrust:codes",  # namespase
                "message": code.pop('message'),
                "workorder": code.pop('workorder', ''),
                "product_id": code.pop('product_id', ''),
                "euipo_data": code.pop('euipo_data', ''),
                "serial_number": code.pop('serial_number', ''),
                "points": 100,
            }
        }
        return self._send_tx(code_asset, self.PUBLIC_KEY, self.PRIVATE_KEY, metadata=dict(is_consumed=False))

    def generate_divisible_asset(self):
        # Generating initial token
        asset = {'data': {'token': 'supertoken'}}
        metadata = {'metadata': 'metadata'}
        self._send_tx(asset, self.PUBLIC_KEY, self.PRIVATE_KEY, metadata, recipients=[([self.PUBLIC_KEY], 1000000000)])

    def upload(self, data):
        try:
            for cause in data['causes']:
                kp = generate_keypair()
                cause["pub_key"] = kp.public_key
                self._send_tx(dict(data=cause), kp.public_key, kp.private_key)
        except KeyError:
            print("No causes were found")
        try:
            [self.upload_code(code) for code in data['codes']]
        except KeyError:
            print("No codes where found")
        else:
            print('All the data was successfully uploaded')


if __name__ == "__main__":
    main()