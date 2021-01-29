from bitcoinrpc.authproxy import AuthServiceProxy
from easybitcoinrpc.blockchain import Blockchain
from easybitcoinrpc.control import Control
from easybitcoinrpc.generating import Generating
from easybitcoinrpc.mining import Mining
from easybitcoinrpc.network import Network
from easybitcoinrpc.raw_transactions import RawTransactions
from easybitcoinrpc.util import Util
from easybitcoinrpc.wallet import Wallet


class RPC:
    def __init__(self, ip='127.0.0.1', port='8332', user='user', password='password', wallet=None):
        port = str(port)
        if wallet:
            self.__url = 'http://%s:%s@%s:%s/wallet/%s' % (user, password, ip, port, wallet)
        else:
            self.__url = 'http://%s:%s@%s:%s' % (user, password, ip, port)

        self.__rpc = AuthServiceProxy(self.__url)

        self.blockchain = Blockchain(self)
        self.control = Control(self)
        self.generating = Generating(self)
        self.mining = Mining(self)
        self.network = Network(self)
        self.transactions = RawTransactions(self)
        self.util = Util(self)
        self.wallet = Wallet(self)

    def batch(self, command):
        return self.__rpc.batch_([command])[0]
