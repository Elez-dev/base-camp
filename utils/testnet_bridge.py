import random
from web3 import Web3
from utils.wallet import Wallet
from utils.retry import exception_handler
from loguru import logger
from settings import TESTNET_BRIDGE_VALUE
import json as js


class TestnetBridge(Wallet):
    def __init__(self, private_key, chain, number):
        super().__init__(private_key, chain, number)
        if chain == 'Optimism':
            self.address = Web3.to_checksum_address('0x8352C746839699B1fc631fddc0C3a00d4AC71A17')
        else:
            self.address = Web3.to_checksum_address('0xfcA99F4B5186D4bfBDbd2C542dcA2ecA4906BA45')
        self.abi = js.load(open('./abi/testnet/abi.txt'))

    @exception_handler('Testnet Bridge')
    def bridge(self):
        amount = round(random.uniform(TESTNET_BRIDGE_VALUE[0], TESTNET_BRIDGE_VALUE[1]), TESTNET_BRIDGE_VALUE[2])
        balance = self.web3.eth.get_balance(self.address_wallet)
        if balance - Web3.to_wei(0.000009, 'ether') < Web3.to_wei(amount, 'ether'):
            amount = Web3.from_wei(balance - Web3.to_wei(0.000009, 'ether'), 'ether')
        logger.info(f'Testnet bridge {amount} ETH\n')
        contract = self.web3.eth.contract(address=self.address, abi=self.abi)
        value = Web3.to_wei(amount, 'ether')
        txn = contract.functions.swapAndBridge(
            value,
            value * 1111,
            161,
            self.address_wallet,
            self.address_wallet,
            '0x0000000000000000000000000000000000000000',
            '0x'
        ).build_transaction({
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'value': value + Web3.to_wei(0.000009, 'ether'),
            **self.get_gas_price()
        })
        tx_hash = self.send_transaction_and_wait(txn, f'Testnet bridge {amount} ETH')

        self.check_transaction_layerzero(tx_hash)
