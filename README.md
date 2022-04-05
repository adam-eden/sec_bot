# Insider trading telegram bot (for SPB-Exchange)

Bot collects insider trades from [finviz.com](https://finviz.com/insidertrading.ashx) (based on SEC Reports) and sends them to our telegram channel.
Data sorted by [SPB-Exchange tickers](https://spbexchange.ru/ru/listing/securities/list/). No OTC deals!
Useful for trading with Russian brokers.

### App Features:
1. Sorting by SPB-Exchange tickers.
2. Sorted by deals (largest to smallest).
3. Categories: sales, purchases, top owner sales (company share more than 10%), top owner purchases and more.
4. Data is sent to telegram in image format. Convenient for viewing!
5. Data for the previous day.

## Deploy

### Developed with python 3.8

1. Create a bot with BotFather. Write the API token.
2. Add a bot to your channel.
3. Clone project
4. Create and activate python virtual environment
5. Install depencies 
```bash
pip install -r requirements.txt
```
6. Fill .env-example with your data and rename it to .env
```bash
# Bot token
token_api = "***"
# Channel number -1001999999999 format
channel_id_api = "1001*********"
```
7. Run sec_bot.py

### Use crontab for Linux
```bash
# We receive information daily for the previous day at 06.55, except Sunday and Monday
55 06 * * 2-6 myvenv/bin/python myvenv/sec_bot.py
```

---
---

P.S. Just learning. Made for myself - [my telegram channel](https://t.me/neurotrading24).