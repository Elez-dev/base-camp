from web3 import Web3
import time
from settings import CHAIN_RPC
from requests.adapters import Retry
import requests
from loguru import logger
from utils.tg_bot import TgBot


SCAN = {
    'Arbitrum': 'https://arbiscan.io/tx/',
    'Optimism': 'https://optimistic.etherscan.io/tx/',
    'Sepolia-Base': 'https://sepolia.basescan.org/tx/',
    'Sepolia-ETH': 'https://sepolia.etherscan.io/tx/'
}


class Wallet(TgBot):

    def __init__(self, private_key, chain, number):
        self.private_key = private_key
        self.chain = chain
        self.number = number
        self.web3 = self.get_web3(chain)
        self.scan = self.get_scan(chain)
        self.account = self.web3.eth.account.from_key(private_key)
        self.address_wallet = self.account.address

    @staticmethod
    def get_web3(chain):
        retries = Retry(total=10, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        adapter = requests.adapters.HTTPAdapter(max_retries=retries)
        session = requests.Session()
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return Web3(Web3.HTTPProvider(CHAIN_RPC[chain], request_kwargs={'timeout': 60}, session=session))

    @staticmethod
    def get_scan(chain):
        return SCAN[chain]

    @staticmethod
    def to_wei(decimal, amount):
        if decimal == 6:
            unit = 'picoether'
        else:
            unit = 'ether'

        return Web3.to_wei(amount, unit)

    @staticmethod
    def from_wei(decimal, amount):
        if decimal == 6:
            unit = 'picoether'
        elif decimal == 8:
            return float(amount / 10 ** 8)
        else:
            unit = 'ether'

        return Web3.from_wei(amount, unit)

    def send_transaction_and_wait(self, tx, message):
        signed_txn = self.web3.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        logger.info('Sent a transaction')
        time.sleep(1)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=900, poll_latency=1)
        if tx_receipt.status == 1:
            logger.success('The transaction was successfully mined')
        else:
            logger.error("Transaction failed, I'm trying again")
            self.send_message_error(self.number, message, self.address_wallet, "Transaction failed, I'm trying again")
            raise ValueError('')

        self.send_message_success(self.number, message, self.address_wallet, f'{self.scan}{tx_hash.hex()}')

        logger.success(f'[{self.number}] {message} || {self.scan}{tx_hash.hex()}\n')
        return tx_hash.hex()

    def get_gas_price(self):
        return {'maxFeePerGas': self.web3.eth.gas_price, 'maxPriorityFeePerGas': int(self.web3.eth.gas_price * 0.001)}

    def get_contract_address(self, tx_hash):
        data = self.web3.eth.get_transaction_receipt(tx_hash)
        return data['contractAddress']

    @staticmethod
    def get_api_call_data(url):
        with requests.Session() as s:
            call_data = s.get(url, timeout=6)
        if call_data.status_code < 400:
            api_data = call_data.json()
            return api_data
        else:
            logger.error("Couldn't get a response")
            raise ValueError('')

    def check_transaction_layerzero(self, tx_hash):
        while True:
            time.sleep(30)
            try:
                url = 'https://api-mainnet.layerzero-scan.com/tx/' + tx_hash
                json_data = self.get_api_call_data(url)

                if not json_data['messages']:
                    logger.info('Bridge is not over yet')
                    continue
                if json_data['messages'][0]['status'] != 'DELIVERED':
                    logger.info('Bridge is not over yet')
                    continue
                else:
                    logger.info(f'Bridge is over\n')
                    time.sleep(1)
                    print()
                    return
            except:
                continue

    def check_transaction_sepolia(self, amount):
        web3 = Web3(Web3.HTTPProvider(CHAIN_RPC['Sepolia-Base'], request_kwargs={'timeout': 60}))

        while True:
            try:
                balance = int(web3.eth.get_balance(self.address_wallet))
                logger.info(f'Balance Sepolia-Base - {Web3.from_wei(balance, "ether")}')
                if int(amount * 0.9) > balance:
                    time.sleep(100)
                    continue
                else:
                    logger.info(f'Bridge is over\n')
                    break
            except Exception as error:
                logger.error(error)
                time.sleep(10)
                continue

