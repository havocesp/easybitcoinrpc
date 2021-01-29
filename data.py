from datetime import datetime
import cryptocompare

code_strings = {
    2: '01',
    10: '0123456789',
    16: '0123456789abcdef',
    32: 'abcdefghijklmnopqrstuvwxyz234567',
    58: '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz',
    256: ''.join([chr(x) for x in range(256)])
}


def get_code_string(base):
    if base in code_strings:
        return code_strings[base]
    else:
        raise ValueError("Invalid base!")


def decode(string, base):
    if base == 256 and isinstance(string, str):
        string = bytes(bytearray.fromhex(string))
    base = int(base)
    code_string = get_code_string(base)
    result = 0
    if base == 256:
        def extract(d, cs):
            return d
    else:
        def extract(d, cs):
            return cs.find(d if isinstance(d, str) else chr(d))

    if base == 16:
        string = string.lower()
    while len(string) > 0:
        result *= base
        result += extract(string[0], code_string)
        string = string[1:]
    return result


class Block:
    def __init__(self, rpc, block, transactions=None):
        self.__rpc = rpc
        self.__block = block
        self.__transactions = transactions

    def __str__(self):

        string = "hash: " + self.get_hash() + "\n" + \
                 "confirmations: " + str(self.get_confirmations()) + "\n" + \
                 "strippedsize: " + str(self.get_stripped_size()) + "\n" + \
                 "size: " + str(self.get_size()) + "\n" + \
                 "weight: " + str(self.get_weight()) + "\n" + \
                 "height: " + str(self.get_height()) + "\n" + \
                 "version: " + str(self.get_version()) + "\n" + \
                 "versionHex: " + self.get_version_hex() + "\n" + \
                 "merkleroot: " + self.get_merkleroot() + "\n" + \
                 "time: " + str(self.get_time()) + "\n" + \
                 "mediantime: " + str(self.get_mediant_time()) + "\n" + \
                 "nonce: " + str(self.get_nonce()) + "\n" + \
                 "bits: " + self.get_bits() + "\n" + \
                 "difficulty: " + str(self.get_difficulty()) + "\n" + \
                 "chainwork: " + self.get_chainwork() + "\n" + \
                 "nTx: " + str(self.get_nTx()) + "\n"

        if self.get_previous_block_hash():
            string += "previousblockhash: " + self.get_previous_block_hash() + "\n"

        if self.get_next_block_hash():
            string += "nextblockhash:" + self.get_next_block_hash() + "\n"

        return string

    def __getitem__(self, item):
        try:
            return self.__block[item]
        except KeyError:
            return None

    def get_raw(self):
        return self.__block

    def get_hash(self):
        return self['hash']

    def get_confirmations(self):
        return self['confirmations']

    def get_stripped_size(self):
        return self['strippedsize']

    def get_size(self):
        return self['size']

    def get_weight(self):
        return self['weight']

    def get_height(self):
        return self['height']

    def get_version(self):
        return self['version']

    def get_version_hex(self):
        return self['versionHex']

    def get_merkleroot(self):
        return self['merkleroot']

    def get_txs(self):
        return self['tx']

    def get_transactions(self):
        if self.__transactions is None:
            self.__transactions = [self.__rpc.transactions.get_transaction(txid) for txid in self.get_txs()]
        return self.__transactions

    def get_time(self):
        return self['time']

    def get_mediant_time(self):
        return self['mediantime']

    def get_nonce(self):
        return self['nonce']

    def get_bits(self):
        return self['bits']

    def get_difficulty(self):
        return self['difficulty']

    def get_chainwork(self):
        return self['chainwork']

    def get_nTx(self):
        return self['nTx']

    def get_previous_block_hash(self):
        return self['previousblockhash']

    def get_previous_block(self):
        return self.__rpc.blockchain.get_block(self.get_previous_block_hash())

    def get_next_block_hash(self):
        return self['nextblockhash']

    def get_next_block(self):
        return self.__rpc.blockchain.get_block(self.get_next_block_hash())


