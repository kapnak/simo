# SiMo

A trading bot made in Python.

## Strategy

The strategy used will not be described there but it very simple, stats-based and back-tested.


## How to use ?

**1 - Have a Binance account**  
[Click to see how to create API key on Binance.  ](https://www.binance.com/en/support/faq/how-to-create-api-keys-on-binance-360002502072)  
Other exchanges will be added.  
Feel free to suggest new exchange or to add it by yourself.


**2 - Clone the git**
```bash
git clone https://github.com/kapnak/simo
```


**3 - Setup accounts**  
Create file in `simo/data/user/` directory in the following format :
```
Binance
<key>
<token>
enable
```
You can set up multiple accounts by creating many files.


**4 - Install venv & requirements**

```bash
python3 -m pip install -r requirements.txt
```

**5 - Start the bot**  
Make sure that your account is funded with at least 10 FDUSD (for Binance).

Start with :
```bash
python3 main.py
```


## Note

The program is currently being tested and is not safe.  
⚠️ Use at your own risks.


## Contact & Donate

Discord : **kapnak**  
Mail : **kapnak.mail@gmail.com**

Monero (XMR) : 
```
444DEqjmWnuiiyuzxAPYwdQgcujJU1UYFAomsdS77wRE9ooPLcmEyqsLtNC11C5bMWPif5gcc7o6gMFXvvQQEbVVN6CNnBT
```
