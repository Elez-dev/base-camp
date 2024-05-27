[![Telegram channel](https://img.shields.io/endpoint?url=https://runkit.io/damiankrawczyk/telegram-badge/branches/master?url=https://t.me/developercode1)](https://t.me/developercode1)
[![PyPI supported Python versions](https://img.shields.io/badge/Python%203.10.10-8A2BE2)](https://www.python.org/downloads/release/python-31010/)

<div align="center">
  <img src="https://img3.teletype.in/files/a1/93/a1937ace-765d-4886-87b4-00c6c1b41f0a.png"  />
  <h1>BASE CAMP SOFT</h1>
  <p>Софт на BASE CAMP - позволяет с легкостью задеплоить 13 контрактов для получения ролей на Guild.xyz</p>
</div>

---

🤠👉 <b>Наш канал:</b> [PYTHON DAO](https://t.me/developercode1)

---
<h2>🙊 INFO</h2>

Для работы нужен [Python 3.10.10](https://www.python.org/downloads/release/python-31010/)

В данном гайде подробно описано как установить Python - [link](https://mirror.xyz/wiedzmin.eth/Z06W81VrxO9KI88vkcxeW0Lc8f2nBo5Wdyqce0HTNm8)

Софт нужен для деплоя 13 контрактов и порлучения за них 5 ролей в [гильдии BASE](https://guild.xyz/base/base-camp) 

Плюс, за это нам дадут 9 поинтов в [Talent Protocol Passport](https://teletype.in/@svalkadao/TalentProtocol)


<b>Софт работает по такой логике:</b>
1. Из ARB/OP ETH мы бриджим в Ethereum Sepolia testnet - [testnetbridge.com](https://testnetbridge.com/sepolia)
2. Затем полученный ETH Sepolia мы бриджим в Base Sepolia - [orbiter.finance](https://rinkeby.orbiter.finance/?source=Sepolia&dest=Base%20Sepolia&token=ETH)
3. Начинаем деплоить контракты
4. После завершения работы, останется только зайти на [guild.xyz/base/base-camp](https://guild.xyz/base/base-camp) и забрать роли

А если вы как и мы фармите [Build.top](https://www.build.top/) - можете номинировать нас: [@elez-dev](https://www.build.top/nominate/0xac5d3f9f74c77821b624ec0830481e0608974ff7) и [@denis](https://www.build.top/nominate/0x13a5e7BdE7477616C953ac4d4a1A82F751053efb)

---
В папке _data_ заполняем Excel файл с приватными ключами

Все настройки происходят в файле _settings.py_ - каждая строчка подписана

---
<h2>🚀 УСТАНОВКА СОФТА</h2>

```
git clone https://github.com/Elez-dev/base-camp.git

cd base-camp-master

pip3.10 install -r requirements.txt

python3.10 main.py
```
---
<h2>🤖 ВОЗМОЖНОСТИ СОФТА:</h2>

```

1  - GENERATE ROUTES           (сначала этот модуль -> потом 2)

2  - RUN ROUTES                (всё это для рандомизации деплоя контрактов)

```
---
<h2>❤️ По всем вопросам в наш чат - https://t.me/pythondao</h2>