class Transaction:
    def __init__(self, rpc, tx):
        self.__rpc = rpc
        self.__tx = tx

        self.__vins = [Vin(vin) for vin in self.get_vin()]
        self.__vouts = [Vout(vout) for vout in self.get_vout()]
        self.__summary = None

    def __str__(self):
        string = "txid: " + self.get_txid() + "\n" + \
                 "hash: " + self.get_hash() + "\n" + \
                 "confirmed: " + str(self.is_confirmed()) + "\n" + \
                 "coinbase: " + str(self.is_coinbase()) + "\n" + \
                 "segwit: " + str(self.is_segwit()) + "\n" + \
                 "size: " + str(self.get_size()) + "\n" + \
                 "vsize: " + str(self.get_vsize()) + "\n" + \
                 "weight: " + str(self.get_weight()) + "\n" + \
                 "locktime: " + str(self.get_locktime()) + "\n"

        string += "vin: "

        for v in self.get_vins():
            string += "\n\t" + str(v).replace("\n", "\n\t") + "\n"

        string += "vout: "

        for v in self.get_vouts():
            string += "\n\t" + str(v).replace("\n", "\n\t") + "\n"

        string += "hex: " + str(self.get_hex()) + "\n"

        if self.is_confirmed():
            string += "blockhash: " + str(self.get_block_hash()) + "\n" + \
                      "confirmations: " + str(self.get_confirmations()) + "\n" + \
                      "time: " + str(self.get_time()) + "\n" + \
                      "blocktime: " + str(self.get_block_time())

        return string

    def __getitem__(self, item):
        try:
            return self.__tx[item]
        except KeyError:
            return None

    def get_raw(self):
        return self.__tx

    def get_txid(self):
        return self['txid']

    def get_hash(self):
        return self['hash']

    def get_version(self):
        return self['version']

    def get_size(self):
        return self['size']

    def get_vsize(self):
        return self['vsize']

    def get_weight(self):
        return self['weight']

    def get_locktime(self):
        return self['locktime']

    def get_vin(self):
        return self['vin']

    def get_vins(self):
        return self.__vins

    def get_vout(self):
        return self['vout']

    def get_vouts(self):
        return self.__vouts

    def get_hex(self):
        return self['hex']

    def get_block_hash(self):
        return self['blockhash']

    def get_confirmations(self):
        return self['confirmations']

    def get_time(self):
        return self['time']

    def get_block_time(self):
        return self['blocktime']

    def is_segwit(self):
        return self.__vins[0].is_segwit()

    def is_coinbase(self):
        return self.__vins[0].is_coinbase()

    def is_confirmed(self):
        return 'confirmations' in self.__tx

    def get_summary(self):
        if self.__summary is None:
            self.__summary = TransactionSummary(self.__rpc, self)
        return self.__summary


class TransactionSummary:
    def __init__(self, rpc, transaction):
        self.__rpc = rpc
        self.__transaction = transaction
        self.__inputs = []
        self.__outputs = []

        for vin in transaction.get_vins():
            txid = vin.get_txid()
            n = vin.get_vout()
            _input = rpc.transactions.get_transaction(txid)
            value = float(_input.get_vouts()[n].get_value())
            addresses = _input.get_vouts()[n].get_script_pubkey().get_addresses()
            for a in addresses:
                self.__inputs.append([a, value / len(addresses)])

        for vout in transaction.get_vouts():
            value = float(vout.get_value())
            addresses = vout.get_script_pubkey().get_addresses()
            for a in addresses:
                self.__outputs.append([a, value / len(addresses)])

        self.__total_input = sum([_input[1] for _input in self.__inputs])
        self.__total_output = sum([_output[1] for _output in self.__outputs])
        self.__fee = self.__total_input - self.__total_output
        if self.__transaction.get_time():
            self.__date = datetime.fromtimestamp(self.__transaction.get_time())

        if self.__transaction.get_block_hash():
            self.__block_height = rpc.blockchain.get_block(transaction.get_block_hash()).get_height()

    def __str__(self):
        string = "txid: " + self.__transaction.get_txid() + "\n" + \
                 "hash: " + self.__transaction.get_hash() + "\n" + \
                 "inputs: " + "\n"

        for _input in self.get_inputs():
            string += "\t" + str(_input[0]) + " " + "{:.8f}".format(_input[1]) + "\n"

        string += "outputs: " + "\n"

        for _output in self.get_outputs():
            string += "\t" + str(_output[0]) + " " + "{:.8f}".format(_output[1]) + "\n"

        string += "total input: " + "{:.8f}".format(self.get_total_input()) + "\n" + \
                  "total output: " + "{:.8f}".format(self.get_total_output()) + "\n" + \
                  "fee: " + "{:.8f}".format(self.get_fee()) + "\n" + \
                  "value now: $" + str(self.get_usd_value()) + "\n"

        string += "confirmed: " + str(self.__transaction.is_confirmed()) + "\n" + \
                  "coinbase: " + str(self.__transaction.is_coinbase()) + "\n" + \
                  "segwit: " + str(self.__transaction.is_segwit()) + "\n" + \
                  "size: " + str(self.__transaction.get_size()) + "\n" + \
                  "vsize: " + str(self.__transaction.get_vsize()) + "\n" + \
                  "weight: " + str(self.__transaction.get_weight()) + "\n" + \
                  "locktime: " + str(self.__transaction.get_locktime()) + "\n"

        string += "hex: " + str(self.__transaction.get_hex()) + "\n"

        if self.__transaction.is_confirmed():
            string += "blockhash: " + str(self.__transaction.get_block_hash()) + "\n" + \
                      "block_height: " + str(self.get_block_height()) + "\n" \
                                                                        "confirmations: " + str(
                self.__transaction.get_confirmations()) + "\n" + \
                      "time: " + str(self.__transaction.get_time()) + "\n" + \
                      "blocktime: " + str(self.__transaction.get_block_time()) + "\n" + \
                      "date: " + str(self.get_date())
        return string

    def get_inputs(self):
        return self.__inputs

    def get_outputs(self):
        return self.__outputs

    def get_total_input(self):
        return self.__total_input

    def get_total_output(self):
        return self.__total_output

    def get_fee(self):
        return self.__fee

    def get_date(self):
        return self.__date

    def get_block_height(self):
        return self.__block_height

    def get_usd_value(self):
        return cryptocompare.get_price('BTC', curr='USD').get('BTC').get('USD') * self.__total_output


