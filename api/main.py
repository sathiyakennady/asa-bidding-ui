from pyteal import *
from src.app_services.app_initializaion_service import AppInitializationService
from src.app_services.app_interaction_service import AppInteractionService
from src.app_utils.credentials import main_developer_credentials, get_developer_credentials
from threading import Timer
import src.app_utils.blockchain_utils as blockchain_utils

main_dev_pk, main_dev_address = main_developer_credentials()

app_initialization_service = AppInitializationService(app_creator_pk=main_dev_pk,
                                                      app_creator_address=main_dev_address,
                                                      asa_unit_name="wawa",
                                                      asa_asset_name="wawa",
                                                      app_duration=100,
                                                      teal_version=3)

lastR=app_initialization_service.get_block_number()
print("check--->")
print(lastR)

print(Global.round())
print(1)
app_initialization_service.create_application()

print(2)
app_initialization_service.create_asa()
print(3)
app_initialization_service.setup_asa_delegate_smart_contract()
print(4)
app_initialization_service.deposit_fee_funds_to_asa_delegate_authority()
print(5)
app_initialization_service.change_asa_credentials()
print(6)
app_initialization_service.setup_algo_delegate_smart_contract()
print(7)
app_initialization_service.deposit_fee_funds_to_algo_delegate_authority()
print(8)
app_initialization_service.setup_app_delegates_authorities()
print(9)
print(f'app_id: {app_initialization_service.app_id} \n'
      f'asa_id: {app_initialization_service.asa_id} \n'
      f'asa_delegate_authority_address: {app_initialization_service.asa_delegate_authority_address} \n'
      f'algo_delegate_authority_address: {app_initialization_service.algo_delegate_authority_address}')


bidder_pk, bidder_address = get_developer_credentials(developer_id=1)


print(10)
app_interaction_service = AppInteractionService(app_id=app_initialization_service.app_id,
                                                asa_id=app_initialization_service.asa_id,
                                                current_owner_address=main_dev_address,
                                                teal_version=3)


lastRound=app_interaction_service.get_block_number()
print("last round--->" )
print(lastRound)

print(11)
app_interaction_service.execute_bidding(bidder_private_key=bidder_pk,
                                        bidder_address=bidder_address,
                                        amount=3000000)

print(12)
app_interaction_service.execute_bidding(bidder_private_key=main_dev_pk,
                                        bidder_address=main_dev_address,
                                        amount=4000000)

print(13)
print()
# This should fail if we try to submit it after the bidding process has ended
#app_interaction_service.execute_bidding(bidder_private_key=bidder_pk,
 #                                        bidder_address=bidder_address,
  #                                       amount=5000005)



lastRound=app_interaction_service.get_block_number()
print("last round--->")
print(lastRound)

while lastR+120 >= lastRound:

    lastRound=app_initialization_service.get_block_number()
    print("in while loop")
    print(lastRound)


app_interaction_service.pay_to_seller(asa_seller_address=app_initialization_service.app_creator_address)



