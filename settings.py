
EXCEL_PASSWORD  = False                             # Если ставите пароль на Excel с приватниками || True/ False
SHUFFLE_WALLETS = True                              # Перемешка кошельков                         || True/ False

TG_BOT_SEND = False                                 # Включить уведомления в тг или нет           || True/ False
TG_TOKEN = ''                                       # API токен тг-бота - создать его можно здесь - https://t.me/BotFather
TG_ID = 0000                                        # id твоего телеграмма можно узнать тут       - https://t.me/getmyid_bot

CHAIN_RPC = {
    'Arbitrum': 'https://rpc.ankr.com/arbitrum',
    'Optimism': 'https://rpc.ankr.com/optimism',
    'Sepolia-Base': 'https://sepolia.base.org',
    'Sepolia-ETH': 'https://ethereum-sepolia-rpc.publicnode.com'
}

RETRY = 3                                           # Количество попыток при ошибках / фейлах

TIME_DELAY = [50, 100]                               # Задержка после ТРАНЗАКЦИЙ     [min, max]
TIME_ACCOUNT_DELAY = [50, 75]                       # Задержка между АККАУНТАМИ     [min, max]
TIME_DELAY_ERROR = [10, 20]                         # Задержка при ошибках / фейлах [min, max]

SEPOLIA_BRIDGE_VALUE = [0.2, 0.3, 3]          # min, max, decimal round
TESTNET_BRIDGE_VALUE = [0.00001, 0.00002, 7]  # min, max, decimal round
