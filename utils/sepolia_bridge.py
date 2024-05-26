import random
from web3 import Web3
from utils.wallet import Wallet
from utils.retry import exception_handler
from loguru import logger
from settings import SEPOLIA_BRIDGE_VALUE

ABI = '''
[
  {
    "constant": false,
    "inputs": [
      {
        "name": "_to",
        "type": "address"
      },
      {
        "name": "_minGasLimit",
        "type": "uint32"
      },
      {
        "name": "_extraData",
        "type": "bytes"
      }
    ],
    "name": "bridgeETHTo",
    "outputs": [],
    "payable": true,
    "stateMutability": "payable",
    "type": "function"
  }
]
'''


class SepoliaBridge(Wallet):
    def __init__(self, private_key, number):
        super().__init__(private_key, 'Sepolia-ETH', number)
        self.address = Web3.to_checksum_address('0xfd0Bf71F60660E2f608ed56e1659C450eB113120')

    @exception_handler('Sepolia Bridge')
    def bridge(self):
        amount = round(random.uniform(SEPOLIA_BRIDGE_VALUE[0], SEPOLIA_BRIDGE_VALUE[1]), SEPOLIA_BRIDGE_VALUE[2])
        balance = self.web3.eth.get_balance(self.address_wallet)
        if balance < Web3.to_wei(amount, 'ether'):
            amount = Web3.from_wei(int(balance * 0.9), 'ether')
        logger.info(f'Sepolia bridge {amount} ETH\n')
        contract = self.web3.eth.contract(address=self.address, abi=ABI)
        txn = contract.functions.bridgeETHTo(
            self.address_wallet, 200000, '0x'
        ).build_transaction({
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'value': Web3.to_wei(amount, 'ether'),
            **self.get_gas_price()
        })

        txn['gas'] = int(txn['gas'] * 1.3)

        self.send_transaction_and_wait(txn, f'Sepolia bridge {amount} ETH || ETH -> Base')

        self.check_transaction_sepolia(Web3.to_wei(amount, 'ether'))
        