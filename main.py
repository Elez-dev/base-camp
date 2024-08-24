import random
import sys
from web3 import Web3
from utils import *
import json
from settings import *

logger.remove()
logger.add("./data/log.txt")
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <7}</level> | <cyan>{message}</cyan>")
web3_eth = Web3(Web3.HTTPProvider(CHAIN_RPC['Arbitrum'], request_kwargs={'timeout': 60}))


class Worker:

    @staticmethod
    def load_data():
        with open('./data/router.json', 'r') as f:
            return json.load(f)

    @staticmethod
    def save_progress(data):
        with open('./data/router.json', 'w') as f:
            json.dump(data, f)

        logger.success('Successfully save progress\n')

    @staticmethod
    def generate_route():
        dick = {}
        for number, key in keys_list:
            address = web3_eth.eth.account.from_key(key).address

            keys = ['quest1', 'quest2', 'quest3', 'quest4', 'quest5', 'quest6', 'quest7', 'quest8', 'quest9', 'quest10', 'quest11', 'quest12', 'quest13']
            random.shuffle(keys)

            new_routes = {key: False for key in keys}

            dick[address] = new_routes

        with open('./data/router.json', 'w') as f:
            json.dump(dick, f)

        logger.success('Successfully generated route\n')

    @staticmethod
    def check_balance_base(address_wallet):
        web3 = Wallet.get_web3('Sepolia-Base')
        balance = web3.eth.get_balance(address_wallet)
        return Web3.from_wei(balance, 'ether')

    @staticmethod
    def check_balance_sepolia(address_wallet):
        web3 = Wallet.get_web3('Sepolia-ETH')
        balance = web3.eth.get_balance(address_wallet)
        return Web3.from_wei(balance, 'ether')

    @staticmethod
    def check_balance_op_or_arb(address_wallet):
        web3_arb = Wallet.get_web3('Arbitrum')
        web3_opt = Wallet.get_web3('Optimism')
        balance_arb = web3_arb.eth.get_balance(address_wallet)
        balance_opt = web3_opt.eth.get_balance(address_wallet)
        logger.info(f'Balance optimism - {Web3.from_wei(balance_opt, "ether")} ETH')
        logger.info(f'Balance arbitrum - {Web3.from_wei(balance_arb, "ether")} ETH\n')
        if balance_arb > balance_opt:
            return 'Arbitrum', Web3.from_wei(balance_arb, 'ether')
        else:
            return 'Optimism', Web3.from_wei(balance_opt, 'ether')

    def check_balance(self, address_wallet, private_key, number):
        balance_base = self.check_balance_base(address_wallet)
        if balance_base < 0.1:
            balance_sepolia = self.check_balance_sepolia(address_wallet)
            if balance_sepolia < 0.1:
                chain, balance_op_or_arb = self.check_balance_op_or_arb(address_wallet)
                if balance_op_or_arb < TESTNET_BRIDGE_VALUE[0] + 0.000009:
                    logger.error(f'Insufficient balance, continuation is not possible\n')
                    return False

                else:
                    testnet_bridger = TestnetBridge(private_key, chain, number)
                    testnet_bridger.bridge()
                    sleeping(*TIME_DELAY)
                    sepolia_bridger = SepoliaBridge(private_key, number)
                    sepolia_bridger.bridge()
                    sleeping(*TIME_DELAY)
            else:
                sepolia_bridger = SepoliaBridge(private_key, number)
                sepolia_bridger.bridge()
                sleeping(*TIME_DELAY)
        else:
            logger.success(f'Balance on Sepolia-Base - {balance_base} ETH\n')

    def work(self):

        i = 0
        for number, key in keys_list:
            try:
                str_number = f'{number} / {all_wallets}'

                i += 1
                address = web3_eth.eth.account.from_key(key).address
                logger.info(f'Account #{i} || {address}\n')

                data = self.load_data()

                contract = CreateContract(key, str_number)
                _contract = ConfirmContract(key, str_number)
                wallet = Wallet(key, 'Sepolia-Base', str_number)

                flag = False

                for quest, complet_task in data[address].items():

                    if complet_task is False and flag is False:
                        result = self.check_balance(address, key, str_number)
                        if result is False:
                            break

                    flag = True

                    if complet_task is True:
                        continue

                    tx_hash = contract.create(quest)
                    contract_address = wallet.get_contract_address(tx_hash)
                    sleeping(*TIME_DELAY)
                    result = _contract.confirm(quest, contract_address)

                    if result is True:
                        data[address][quest] = True
                        self.save_progress(data)

                    sleeping(*TIME_DELAY)

                logger.success(f'Account completed, sleep and move on to the next one\n')
                sleeping(*TIME_ACCOUNT_DELAY)
            except Exception as error:
                logger.error(error)
                sleeping(*TIME_DELAY_ERROR)
                continue


if __name__ == '__main__':
    list1 = get_accounts_data()
    all_wallets = len(list1)
    logger.info(f'Number of wallets: {all_wallets}\n')
    keys_list = shuffle(list1)

    while True:
        while True:
            logger.info('''
    1  - GENERATE ROUTES           (сначала этот модуль -> потом 2)
    2  - RUN ROUTES
                        ''')
            time.sleep(0.1)
            act = int(input('Choose an action: '))

            if act == 1:
                Worker.generate_route()
                continue

            if act in range(1, 3):
                break

        worker = Worker()
        worker.work()