class Vin:
    def __init__(self, vin):
        self.__vin = vin

    def __str__(self):

        string = ""
        if not self.is_coinbase():
            string += "txid: " + self.get_txid() + "\n" + \
                      "vout: " + str(self.get_vout()) + "\n"

            if self.get_script_sig().get_asm() != "":
                string += "scriptSig: " + "\n\t" + str(self.get_script_sig()).replace("\n", "\n\t") + "\n"

            if self.get_txin_witness():
                string += "txinwitness: " + "\n"
                for witness in self.get_txin_witness():
                    if witness != "":
                        string += "\t" + witness + "\n"
        else:
            string += "coinbase: " + self.get_coinbase() + "\n"

        string += "sequence: " + str(self.get_sequence())

        return string

    def __getitem__(self, item):
        if item in self.__vin:
            return self.__vin[item]
        else:
            return None

    def get_raw(self):
        return self.__vin

    def get_txid(self):
        return self['txid']

    def get_vout(self):
        return self['vout']

    def get_script_sig(self):
        return ScriptSig(self['scriptSig'])

    def get_txin_witness(self):
        return self['txinwitness']

    def get_sequence(self):
        return self['sequence']

    def get_coinbase(self):
        return self['coinbase']

    def is_segwit(self):
        return 'txinwitness' in self.__vin

    def is_coinbase(self):
        return 'coinbase' in self.__vin


class ScriptSig:
    def __init__(self, script_sig):
        self.__script_sig = script_sig

    def __str__(self):
        string = "asm: " + self.get_asm().replace(" ", "\n\t") + "\n" + "hex: " + self.get_hex()
        return string

    def __getitem__(self, item):
        return self.__script_sig[item]

    def get_raw(self):
        return self.__script_sig

    def get_asm(self):
        return self['asm']

    def get_hex(self):
        return self['hex']

    def get_r(self):
        sig = self.get_asm()
        if '[' in sig:
            sig = sig[:sig.index('[')]
            left = sig[8:8 + decode(sig[6:8], 16) * 2]
            return HexDecValue(left)
        else:
            return None

    def get_s(self):
        sig = self.get_asm()
        if '[' in sig:
            leftlen = decode(sig[6:8], 16) * 2
            rightlen = decode(sig[10 + leftlen:12 + leftlen], 16) * 2
            right = sig[12 + leftlen:12 + leftlen + rightlen]
            return right
        else:
            return None


class Vout:
    def __init__(self, vout):
        self.__vout = vout

    def __str__(self):
        string = "value: " + str(self.get_value()) + "\n" + \
                 "n: " + str(self.get_n()) + "\n" + \
                 "scriptPubKey:" + "\n\t" + str(self.get_script_pubkey()).replace("\n", "\n\t")

        return string

    def __getitem__(self, item):
        return self.__vout[item]

    def get_raw(self):
        return self.__vout

    def get_value(self):
        return self['value']

    def get_n(self):
        return self['n']

    def get_script_pubkey(self):
        return ScriptPubKey(self['scriptPubKey'])


class ScriptPubKey:
    def __init__(self, script_pubkey):
        self.__script_pubkey = script_pubkey

    def __str__(self):

        string = "asm: " + self.get_asm() + "\n" + \
                 "hex: " + self.get_hex() + "\n" + \
                 "type: " + self.get_type() + "\n"

        string += "reqSigs: " + str(self.get_req_sigs())
        if self.get_addresses():
            string += "\n" + "addresses: "
            for address in self.get_addresses():
                string += "\n\t" + address

        return string

    def __getitem__(self, item):
        try:
            return self.__script_pubkey[item]
        except KeyError:
            return None

    def get_raw(self):
        return self.__script_pubkey

    def get_asm(self):
        return self['asm']

    def get_hex(self):
        return self['hex']

    def get_req_sigs(self):
        return self['reqSigs']

    def get_type(self):
        return self['type']

    def get_addresses(self):
        return self['addresses']


class HexDecValue:
    def __init__(self, hex_value):
        self.__hex = hex_value
        self.__dec = decode(hex_value, 16)

    def __str__(self):
        return str(self.__hex)

    def hex(self):
        return self.__hex

    def dec(self):
        return self.__dec
