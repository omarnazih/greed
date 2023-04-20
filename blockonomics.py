import requests
import configloader
import logging
import sqlalchemy
import datetime
from decimal import Decimal
import json
import re

import database as db

log = logging.getLogger(__name__)

# Define all the database tables using the sqlalchemy declarative base
class Blockonomics:

    @staticmethod
    def fetch_new_btc_price():
        url = 'https://www.blockonomics.co/api/price'
        params = {'currency':configloader.user_cfg["Payments"]["currency"]}
        r = requests.get(url,params)
        if r.status_code == 200:
          price = r.json()['price']
          log.debug("BTC Price %s" % price)
          return price
        else:
          log.error("Fetch BTC Price Failed, Status: %s, Response: %s" % (r.status_code, r.content))
    
    @staticmethod
    def _get_secret():
        return configloader.user_cfg["Bitcoin"]["secret"]

    @staticmethod
    def new_address(reset=False):
        api_key = configloader.user_cfg["Bitcoin"]["api_key"]
        url = 'https://www.blockonomics.co/api/new_address'
        params = {}
        if reset == True:
          params['reset'] = 1
        
        headers = {'Authorization': "Bearer " + api_key}
        r = requests.post(url, headers=headers, params={**params, "match_callback": Blockonomics._get_secret()})
        if r.status_code == 200:
          return r
        else:
          log.error("New Address Generation Failed, Status: %s, Response: %s" % (r.status_code, r.content), exc_info=False)
          return r

class BlockonomicsPoll:

    def __init__(self, bot, engine) -> None:
        self.bot = bot

        log.debug(f"Opening new database session for Blockonomics Poll")
        self.session = sqlalchemy.orm.sessionmaker(bind=engine)()

    def __del__(self):
        self.session.close()

    def check_for_pending_transactions(self) -> None:

        pending_addresses = [o.address for o in self.session.query(db.BtcTransaction.address).filter(db.BtcTransaction.status != 2)]
        if not pending_addresses: return

        response = self._get_history_for_addresses(addresses=pending_addresses)
        # Update Pending Transactions
        for transaction in response.get('pending', []):
            self.handle_update(
                address=transaction['addr'][0],
                status=transaction['status'],
                satoshi=transaction['value'],
                txid=transaction['txid']
            )

        # Update Confirmed Transactions
        for transaction in response.get('history', []):
            self.handle_update(
                address=transaction['addr'][0],
                status=2,
                satoshi=transaction['value'],
                txid=transaction['txid']
            )

    def _get_history_for_addresses(self, addresses: list) -> dict:
        
        api_key = configloader.user_cfg["Bitcoin"]["api_key"]

        url = "https://www.blockonomics.co/api/searchhistory"
        body = { "addr": ", ".join(addresses) }
        headers = { "Authorization": "Bearer %s" % api_key }

        r = requests.post(
            url=url,
            data=json.dumps(body),
            headers=headers
        )

        if r.status_code == 200:
            return r.json()
        else:
          log.error("Get Payments History failed, Status: %s, Response: %s" % (r.status_code, r.content))
          return {"pending": [], "history": []}

    def _satoshi_to_fiat(self, satoshi, transaction_price) -> float:
        """Convert satoshi to fiat"""

        received_btc = satoshi/1.0e8
        received_dec = round(Decimal(received_btc * transaction_price), int(configloader.user_cfg["Payments"]["currency_exp"]))
        return float(received_dec)
    
    @classmethod
    def _sanitize_address(cls, address: str) -> str:
        return re.sub(r"[^a-zA-Z0-9]", "", address)

    def handle_update(self, address, status, satoshi, txid) -> str:
        """Handles Transaction Updates"""
        
        address = self._sanitize_address(address)

        transaction = self.session.query(db.BtcTransaction).filter(db.BtcTransaction.address == address).one_or_none()
        if transaction and transaction.txid == "":
            
            # Check the status
            if transaction.status == -1:
                current_time = datetime.datetime.now()
                timeout = 30

                # If timeout has passed, use new btc price
                if current_time - datetime.timedelta(minutes = timeout) > datetime.datetime.strptime(transaction.timestamp, '%Y-%m-%d %H:%M:%S.%f'):
                    transaction.price = Blockonomics.fetch_new_btc_price()
                transaction.timestamp = current_time
                transaction.status = 0
                self.bot.send_message(transaction.user_id, "Payment recieved!\nYour account will be credited on confirmation.")
            
            if status == 2:
                received_float = self._satoshi_to_fiat(satoshi, transaction.price)

                log.info("Recieved %(received_float)s %(currency)s on address %(address)s" % {
                    "received_float": received_float,
                    "currency": configloader.user_cfg["Payments"]["currency"],
                    "address": address
                })

                # Add the credit to the user account
                user = self.session.query(db.User).filter(db.User.user_id == transaction.user_id).one_or_none()
                user.credit += int(received_float * (10 ** int(configloader.user_cfg["Payments"]["currency_exp"])))

                # Add a transaction to list
                new_transaction = db.Transaction(
                    user=user,
                    value=int(received_float * (10 ** int(configloader.user_cfg["Payments"]["currency_exp"]))),
                    provider="Bitcoin",
                    notes = address
                )

                # Add and commit the transaction
                self.session.add(new_transaction)

                # Update the received_value for address in DB
                transaction.value += received_float
                transaction.txid = txid
                transaction.status = 2
                self.session.commit()

                self.bot.send_message(
                    transaction.user_id, 
                    "Payment confirmed!\nYour account has been credited with %(received_float)s %(currency)s." % {
                        "received_float": received_float,
                        "currency": configloader.user_cfg["Payments"]["currency"]
                    }
                )

                return "Success"
            else:
                self.session.commit()
                return "Not enough confirmations"
        else:
            self.session.commit()
            return "Transaction already proccessed"
        