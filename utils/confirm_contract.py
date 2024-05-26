from utils.wallet import Wallet
from utils.retry import exception_handler
from web3 import Web3
from loguru import logger

address_confirm = {
    'quest1': {
        'address': '0x075eb9dc52177aa3492e1d26f0fde3d729625d2f',
        'description': 'Deploy a testnet'
    },

    'quest2': {
        'address': '0xF4D953A3976F392aA5509612DEfF395983f22a84',
        'description': 'Control Structures'
    },

    'quest3': {
        'address': '0x567452C6638c0D2D9778C20a3D59749FDCaa7aB3',
        'description': 'Storage in solidity'
    },

    'quest4': {
        'address': '0x5B0F80cA6f5bD60Cc3b64F0377f336B2B2A56CdF',
        'description': 'Arrays in solidity'
    },

    'quest5': {
        'address': '0xD32E3ACe3272e2037003Ca54CA7E5676f9b8D06C',
        'description': 'The mapping type'
    },

    'quest6': {
        'address': '0x9eB1Fa4cD9bd29ca2C8e72217a642811c1F6176d',
        'description': 'Structs'
    },

    'quest7': {
        'address': '0xF90dA05e77a33Fe6D64bc2Df84e7dd0069A2111C',
        'description': 'Inheritance Exercise'
    },

    'quest8': {
        'address': '0x8dD188Ec36084D59948F90213AFCd04429E33c0c',
        'description': 'Imports'
    },

    'quest9': {
        'address': '0xC1BD0d9A8863f2318001BC5024c7f5F58a2236F7',
        'description': 'Errors'
    },

    'quest10': {
        'address': '0x4f21e69d0CDE8C21cF82a6b37Dda5444716AFA46',
        'description': 'The new keyword'
    },

    'quest11': {
        'address': '0x10Ce928030E136EcC74d4a4416Db9b533e3c694D',
        'description': 'Minimal Tokens Exercise'
    },

    'quest12': {
        'address': '0x4F333c49B820013e5E6Fe86634DC4Da88039CE50',
        'description': 'Create ERC-20 token'
    },

    'quest13': {
        'address': '0x15534ED3d1dBA55148695B2Ba4164F147E47a10c',
        'description': 'Create ERC-721 token'
    },

}


class ConfirmContract(Wallet):
    def __init__(self, private_key, number):
        super().__init__(private_key, 'Sepolia-Base', number)

    @exception_handler('Test contract')
    def confirm(self, quest, address_contract):
        logger.info('Test contract\n')
        data = f'0x06d82f29000000000000000000000000' + address_contract[2:]
        tx = {
            'chainId': 84532,
            'from': self.address_wallet,
            'to': Web3.to_checksum_address(address_confirm[quest]['address']),
            'data': data,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }
        tx['gas'] = self.web3.eth.estimate_gas(tx)
        self.send_transaction_and_wait(tx, f'{address_confirm[quest]["description"]} quest complete')
        return True
