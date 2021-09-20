import glob
import io
import os
import uuid

import numpy as np
from flask import Flask, jsonify, make_response, render_template, request
from pyteal import *
from src.app_services.app_initializaion_service import AppInitializationService
from src.app_services.app_interaction_service import AppInteractionService
from src.app_utils.credentials import main_developer_credentials, get_developer_credentials

app = Flask(__name__)
app.secret_key = "s3cr3t"
app.debug = False
app._static_folder = os.path.abspath("templates/static/")

global bidding_amount
main_dev_pk, main_dev_address = main_developer_credentials()

app_initialization_service = AppInitializationService(app_creator_pk=main_dev_pk,
                                                      app_creator_address=main_dev_address,
                                                      asa_unit_name="wawa",
                                                      asa_asset_name="wawa",
                                                      app_duration=100,
                                                      teal_version=3)

app_initialization_service.create_application()

app_initialization_service.create_asa()

app_initialization_service.setup_asa_delegate_smart_contract()

app_initialization_service.deposit_fee_funds_to_asa_delegate_authority()

app_initialization_service.change_asa_credentials()

app_initialization_service.setup_algo_delegate_smart_contract()

app_initialization_service.deposit_fee_funds_to_algo_delegate_authority()

app_initialization_service.setup_app_delegates_authorities()

print(f'app_id: {app_initialization_service.app_id} \n'
      f'asa_id: {app_initialization_service.asa_id} \n'
      f'asa_delegate_authority_address: {app_initialization_service.asa_delegate_authority_address} \n'
      f'algo_delegate_authority_address: {app_initialization_service.algo_delegate_authority_address}')


bidder_pk, bidder_address = get_developer_credentials(developer_id=1)

app_interaction_service = AppInteractionService(app_id=app_initialization_service.app_id,
                                                asa_id=app_initialization_service.asa_id,
                                                current_owner_address=main_dev_address,
                                                teal_version=3)



@app.route("/", methods=["GET"])
def index():
    title = "Create the input image"
    global  bidding_amount
    bidding_amount=3000005
    return render_template("layouts/index.html", title=title)


@app.route("/bidding", methods=["POST"])
def bidding():
    print("ajax request")
    global  bidding_amount
    if request.method == "POST":
        qtc_data = request.get_json()

    print(qtc_data)
    print(qtc_data[0].get("bidder_private_key"))
    bidder_private_key=qtc_data[0].get("bidder_private_key")
    bidder_address=qtc_data[1].get("bidder_private_key")
    amount=qtc_data[2].get("amount")
    print(bidder_address)
    print(amount)


    if amount > bidding_amount:
        print("if")
        bidding_amount=amount
    else:
        print("else")
        return "amount change"

    app_interaction_service.execute_bidding(bidder_private_key=bidder_private_key,
                                            bidder_address=bidder_address,
                                            amount=amount)
    results = {'processed': 'true'}
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
