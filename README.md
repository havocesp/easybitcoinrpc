# Easy Bitcoin RPC

Easy Bitcoin RPC is a simple and easy to use Python library for Bitcoin RPC

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install easybitcoinrpc
```

## Usage

### Connecting

```python
from easybitcoinrpc import RPC

# RPC() returns connection object

rpc = RPC() # defaults: ip=127.0.0.1, port="8332", user="user", password="password", wallet=None

rpc = RPC(user="rpcuser", password="rpcpassword")

rpc = RPC(ip="192.168.1.1", port=9999, user="rpcuser", password="rpcpassword")

rpc = RPC(wallet="Wallet")

```

Specifing wallet when connection is made is prefered method to get access to wallet, loading wallet after connecting sometimes dosn't work.

### RPC methods

RPC object has methods for all Bitcoins RPC calls and those methods are seperated into sections as on [Bitcoin RPC API Reference](https://developer.bitcoin.org/reference/rpc/)


```python
from easybitcoinrpc import RPC
rpc = RPC()

rpc.blockchain # returns object which has all methods from blockchain category
rpc.wallet # returns object which has all methods from wallet category
rpc.util # returns object which has all methods from util category
rpc.mining # returns object which has all methods from mining category
rpc.network # returns object which has all methods from network category
rpc.generating # returns object which has all methods from generating category
rpc.control # returns object which has all methods from control category
rpc.transactions # returns object which has all methods from transactions category

rpc.batch(["getbestblockhash"]) # batch method also can be used to made requests
rpc.batch(["getblock", 1000]) # parameters are passed in list, where first parameter is RPC command
```

All methods have documentation copied from [Bitcoin RPC API Reference](https://developer.bitcoin.org/reference/rpc/), 
they also have parameters specified with their types and their default values.

### Data
Methods which implements blocks and transactions related calls, returns custom data objects like Block, Transaction, Vin, ScriptSig and etc.

```python
from easybitcoinrpc import RPC
rpc = RPC()

block = rpc.blockchain.get_best_block()
transactions = block.get_transactions()
vins = transactions[0].get_vins()
script_sig = vins[0].get_script_sig()
r = script_sig.get_r()
```

Those data objects have getters for all values.

```python
from easybitcoinrpc import RPC
rpc = RPC()

block = rpc.blockchain.get_best_block()

block.get_time()
block.get_previous_block()
block.get_hash()
```

Objects have special methods, not provided by Bitcoin RPC, like for example checking if transaction is 
segwit or getting ECDSA values.


```python
from easybitcoinrpc import RPC
rpc = RPC()

block = rpc.blockchain.get_best_block()

for t in block.get_transactions():
    if t.is_segwit():
        print(t.get_txid())
    else:
        for v in t.get_vins():
            print(t.get_txid(), v.get_sequence(), v.get_script_sig().get_r())
```

Objects have overridden str methods for better visualisation of data.

```python
from easybitcoinrpc import RPC
rpc = RPC()

block = rpc.blockchain.get_best_block()
print(block)

# Returns
# hash: 0000000000000000000a307d7eefb6ddebdd8a2737ad627f8f6d9964aeb2c29f
# confirmations: 1
# strippedsize: 977645
# size: 1066449
# weight: 3999384
# height: 669376
# version: 1073733632
# versionHex: 3fffe000
# merkleroot: 24f11777dbd32dd74ea0040dce9a12765be2683b19e05d36cd3317f0b8d1a36c
# time: 1612612936
# mediantime: 1612611893
# nonce: 1200025529
# bits: 170d21b9
# difficulty: 21434395961348.92
# chainwork: 00000000000000000000000000000000000000001910b793231a7d36bec2cf03
# nTx: 537
# previousblockhash: 00000000000000000004c1761fcc1799f11362dfdcfa3ad4ff4dbb2557dda85a
```

Transaction object has TransactionSummary object for presenting transaction like on blockchain.com.
```python
from easybitcoinrpc import RPC
rpc = RPC()

t = rpc.transactions.get_transaction('9c38bd04960abf7a77d1ce132f9ae62b37fd4509954f87b19b408141fc0cdcd6')
print(t.get_summary())

# txid: 9c38bd04960abf7a77d1ce132f9ae62b37fd4509954f87b19b408141fc0cdcd6
# hash: 6fac396e18cc20e78c9122e97c7a20e771cf754592c23cb957c9ea86a0167cd3
# inputs: 
# 	37Dynkc7bEyGkUSSWCDzKDNR2kgan2SHBw 0.00500000
# outputs: 
# 	1CrwSmssxrrXEzhx3xkK3rkYFKMoMRJkkG 0.00100000
# 	35WVXNKNswS5poxZdmbrKqPktg14iqFRNS 0.00383133
# total input: 0.00500000
# total output: 0.00483133
# fee: 0.00016867
# value now: $195.3267102094
# confirmed: True
# coinbase: False
# segwit: True
# size: 249
# vsize: 168
# weight: 669
# locktime: 0
# hex: 01000000000101df3088baec96e27ad7a597d13bcb3be0e3308824a112f1b4ced5aa1471de1c5
# 5050000001716001461f566997fabed1fccda69b37dd6ad046601d00cffffffff02a08601000000000
# 01976a914821b36b01b37d67dfb2cd405f41c9fe552ca22eb88ac9dd805000000000017a91429e2f79
# c546d089c7972da1a9754b13d0d22e164870247304402202100113c72a11389c62d8bf2a6fa612b24e
# 8582a94ad39517ab3c13ced265740022000c0a037bb72eaf447906760bb52bc4f0913e2088b4374bf5
# f1596584edcb10b0121020e6508ab2d6bcfcbce1cf1317429e5c37aa42a975319827a85fa2e0c0088f
# 62600000000
# blockhash: 000000000000000000094245acb071335f547ce5a1dba9ee47c2639d0b6d52a3
# block_height: 669377
# confirmations: 1
# time: 1612613544
# blocktime: 1612613544
# date: 2021-02-06 13:12:24

t.get_summary().get_date()
t.get_summary().get_usd_value()
t.get_summary().get_block_height()
t.get_summary().get_total_output()
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)