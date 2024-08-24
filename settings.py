
EXCEL_PASSWORD  = False                           # Установить пароль на Excel файл с приватными ключами  || True/False
SHUFFLE_WALLETS = True                            # Перемешивать кошельки перед выполнением операций      || True/False

TG_BOT_SEND = False                               # Включить уведомления в Telegram или нет               || True/False
TG_TOKEN = ''                                     # API токен для Telegram-бота - можно создать здесь     - https://t.me/BotFather
TG_ID = 0000                                      # ID вашего Telegram можно узнать здесь                 - https://t.me/getmyid_bot

CHAIN_RPC = {
    'Arbitrum': 'https://rpc.zerion.io/v1/arbitrum',
    'Optimism': 'https://rpc.zerion.io/v1/optimism',
    'Sepolia-Base': 'https://sepolia.base.org',
    'Sepolia-ETH': 'https://ethereum-sepolia-rpc.publicnode.com'
}

RETRY = 3                                         # Количество попыток при возникновении ошибок/сбоев

TIME_DELAY = [50, 100]                            # Задержка после транзакций (в секундах)                [мин, макс]
TIME_ACCOUNT_DELAY = [250, 275]                   # Задержка между аккаунтами                             [мин, макс]
TIME_DELAY_ERROR = [10, 20]                       # Задержка при возникновении ошибок/сбоев               [мин, макс]

TESTNET_BRIDGE_VALUE = [0.00001, 0.00002, 7]      # Количество ETH для testnetbridge.com : минимальное, максимальное и количество десятичных знаков
SEPOLIA_BRIDGE_VALUE = [0.2, 0.3, 3]              # Количество ETH для моста ETH Sepolia -> Base Sepolia: минимальное, максимальное и количество десятичных знаков
