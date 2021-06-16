
The repository was prepared for educational purposes by [1DES](https://1des.com). 
[How to develop a machine learning trading bot: Data Collection](https://1des.com/blog/posts/how-to-develop-machine-learning-trading-bot-data-collection)

# Goal
This code is intended to collect the stream prices of the BTC/USDT and BTC/EUR pairs on Binance and the BTC/USD and BTC/EUR pairs on Kraken.

# Setup
1 - Start with cloning the repository:

`git clone git@github.com:the1des/crypto_data_collection.git `

2- Installed all the requirements:
`pip install -r requirements.txt`

3- use the SQL queries files and make a database:
[crypto_data_collection/sql](sql)

4- make a copy of the file ".env.example" and rename it ".env", and then update the following environmental variables:
`DB_HOST=localhost
DB_USERNAME=postgres
DB_PASSWORD=YOURPASSWORD
DB_DATABASE=ohlc`

5- Run the code for Binance:
`python bin/binance.py `
And Kraken:
`python bin/kraken.py `
