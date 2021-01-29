class Wallet:
    def __init__(self, rpc):
        self.__rpc = rpc

    def abandon_transaction(self, txid: str) -> None:
        """
        Mark in-wallet transaction <txid> as abandoned This will mark this transaction and all its in-wallet
        descendants as abandoned which will allow for their inputs to be respent. It can be used to replace “stuck” or
        evicted transactions. It only works on transactions which are not included in a block and are not currently
        in the mempool. It has no effect on transactions which are already abandoned.

        Parameters
        -------
        txid : str
            The transaction id.
        """
        return self.__rpc.batch(["abandontransaction", txid])

    def abort_rescan(self) -> None:
        """
        Stops current wallet rescan triggered by an RPC call, e.g. by an importprivkey call.
        """
        return self.__rpc.batch(["abortrescan"])

    def add_multi_sig_address(self, nrequired: int, keys: list, label=None, address_type=None) -> dict:
        """
        Add a nrequired-to-sign multisignature address to the wallet. Requires a new wallet backup. Each key is
        a Bitcoin address or hex-encoded public key. This functionality is only intended for use with non-watchonly
        addresses.See importaddress for watchonly p2sh address support.If ‘label’ is specified,
        assign address to that label.

        Parameters
        -------
        nrequired : int
            The number of required signatures out of the n keys or addresses.

        keys : list
            A llist of bitcoin addresses or hex-encoded public keys

        label : str
            A label to assign the addresses to.

        address_type : str
            The address type to use. Options are “legacy”, “p2sh-segwit”, and “bech32”.

        Returns
        -------
        dict
            {
            "address":"multisigaddress",    (string) The value of the new multisig address.
            "redeemScript":"script"         (string) The string value of the hex-encoded redemption script.
            }
        """
        return self.__rpc.batch(["addmultisigaddress", nrequired, keys, label, address_type])

    def backup_wallet(self, destination: str) -> None:
        """
        Safely copies current wallet file to destination, which can be a directory or a path with filename.

        Parameters
        -------
        destination : str
            The destination directory or file
        """
        return self.__rpc.batch(["backupwallet", destination])

    def bump_fee(self, txid: str, options=None) -> dict:
        """
        Bumps the fee of an opt-in-RBF transaction T, replacing it with a new transaction B. An opt-in RBF transaction
        with the given txid must be in the wallet. The command will pay the additional fee by decreasing
        (or perhaps removing) its change output. If the change output is not big enough to cover the increased fee,
        the command will currently fail instead of adding new inputs to compensate. (A future implementation could
        improve this.) The command will fail if the wallet or mempool contains a transaction that spends one of T’s
        outputs. By default, the new fee will be calculated automatically using estimatesmartfee. The user can specify
        a confirmation target for estimatesmartfee. Alternatively, the user can specify totalFee, or use RPC settxfee
        to set a higher fee rate. At a minimum, the new fee rate must be high enough to pay an additional new relay fee
        (incrementalfee returned by getnetworkinfo) to enter the node’s mempool.

        Parameters
        -------
        txid : str
            The txid to be bumped

        options : dict
            {
            "confTarget": n,    (numeric, optional, default=fallback to wallet's default) Confirmation target
            "totalFee": n,      (numeric, optional, default=fallback to 'confTarget') Total fee (NOT feerate) to pay,
                                in satoshis. In rare cases, the actual fee paid might be slightly higher than the
                                specified totalFee if the tx change output has to be removed because it is too close to
                                the dust threshold.
            "replaceable": bool,(boolean, optional, default=true) Whether the new transaction should still be
                                marked bip-125 replaceable. If true, the sequence numbers in the transaction will
                                be left unchanged from the original. If false, any input sequence numbers in the
                                original transaction that were less than 0xfffffffe will be increased to 0xfffffffe
                                so the new transaction will not be explicitly bip-125 replaceable (though it may
                                still be replaceable in practice, for example if it has unconfirmed ancestors which
                                are replaceable).
            "estimate_mode": "str", (string, optional, default=UNSET) The fee estimate mode, must be one of:
                             "UNSET"
                             "ECONOMICAL"
                             "CONSERVATIVE"
            }

        Returns
        -------
        dict
            {
            "txid":    "value",   (string)  The id of the new transaction
            "origfee":  n,         (numeric) Fee of the replaced transaction
            "fee":      n,         (numeric) Fee of the new transaction
            "errors":  [ str... ] (json array of strings) Errors encountered during processing (may be empty)
            }
        """
        return self.__rpc.batch(["bumpfee", txid, options])

    def create_wallet(self, wallet_name: str, disable_private_keys=None, blank=None) -> dict:
        """
        Creates and loads a new wallet.

        Parameters
        -------
        wallet_name : str
            The name for the new wallet. If this is a path, the wallet will be created at the path location.

        disable_private_keys : bool
            Disable the possibility of private keys (only watchonlys are possible in this mode).

        blank : bool
            Create a blank wallet. A blank wallet has no keys or HD seed. One can be set using sethdseed.

        Returns
        -------
        dict
            {
            "name" :    <wallet_name>,      (string) The wallet name if created successfully. If the wallet was
                                            created using a full path, the wallet_name will be the full path.
            "warning" : <warning>,          (string) Warning message if wallet was not loaded cleanly.
            }
        """
        return self.__rpc.batch(["createwallet", wallet_name, disable_private_keys, blank])

    def dump_privkey(self, address: str) -> str:
        """
        Reveals the private key corresponding to ‘address’. Then the importprivkey can be used with this output

        Parameters
        -------
        address : str
            The bitcoin address for the private key.

        Returns
        -------
        str
            The private key
        """
        return self.__rpc.batch(["dumpprivkey", address])

    def dump_wallet(self, filename: str) -> dict:
        """
        Dumps all wallet keys in a human-readable format to a server-side file. This does not allow overwriting
        existing files. Imported scripts are included in the dumpfile, but corresponding BIP173 addresses, etc. may
        not be added automatically by importwallet. Note that if your wallet contains keys which are not derived from
        your HD seed (e.g. imported keys), these are not covered by only backing up the seed itself, and must be backed
        up too (e.g. ensure you back up the whole dumpfile).

        Parameters
        -------
        filename : str
            The filename with path (either absolute or relative to bitcoind).

        Returns
        -------
        dict
            {
            "filename" :        (string) The filename with full absolute path
            }
        """
        return self.__rpc.batch(["dumpwallet", filename])

    def encrypt_wallet(self, passphrase: str) -> None:
        """
        Encrypts the wallet with ‘passphrase’. This is for first time encryption. After this, any calls that interact
        with private keys such as sending or signing will require the passphrase to be set prior the making these calls.
        Use the walletpassphrase call for this, and then walletlock call. If the wallet is already encrypted,
        use the walletpassphrasechange call.

        Parameters
        -------
        passphrase : str
            The pass phrase to encrypt the wallet with. It must be at least 1 character, but should be long.
        """
        return self.__rpc.batch(["encryptwallet", passphrase])

    def get_addresses_by_label(self, label: str) -> dict:
        """
        Returns the list of addresses assigned the specified label.

        Parameters
        -------
        label : str
            The label.

        Returns
        -------
        dict
            {
            "address":
                {
                "purpose": "string" (string)  Purpose of address ("send" for sending address, "receive" for receiving
                address)
                },...
            }
        """
        return self.__rpc.batch(["getaddressesbylabel", label])

    def get_address_info(self, address: str) -> dict:
        """
        Return information about the given bitcoin address. Some information requires the address to be in the wallet.

        Parameters
        -------
        address : str
            The bitcoin address to get the information of.

        Returns
        -------
        dict
            {
            "address" : "address",        (string) The bitcoin address validated
            "scriptPubKey" : "hex",       (string) The hex-encoded scriptPubKey generated by the address
            "ismine" : true|false,        (boolean) If the address is yours or not
            "iswatchonly" : true|false,   (boolean) If the address is watchonly
            "solvable" : true|false,      (boolean) Whether we know how to spend coins sent to this address, ignoring
                                            the possible lack of private keys
            "desc" : "desc",              (string, optional) A descriptor for spending coins sent to this address
                                          (only when solvable)
            "isscript" : true|false,      (boolean) If the key is a script
            "ischange" : true|false,      (boolean) If the address was used for change output
            "iswitness" : true|false,     (boolean) If the address is a witness address
            "witness_version" : version   (numeric, optional) The version number of the witness program
            "witness_program" : "hex"     (string, optional) The hex value of the witness program
            "script" : "type"             (string, optional) The output script type. Only if "isscript" is true and
                                          the redeemscript is known. Possible types: nonstandard, pubkey, pubkeyhash,
                                          scripthash, multisig, nulldata, witness_v0_keyhash, witness_v0_scripthash,
                                          witness_unknown
            "hex" : "hex",                (string, optional) The redeemscript for the p2sh address
            "pubkeys"                     (string, optional) Array of pubkeys associated with the known redeemscript
                                          (only if "script" is "multisig")
            [
              "pubkey"
              ,...
            ]
            "sigsrequired" : xxxxx        (numeric, optional) Number of signatures required to spend multisig output
                                          (only if "script" is "multisig")
            "pubkey" : "publickeyhex",    (string, optional) The hex value of the raw public key, for single-key
                                          addresses (possibly embedded in P2SH or P2WSH)
            "embedded" : {...},           (object, optional) Information about the address embedded in P2SH or P2WSH,
                                          if relevant and known. It includes all getaddressinfo output fields for the
                                          embedded address, excluding metadata ("timestamp", "hdkeypath", "hdseedid")
                                          and relation to the wallet ("ismine", "iswatchonly").
            "iscompressed" : true|false,  (boolean, optional) If the pubkey is compressed
            "label" :  "label"            (string) The label associated with the address, "" is the default label
            "timestamp" : timestamp,      (number, optional) The creation time of the key if available in seconds since
                                          epoch (Jan 1 1970 GMT)
            "hdkeypath" : "keypath"       (string, optional) The HD keypath if the key is HD and available
            "hdseedid" : "<hash160>"      (string, optional) The Hash160 of the HD seed
            "hdmasterfingerprint" : "<hash160>" (string, optional) The fingperint of the master key.
            "labels"                      (object) Array of labels associated with the address.
            [
              { (json object of label data)
                "name": "labelname" (string) The label
                "purpose": "string" (string) Purpose of address ("send" for sending address, "receive" for receiving
                                            address)
              },...
            ]
            }
        """
        return self.__rpc.batch(["getaddressinfo", address])

    def get_balance(self, dummy=None, minconf=None, include_watchonly=None) -> int:
        """
        Returns the total available balance. The available balance is what the wallet considers currently spendable,
        and is thus affected by options which limit spendability such as -spendzeroconfchange.

        Parameters
        -------
        dummy : str
            Remains for backward compatibility. Must be excluded or set to “*”.

        minconf : str
            Only include transactions confirmed at least this many times.

        include_watchonly : bool
            Also include balance in watch-only addresses (see ‘importaddress’)

        Returns
        -------
        int
            The total amount in BTC received for this wallet.
        """
        return self.__rpc.batch(["getbalance", dummy, minconf, include_watchonly])

    def get_new_address(self, label=None, address_type=None) -> str:
        """
        Returns a new Bitcoin address for receiving payments. If ‘label’ is specified, it is added to the address
        book so payments received with the address will be associated with ‘label’.

        Parameters
        -------
        label : str
            The label name for the address to be linked to. It can also be set to the empty string “” to represent the
            default label. The label does not need to exist, it will be created if there is no label by the given name.

        address_type : str
            The address type to use. Options are “legacy”, “p2sh-segwit”, and “bech32”.

        Returns
        -------
        str
            The new bitcoin address.
        """
        return self.__rpc.batch(["getnewaddress", label, address_type])

    def get_raw_change_address(self, address_type=None) -> str:
        """
        Returns a new Bitcoin address, for receiving change. This is for use with raw transactions, NOT normal use.

        Parameters
        -------
        address_type : str
            The address type to use. Options are “legacy”, “p2sh-segwit”, and “bech32”.

        Returns
        -------
        str
            The address.
        """
        return self.__rpc.batch(["getrawchangeaddress", address_type])

    def get_received_by_address(self, address: str, minconf=None) -> int:
        """
        Returns the total amount received by the given address in transactions with at least minconf confirmations.

        Parameters
        -------
        address : str
            The bitcoin address for transactions.

        minconf : int
            Only include transactions confirmed at least this many times.

        Returns
        -------
        int
            The total amount in BTC received at this address.
        """
        return self.__rpc.batch(["getreceivedbyaddress", address, minconf])

    def get_received_by_label(self, label: str, minconf=None) -> int:
        """
        Returns the total amount received by addresses with <label> in transactions with at least [minconf]
        confirmations.

        Parameters
        -------
        label : str
            The selected label, may be the default label using “”.

        minconf : int
            Only include transactions confirmed at least this many times.

        Returns
        -------
        int
            The total amount in BTC received for this label.
        """
        return self.__rpc.batch(["getreceivedbylabel", label, minconf])

    def get_transaction(self, txid: str, include_watchonly=None) -> dict:
        """
        Get detailed information about in-wallet transaction <txid>

        Parameters
        -------
        txid : str
            The transaction id

        include_watchonly : bool
            Whether to include watch-only addresses in balance calculation and details[].

        Returns
        -------
        dict
            {
            "amount" : x.xxx,        (numeric) The transaction amount in BTC
            "fee": x.xxx,            (numeric) The amount of the fee in BTC. This is negative and only available for the
                                     'send' category of transactions.
            "confirmations" : n,     (numeric) The number of confirmations
            "blockhash" : "hash",    (string) The block hash
            "blockindex" : xx,       (numeric) The index of the transaction in the block that includes it
            "blocktime" : ttt,       (numeric) The time in seconds since epoch (1 Jan 1970 GMT)
            "txid" : "transactionid",(string) The transaction id.
            "time" : ttt,            (numeric) The transaction time in seconds since epoch (1 Jan 1970 GMT)
            "timereceived" : ttt,    (numeric) The time received in seconds since epoch (1 Jan 1970 GMT)
            "bip125-replaceable": "yes|no|unknown",  (string) Whether this transaction could be replaced due to BIP125
                                        (replace-by-fee); may be unknown for unconfirmed transactions not in the mempool
            "details" : [
            {
              "address" : "address",          (string) The bitcoin address involved in the transaction
              "category" :                    (string) The transaction category.
                           "send"             Transactions sent.
                           "receive"          Non-coinbase transactions received.
                           "generate"         Coinbase transactions received with more than 100 confirmations.
                           "immature"         Coinbase transactions received with 100 or fewer confirmations.
                           "orphan"           Orphaned coinbase transactions received.
              "amount" : x.xxx,               (numeric) The amount in BTC
              "label" : "label",              (string) A comment for the address/transaction, if any
              "vout" : n,                     (numeric) the vout value
              "fee": x.xxx,                   (numeric) The amount of the fee in BTC. This is negative and only
                                              available for the
                                              'send' category of transactions.
              "abandoned": xxx                (bool) 'true' if the transaction has been abandoned (inputs are
                                              respendable). Only available for the
                                              'send' category of transactions.
            }
            ,...
            ],
            "hex" : "data"         (string) Raw data for transaction
            }
        """
        return self.__rpc.batch(["gettransaction", txid, include_watchonly])

    def get_unconfirmed_balance(self) -> int:
        """
        Returns the server’s total unconfirmed balance

        Returns
        -------
        int
            Server’s total unconfirmed balance.
        """
        return self.__rpc.batch(["getunconfirmedbalance"])

    def get_wallet_info(self) -> dict:
        """
        Returns an object containing various wallet state info

        Returns
        -------
        dict
            {
            "walletname": xxxxx,               (string) the wallet name
            "walletversion": xxxxx,            (numeric) the wallet version
            "balance": xxxxxxx,                (numeric) the total confirmed balance of the wallet in BTC
            "unconfirmed_balance": xxx,        (numeric) the total unconfirmed balance of the wallet in BTC
            "immature_balance": xxxxxx,        (numeric) the total immature balance of the wallet in BTC
            "txcount": xxxxxxx,                (numeric) the total number of transactions in the wallet
            "keypoololdest": xxxxxx,           (numeric) the timestamp (seconds since Unix epoch) of the oldest
                                                pre-generated key in the key pool
            "keypoolsize": xxxx,               (numeric) how many new keys are pre-generated (only counts external keys)
            "keypoolsize_hd_internal": xxxx,   (numeric) how many new keys are pre-generated for internal use (used for
                                                change outputs, only appears if the wallet is using this feature,
                                                otherwise external keys are used)
            "unlocked_until": ttt,             (numeric) the timestamp in seconds since epoch (midnight Jan 1 1970 GMT)
                                                that the wallet is unlocked for transfers, or 0 if the wallet is locked
            "paytxfee": x.xxxx,                (numeric) the transaction fee configuration, set in BTC/kB
            "hdseedid": "<hash160>"            (string, optional) the Hash160 of the HD seed (only present when HD is
                                                enabled)
            "private_keys_enabled": true|false (boolean) false if privatekeys are disabled for this wallet (enforced
                                                watch-only wallet)
            }
        """
        return self.__rpc.batch(["getwalletinfo"])

    def import_address(self, address: str, label=None, rescan=None, p2sh=None) -> None:
        """
        Adds an address or script (in hex) that can be watched as if it were in your wallet but cannot be used to spend.
        Requires a new wallet backup. Note: This call can take over an hour to complete if rescan is true, during that
        time, other rpc calls may report that the imported address exists but related transactions are still missing,
        leading to temporarily incorrect/bogus balances and unspent outputs until rescan completes. If you have the
        full public key, you should call importpubkey instead of this.
        Note: If you import a non-standard raw script in hex form, outputs sending to it will be treated as change,
        and not show up in many RPCs

        Parameters
        -------
        address : str
            The Bitcoin address (or hex-encoded script).

        label : str
            An optional label.

        rescan : bool
            Rescan the wallet for transactions.

        p2sh : bool
            Add the P2SH version of the script as well
        """
        return self.__rpc.batch(["importaddress", address, label, rescan, p2sh])

    def import_multi(self, requests: list, options=None) -> list:
        """
        Import addresses/scripts (with private or public keys, redeem script (P2SH)), optionally rescanning
        the blockchain from the earliest creation time of the imported scripts. Requires a new wallet backup.
        If an address/script is imported without all of the private keys required to spend from that address, it will
        be watchonly. The ‘watchonly’ option must be set to true in this case or a warning will be returned.
        Conversely, if all the private keys are provided and the address/script is spendable, the watchonly option must
        be set to false, or a warning will be returned.
        Note: This call can take over an hour to complete if rescan is true, during that time, other rpc calls may
        report that the imported keys, addresses or scripts exists but related transactions are still missing.

        Parameters
        -------
        requests : list
            Data to be imported
            [{
            "desc": "str",          (string) Descriptor to import. If using descriptor, do not also provide
                                    address/scriptPubKey, scripts, or pubkeys
            "scriptPubKey": "<script>" | { "address":"<address>" },
                                    (string / json, required) Type of scriptPubKey (string for script, json for
                                    address). Should not be provided if using a descriptor
            "timestamp": timestamp | "now",
                                    (integer / string, required) Creation time of the key in seconds since epoch
                                    (Jan 1 1970 GMT), or the string "now" to substitute the current synced blockchain
                                    time. The timestamp of the oldest key will determine how far back blockchain rescans
                                    need to begin for missing wallet transactions. "now" can be specified to bypass
                                    scanning, for keys which are known to never have been used, and 0 can be specified
                                    to scan the entire blockchain. Blocks up to 2 hours before the earliest key
                                    creation time of all keys being imported by the importmulti call will be scanned.
            "redeemscript": "str",  (string) Allowed only if the scriptPubKey is a P2SH or P2SH-P2WSH
                                    address/scriptPubKey
            "witnessscript": "str", (string) Allowed only if the scriptPubKey is a P2SH-P2WSH or
                                    P2WSH address/scriptPubKey
            "pubkeys": [            (json array, optional, default=empty array) Array of strings giving pubkeys to
                                    import. They must occur in P2PKH or P2WPKH scripts. They are not required when the
                                    private key is also provided (see the "keys" argument).
              "pubKey",             (string)
              ...
            ],
            "keys": [               (json array, optional, default=empty array) Array of strings giving private keys
                                    to import. The corresponding public keys must occur in the output or redeemscript.
              "key",                (string)
              ...
            ],
            "range": n or [n,n],    (numeric or array) If a ranged descriptor is used, this specifies the end or the
                                    range (in the form [begin,end]) to import
            "internal": bool,       (boolean, optional, default=false) Stating whether matching outputs should be
                                    treated as not incoming payments (also known as change)
            "watchonly": bool,      (boolean, optional, default=false) Stating whether matching outputs should be
                                    considered watchonly.
            "label": "str",         (string, optional, default='') Label to assign to the address, only allowed with
                                    internal=false
            "keypool": bool,        (boolean, optional, default=false) Stating whether imported public keys should be
                                    added to the keypool for when users request new addresses. Only allowed when wallet
                                    private keys are disabled
            }]

        options : dict
            {
            "rescan": bool,         (boolean, optional, default=true) Stating if should rescan the blockchain after
                                    all imports
            }
        Returns
        -------
        list
            Response is an array with the same size as the input that has the execution result
        """
        return self.__rpc.batch(["importmulti", requests, options])

    def import_privkey(self, privkey: str, label=None, rescan=None) -> None:
        """
        Adds a private key (as returned by dumpprivkey) to your wallet. Requires a new wallet backup.
        Hint: use importmulti to import more than one private key.
        Note: This call can take over an hour to complete if rescan is true, during that time, other rpc calls may
        report that the imported key exists but related transactions are still missing, leading to temporarily
        incorrect/bogus balances and unspent outputs until rescan completes.

        Parameters
        -------
        privkey : str
            The private key (see dumpprivkey).

        label : str
            An optional label.

        rescan : bool
            Rescan the wallet for transactions.
        """
        return self.__rpc.batch(["importprivkey", privkey, label, rescan])

    def import_pruned_funds(self, rawtransaction: str, txoutproof: str) -> None:
        """
        Imports funds without rescan. Corresponding address or script must previously be included in wallet.
        Aimed towards pruned wallets. The end-user is responsible to import additional transactions that subsequently
        spend the imported outputs or rescan after the point in the blockchain the transaction is included.

        Parameters
        -------
        rawtransaction : str
            A raw transaction in hex funding an already-existing address in wallet.

        txoutproof : str
            The hex output from gettxoutproof that contains the transaction.
        """
        return self.__rpc.batch(["importprunedfunds", rawtransaction, txoutproof])

    def import_pubkey(self, pubkey: str, label=None, rescan=None) -> None:
        """
        Adds a public key (in hex) that can be watched as if it were in your wallet but cannot be used to spend.
        Requires a new wallet backup.
        Note: This call can take over an hour to complete if rescan is true, during that time, other rpc calls may
        report that the imported pubkey exists but related transactions are still missing, leading to temporarily
        incorrect/bogus balances and unspent outputs until rescan completes.

        Parameters
        -------
        pubkey : str
            The hex-encoded public key.

        label : str
            An optional label.

        rescan : bool
            Rescan the wallet for transactions.
        """
        return self.__rpc.batch(["importpubkey", pubkey, label, rescan])

    def import_wallet(self, filename: str) -> None:
        """
        Imports keys from a wallet dump file (see dumpwallet). Requires a new wallet backup to include imported keys.

        Parameters
        -------
        filename : str
            The wallet file.
        """
        return self.__rpc.batch(["importwallet", filename])

    def keypool_refill(self, newsize=None) -> None:
        """
        Fills the keypool.

        Parameters
        -------
        newsize : int
            The new keypool size.
        """
        return self.__rpc.batch(["keypoolrefill", newsize])

    def list_address_groupings(self) -> list:
        """
        Lists groups of addresses which have had their common ownership made public by common use as inputs or as
        the resulting change in past transactions

        Returns
        -------
        list
            [
                [
                    [
                      "address",            (string) The bitcoin address
                      amount,               (numeric) The amount in BTC
                      "label"               (string, optional) The label
                    ]
                    ,...
                    ]
                ,...
            ]
        """
        return self.__rpc.batch(["listaddressgroupings"])

    def list_labels(self, purpose=None) -> list:
        """
        Returns the list of all labels, or labels that are assigned to addresses with a specific purpose.

        Parameters
        -------
        purpose : str
            Address purpose to list labels for (‘send’,’receive’). An empty string is the same as not providing
            this argument.

        Returns
        -------
        list
            [
            "label",      (string) Label name
            ...
            ]
        """
        return self.__rpc.batch(["listlabels", purpose])

    def list_lock_unspent(self) -> list:
        """
        Returns list of temporarily unspendable outputs. See the lockunspent call to lock and unlock transactions
        for spending.

        Returns
        -------
        list
            [{
            "txid" : "transactionid",     (string) The transaction id locked
            "vout" : n                      (numeric) The vout value
            },...]
        """
        return self.__rpc.batch(["listlockunspent"])

    def list_received_by_address(self, minconf=None, include_empty=None, include_watchonly=None,
                                 address_filter=None) -> list:
        """
        List balances by receiving address.

        Parameters
        -------
        minconf : int
            The minimum number of confirmations before payments are included.

        include_empty : bool
            Whether to include addresses that haven’t received any payments.

        include_watchonly : bool
            Whether to include watch-only addresses (see ‘importaddress’).

        address_filter : str
            If present, only return information on this address.

        Returns
        -------
        list
            [{
            "involvesWatchonly" : true,    (bool) Only returned if imported addresses were involved in transaction
            "address" : "receivingaddress",(string) The receiving address
            "amount" : x.xxx,              (numeric) The total amount in BTC received by the address
            "confirmations" : n,           (numeric) The number of confirmations of the most recent transaction included
            "label" : "label",             (string) The label of the receiving address. The default label is "".
            "txids":
                [
               "txid",                     (string) The ids of transactions received with the address
                ...
                ]
            },...]
        """
        return self.__rpc.batch(["listreceivedbyaddress", minconf, include_empty, include_watchonly, address_filter])

    def list_received_by_label(self, minconf=None, include_empty=None, include_watchonly=None) -> dict:
        """
        List received transactions by label.

        Parameters
        -------
        minconf : int
            The minimum number of confirmations before payments are included.

        include_empty : bool
            Whether to include labels that haven’t received any payments.

        include_watchonly : bool
            Whether to include watch-only addresses (see ‘importaddress’).

        Returns
        -------
        dict
            [{
            "involvesWatchonly" : true,   (bool) Only returned if imported addresses were involved in transaction
            "amount" : x.xxx,             (numeric) The total amount received by addresses with this label
            "confirmations" : n,          (numeric) The number of confirmations of the most recent transaction included
            "label" : "label"           (string) The label of the receiving address. The default label is "".
            },...]
        """
        return self.__rpc.batch(["listreceivedbylabel", minconf, include_empty, include_watchonly])

    def list_since_block(self, blockhash=None, target_confirmations=None, include_watchonly=None,
                         include_removed=None) -> dict:
        """
        Get all transactions in blocks since block [blockhash], or all transactions if omitted. If “blockhash” is no
        longer a part of the main chain, transactions from the fork point onward are included. Additionally, if
        include_removed is set, transactions affecting the wallet which were removed are returned in the “removed”
        array.

        Parameters
        -------
        blockhash : str
            If set, the block hash to list transactions since, otherwise list all transactions.

        target_confirmations : int
            Return the nth block hash from the main chain. e.g. 1 would mean the best block hash.
            Note: this is not used as a filter, but only affects [lastblock] in the return value.

        include_watchonly : bool
            Include transactions to watch-only addresses (see ‘importaddress’).

        include_removed : bool
            Show transactions that were removed due to a reorg in the “removed” array
            (not guaranteed to work on pruned nodes).

        Returns
        -------
        dict
            {
            "transactions": [
            "address":"address",      (string) The bitcoin address of the transaction.
            "category":               (string) The transaction category.
                        "send"                  Transactions sent.
                        "receive"               Non-coinbase transactions received.
                        "generate"              Coinbase transactions received with more than 100 confirmations.
                        "immature"              Coinbase transactions received with 100 or fewer confirmations.
                        "orphan"                Orphaned coinbase transactions received.
            "amount": x.xxx,          (numeric) The amount in BTC. This is negative for the 'send' category, and is
                                                positive for all other categories
            "vout" : n,               (numeric) the vout value
            "fee": x.xxx,             (numeric) The amount of the fee in BTC. This is negative and only available for
                                                the 'send' category of transactions.
            "confirmations": n,       (numeric) The number of confirmations for the transaction.
                                                When it's < 0, it means the transaction conflicted that many blocks ago.
            "blockhash": "hashvalue", (string) The block hash containing the transaction.
            "blockindex": n,          (numeric) The index of the transaction in the block that includes it.
            "blocktime": xxx,         (numeric) The block time in seconds since epoch (1 Jan 1970 GMT).
            "txid": "transactionid",  (string) The transaction id.
            "time": xxx,              (numeric) The transaction time in seconds since epoch (Jan 1 1970 GMT).
            "timereceived": xxx,      (numeric) The time received in seconds since epoch (Jan 1 1970 GMT).
            "bip125-replaceable": "yes|no|unknown",  (string) Whether this transaction could be replaced due to BIP125
                                                     (replace-by-fee); may be unknown for unconfirmed transactions not
                                                     in the mempool
            "abandoned": xxx,       (bool) 'true' if the transaction has been abandoned (inputs are respendable).
                                    Only available for the 'send' category of transactions.
            "comment": "...",       (string) If a comment is associated with the transaction.
            "label" : "label"       (string) A comment for the address/transaction, if any
            "to": "...",            (string) If a comment to is associated with the transaction.
            ],
            "removed": [
            <structure is the same as "transactions" above, only present if include_removed=true>
            Note: transactions that were re-added in the active chain will appear as-is in this array, and may thus
            have a positive confirmation count.
            ],
            "lastblock": "lastblockhash"     (string) The hash of the block (target_confirmations-1) from the best
            block on the main chain. This is typically used to feed back into listsinceblock the next time you call it.
            So you would generally use a target_confirmations of say 6, so you will be continually re-notified of
            transactions until they've reached 6 confirmations plus any new ones
            }
        """
        return self.__rpc.batch(["listsinceblock", blockhash, target_confirmations, include_watchonly, include_removed])

    def list_transactions(self, label=None, count=None, skip=None, include_watchonly=None) -> list:
        """
        If a label name is provided, this will return only incoming transactions paying to addresses with the specified
        label. Returns up to ‘count’ most recent transactions skipping the first ‘from’ transactions.

        Parameters
        -------
        label : str
            If set, should be a valid label name to return only incoming transactions with the specified label,
            or “*” to disable filtering and return all transactions.

        count : int
            The number of transactions to return.

        skip : int
            The number of transactions to skip.

        include_watchonly : bool
            Include transactions to watch-only addresses (see ‘importaddress’).

        Returns
        -------
        list
            [{
            "address":"address",        (string) The bitcoin address of the transaction.
            "category":                 (string) The transaction category.
                        "send"                  Transactions sent.
                        "receive"               Non-coinbase transactions received.
                        "generate"              Coinbase transactions received with more than 100 confirmations.
                        "immature"              Coinbase transactions received with 100 or fewer confirmations.
                        "orphan"                Orphaned coinbase transactions received.
            "amount": x.xxx,            (numeric) The amount in BTC. This is negative for the 'send' category, and is
                                            positive for all other categories
            "label": "label",           (string) A comment for the address/transaction, if any
            "vout": n,                  (numeric) the vout value
            "fee": x.xxx,               (numeric) The amount of the fee in BTC. This is negative and only available for
                                            the 'send' category of transactions.
            "confirmations": n,         (numeric) The number of confirmations for the transaction. Negative
                                            confirmations indicate the transaction conflicts with the block chain
            "trusted": xxx,             (bool) Whether we consider the outputs of this unconfirmed transaction safe to
                                            spend.
            "blockhash": "hashvalue",   (string) The block hash containing the transaction.
            "blockindex": n,            (numeric) The index of the transaction in the block that includes it.
            "blocktime": xxx,           (numeric) The block time in seconds since epoch (1 Jan 1970 GMT).
            "txid": "transactionid",    (string) The transaction id.
            "time": xxx,                (numeric) The transaction time in seconds since epoch (midnight Jan 1 1970 GMT).
            "timereceived": xxx,        (numeric) The time received in seconds since epoch (midnight Jan 1 1970 GMT).
            "comment": "...",           (string) If a comment is associated with the transaction.
            "bip125-replaceable": "yes|no|unknown",  (string) Whether this transaction could be replaced due to BIP125
                                                        (replace-by-fee); may be unknown for unconfirmed transactions
                                                        not in the mempool
            "abandoned": xxx            (bool) 'true' if the transaction has been abandoned (inputs are respendable).
                                            Only available for the 'send' category of transactions.
            }]
        """
        return self.__rpc.batch(["listtransactions", label, count, skip, include_watchonly])

    def list_unspent(self, minconf=None, maxconf=None, addresses=None, include_unsafe=None, query_options=None) -> list:
        """
        Returns array of unspent transaction outputs with between minconf and maxconf (inclusive) confirmations.
        Optionally filter to only include txouts paid to specified addresses.

        Parameters
        -------
        minconf : int
            The minimum confirmations to filter

        maxconf : int
            The maximum confirmations to filter

        addresses : list
            A list of bitcoin addresses to filter

        include_unsafe : bool
            Include outputs that are not safe to spend. See description of “safe” attribute below.

        query_options : dict
            query options
            {
              "minimumAmount": amount,      (numeric or string, optional, default=0) Minimum value of each UTXO in BTC
              "maximumAmount": amount,      (numeric or string, optional, default=unlimited) Maximum value of each
                                                UTXO in BTC
              "maximumCount": n,            (numeric, optional, default=unlimited) Maximum number of UTXOs
              "minimumSumAmount": amount,   (numeric or string, optional, default=unlimited) Minimum sum value of all
                                                UTXOs in BTC
            }

        Returns
        -------
        list
            [{
            "txid" : "txid",          (string) the transaction id
            "vout" : n,               (numeric) the vout value
            "address" : "address",    (string) the bitcoin address
            "label" : "label",        (string) The associated label, or "" for the default label
            "scriptPubKey" : "key",   (string) the script key
            "amount" : x.xxx,         (numeric) the transaction output amount in BTC
            "confirmations" : n,      (numeric) The number of confirmations
            "redeemScript" : "script" (string) The redeemScript if scriptPubKey is P2SH
            "witnessScript" : "script" (string) witnessScript if the scriptPubKey is P2WSH or P2SH-P2WSH
            "spendable" : xxx,        (bool) Whether we have the private keys to spend this output
            "solvable" : xxx,         (bool) Whether we know how to spend this output, ignoring the lack of keys
            "desc" : xxx,             (string, only when solvable) A descriptor for spending this output
            "safe" : xxx              (bool) Whether this output is considered safe to spend. Unconfirmed transactions
                                      from outside keys and unconfirmed replacement transactions are considered unsafe
                                      and are not eligible for spending by fundrawtransaction and sendtoaddress.
            },...]
        """
        return self.__rpc.batch(["listunspent", minconf, maxconf, addresses, include_unsafe, query_options])

    def list_wallet_dir(self) -> dict:
        """
        Returns a list of wallets in the wallet directory.

        Returns
        -------
        dict
            {
            "wallets" : [
                {
                  "name" : "name"          (string) The wallet name
                }
                ,...
            ]}
        """
        return self.__rpc.batch(["listwalletdir"])

    def list_wallets(self) -> list:
        """
        Returns a list of currently loaded wallets. For full information on the wallet, use “getwalletinfo”

        Returns
        -------
        list
            [
            "walletname"            (string) the wallet name
            ...
            ]
        """
        return self.__rpc.batch(["listwallets"])

    def load_wallet(self, filename: str) -> dict:
        """
        Loads a wallet from a wallet file or directory. Note that all wallet command-line options used when starting
        bitcoind will be applied to the new wallet (eg -zapwallettxes, upgradewallet, rescan, etc).

        Parameters
        -------
        filename : str
            The wallet directory or .dat file.

        Returns
        -------
        dict
            {
            "name" :    <wallet_name>,        (string) The wallet name if loaded successfully.
            "warning" : <warning>,            (string) Warning message if wallet was not loaded cleanly.
            }
        """
        return self.__rpc.batch(["loadwallet", filename])

    def lock_unspent(self, unlock: bool, transactions=None) -> bool:
        """
        Updates list of temporarily unspendable outputs. Temporarily lock (unlock=false) or unlock (unlock=true)
        specified transaction outputs. If no transaction outputs are specified when unlocking then all current locked
        transaction outputs are unlocked. A locked transaction output will not be chosen by automatic coin selection,
        when spending bitcoins. Locks are stored in memory only. Nodes start with zero locked outputs, and the locked
        output list is always cleared (by virtue of process exit) when a node stops or fails.
        Also see the listunspent call

        Parameters
        -------
        unlock : bool
            Whether to unlock (true) or lock (false) the specified transactions.

        transactions : list
            [
                {
                    "txid": "hex",    (string, required) The transaction id
                    "vout": n,        (numeric, required) The output number
                },
            ...
            ]

        Returns
        -------
        bool
            Whether the command was successful or not.
        """
        return self.__rpc.batch(["lockunspent", unlock, transactions])

    def remove_pruned_funds(self, txid: str) -> None:
        """
        Deletes the specified transaction from the wallet. Meant for use with pruned wallets and as a companion
        to importprunedfunds. This will affect wallet balances.

        Parameters
        -------
        txid : str
            The hex-encoded id of the transaction you are deleting.
        """
        return self.__rpc.batch(["removeprunedfunds", txid])

    def rescan_blockchain(self, start_height=None, stop_height=None) -> dict:
        """
        Rescan the local blockchain for wallet related transactions.

        Parameters
        -------
        start_height : int
            Block height where the rescan should start.

        stop_height : int
            The last block height that should be scanned.
            If none is provided it will rescan up to the tip at return time of this call.

        Returns
        -------
        dict
            {
            "start_height"     (numeric) The block height where the rescan started (the requested height or 0)
            "stop_height"      (numeric) The height of the last rescanned block. May be null in rare cases if there
                                    was a reorg and the call didn't scan any blocks because they were
                                    already scanned in the background.
            }
        """
        return self.__rpc.batch(["rescanblockchain", start_height, stop_height])

    def send_many(self, dummy: str, amounts: dict, minconf=None, comment=None, subtractfeefrom=None, replaceable=None,
                  conf_target=None, estimate_mode=None) -> str:
        """
        Send multiple times. Amounts are double-precision floating point numbers.

        Parameters
        -------
        dummy : str
            Must be set to “” for backwards compatibility.

        amounts : dict
            A dict with addresses and amounts
            {
              "address": amount,    (numeric or string, required) The bitcoin address is the key,
                                    the numeric amount (can be string) in BTC is the value
            }

        minconf : int
            Only use the balance confirmed at least this many times.

        comment : str
            A comment.

        subtractfeefrom : list
            A list with addresses. The fee will be equally deducted from the amount of each selected address.
            Those recipients will receive less bitcoins than you enter in their corresponding amount field.
            If no addresses are specified here, the sender pays the fee.
            [
                "address",            (string) Subtract fee from this address
            ...
            ]

        replaceable : bool
            Allow this transaction to be replaced by a transaction with higher fees via BIP 125.

        conf_target : int
            Confirmation target (in blocks).

        estimate_mode : str
            The fee estimate mode, must be one of: “UNSET” “ECONOMICAL” “CONSERVATIVE”

        Returns
        -------
        str
            The transaction id for the send. Only 1 transaction is created.
        """
        return self.__rpc.batch(["sendmany", dummy, amounts, minconf, comment, subtractfeefrom, replaceable,
                                 conf_target, estimate_mode])

    def send_to_address(self, address: str, amount: int or str, comment=None, comment_to=None,
                        subtractfeefromamount=None,
                        replaceable=None, conf_target=None, estimate_mode=None) -> str:
        """
        Send an amount to a given address.

        Parameters
        -------
        address : str
            The bitcoin address to send to.

        amount : int or str
            The amount in BTC to send. eg 0.1

        comment : str
            A comment used to store what the transaction is for. This is not part of the transaction,
            just kept in your wallet.

        comment_to : str
            A comment to store the name of the person or organization to which you’re sending the transaction.
            This is not part of the transaction, just kept in your wallet.

        subtractfeefromamount : bool
            The fee will be deducted from the amount being sent.
            The recipient will receive less bitcoins than you enter in the amount field.

        replaceable : bool
            Allow this transaction to be replaced by a transaction with higher fees via BIP 125.

        conf_target : int
            Confirmation target (in blocks).

        estimate_mode : str
            The fee estimate mode, must be one of: “UNSET” “ECONOMICAL” “CONSERVATIVE”.

        Returns
        -------
        str
            The transaction id.
        """
        return self.__rpc.batch(["sendtoaddress", address, amount, comment, comment_to, subtractfeefromamount,
                                 replaceable, conf_target, estimate_mode])

    def set_hd_seed(self, newkeypool=None, seed=None) -> None:
        """
        Set or generate a new HD wallet seed. Non-HD wallets will not be upgraded to being a HD wallet. Wallets that
        are already HD will have a new HD seed set so that new keys added to the keypool will be derived from this
        new seed. Note that you will need to MAKE A NEW BACKUP of your wallet after setting the HD wallet seed

        Parameters
        -------
        newkeypool : bool
            Whether to flush old unused addresses, including change addresses, from the keypool and regenerate it.
            If true, the next address from getnewaddress and change address from getrawchangeaddress will be from
            this new seed. If false, addresses (including change addresses if the wallet already had HD Chain Split
            enabled) from the existing keypool will be used until it has been depleted.

        seed : str
            The WIF private key to use as the new HD seed.
            The seed value can be retrieved using the dumpwallet command. It is the private key marked hdseed=1
        """
        return self.__rpc.batch(["sethdseed", newkeypool, seed])

    def set_label(self, address: str, label: str) -> None:
        """
        Sets the label associated with the given address.

        Parameters
        -------
        address : str
            The bitcoin address to be associated with a label.

        label : str
            The label to assign to the address.
        """
        return self.__rpc.batch(["setlabel", address, label])

    def set_tx_fee(self, amount: int or str) -> bool:
        """
        Set the transaction fee per kB for this wallet. Overrides the global -paytxfee command line parameter.

        Parameters
        -------
        amount : int or str
            The transaction fee in BTC/kB.

        Returns
        -------
        bool
            Returns true if successful
        """
        return self.__rpc.batch(["settxfee", amount])

    def sign_message(self, address: str, message: str) -> str:
        """
        Sign a message with the private key of an address

        Parameters
        -------
        address : str
            The bitcoin address to use for the private key.

        message : str
            The message to create a signature of.

        Returns
        -------
        str
            The signature of the message encoded in base 64.
        """
        return self.__rpc.batch(["signmessage", address, message])

    def sign_raw_transaction_with_wallet(self, hexstring: str, prevtxs=None, sighashtype=None) -> dict:
        """
        Sign inputs for raw transaction (serialized, hex-encoded). The second optional argument (may be null) is an
        array of previous transaction outputs that this transaction depends on but may not yet be in the block chain.

        Parameters
        -------
        hexstring : str
            The transaction hex string.

        prevtxs : list
            [{
            "txid": "hex",             (string, required) The transaction id
            "vout": n,                 (numeric, required) The output number
            "scriptPubKey": "hex",     (string, required) script key
            "redeemScript": "hex",     (string) (required for P2SH) redeem script
            "witnessScript": "hex",    (string) (required for P2WSH or P2SH-P2WSH) witness script
            "amount": amount,          (numeric or string, required) The amount spent
            },...]

        sighashtype : str
            The signature hash type. Must be one of
            “ALL” “NONE” “SINGLE” “ALL|ANYONECANPAY” “NONE|ANYONECANPAY” “SINGLE|ANYONECANPAY".

        Returns
        -------
        dict
            {
            "hex" : "value",                  (string) The hex-encoded raw transaction with signature(s)
            "complete" : true|false,          (boolean) If the transaction has a complete set of signatures
            "errors" : [                      (json array of objects) Script verification errors (if there are any)
                {
                "txid" : "hash",              (string) The hash of the referenced, previous transaction
                "vout" : n,                   (numeric) The index of the output to spent and used as input
                "scriptSig" : "hex",          (string) The hex-encoded signature script
                "sequence" : n,               (numeric) Script sequence number
                "error" : "text"              (string) Verification or signing error related to the input
                }
            ,...]}
        """
        return self.__rpc.batch(["signrawtransactionwithwallet", hexstring, prevtxs, sighashtype])

    def unload_wallet(self, wallet_name=None) -> None:
        """
        Unloads the wallet referenced by the request endpoint otherwise unloads the wallet specified in the argument.
        Specifying the wallet name on a wallet endpoint is invalid.

        Parameters
        -------
        wallet_name : str
            The name of the wallet to unload.
        """
        return self.__rpc.batch(["unloadwallet", wallet_name])

    def wallet_create_funded_psbt(self, inputs: list, outputs: list, locktime=None, options=None,
                                  bip32derivs=None) -> dict:
        """
        Creates and funds a transaction in the Partially Signed Transaction format. Inputs will be added if supplied
        inputs are not enough Implements the Creator and Updater roles.

        Parameters
        -------
        inputs : list
            [{
                "txid": "hex",               (string, required) The transaction id
                "vout": n,                   (numeric, required) The output number
                "sequence": n,               (numeric, required) The sequence number
                },...]

        outputs : list
            A list of dicts with outputs (key-value pairs), where none of the keys are duplicated.
            That is, each address can only appear once and there can only be one ‘data’ object. For compatibility
            reasons, a dictionary, which holds the key-value pairs directly, is also accepted as second parameter.

            [{
                "address": amount,  (numeric or string, required) A key-value pair. The key (string) is the bitcoin
                                    address, the value (float or string) is the amount in BTC
            },
            {
                "data": "hex",      (string, required) A key-value pair. The key must be "data", the value is
                                    hex-encoded data
            },...]

        locktime : int
            Raw locktime. Non-0 value also locktime-activates inputs.

        options : dict
            “replaceable”: bool, (boolean, optional, default=false) Marks this transaction as BIP125 replaceable.
            Allows this transaction to be replaced by a transaction with higher fees “conf_target”: n, (numeric,
            optional, default=Fallback to wallet’s confirmation target) Confirmation target (in blocks)
            “estimate_mode”: “str”, (string, optional, default=UNSET) The fee estimate mode, must be one of:
            “UNSET” “ECONOMICAL” “CONSERVATIVE” }

            {
            "changeAddress": "hex",     (string, optional, default=pool address) The bitcoin address to receive
                                            the change
            "changePosition": n,        (numeric, optional, default=random) The index of the change output
            "change_type": "str",       (string, optional, default=set by -changetype) The output type to use.
                                            Only valid if changeAddress is not specified. Options are "legacy",
                                            "p2sh-segwit", and "bech32".
            "includeWatching": bool,    (boolean, optional, default=false) Also select inputs which are watch only
            "lockUnspents": bool,       (boolean, optional, default=false) Lock selected unspent outputs
            "feeRate": amount,          (numeric or string, optional, default=not set: makes wallet determine the fee)
                                            Set a specific fee rate in BTC/kB
            "subtractFeeFromOutputs": [ (list, optional, default=empty array) A json array of integers.
                                            The fee will be equally deducted from the amount of each specified output.
                                            Those recipients will receive less bitcoins than you enter in their
                                            corresponding amount field. If no outputs are specified here, the sender
                                            pays the fee.
            vout_index,                  (numeric) The zero-based output index, before a change output is added.
            ...
            ],}

        bip32derivs : bool
            If true, includes the BIP 32 derivation paths for public keys if we know them.

        Returns
        -------
        dict
            {
            "psbt": "value",        (string)  The resulting raw transaction (base64-encoded string)
            "fee":       n,         (numeric) Fee in BTC the resulting transaction pays
            "changepos": n          (numeric) The position of the added change output, or -1
            }
        """
        return self.__rpc.batch(["walletcreatefundedpsbt", inputs, outputs, locktime, options, bip32derivs])

    def wallet_lock(self) -> None:
        """
        Removes the wallet encryption key from memory, locking the wallet. After calling this method, you will need
        to call walletpassphrase again before being able to call any methods which require the wallet to be unlocked.
        """
        return self.__rpc.batch(["walletlock"])

    def wallet_passphrase(self, passphrase: str, timeout: int) -> None:
        """
        Stores the wallet decryption key in memory for ‘timeout’ seconds.
        This is needed prior to performing transactions related to private keys such as sending bitcoins Note:
        Issuing the walletpassphrase command while the wallet is already unlocked will set a new unlock time that
        overrides the old one.

        Parameters
        -------
        passphrase : str
            The wallet passphrase.

        timeout : int
            The time to keep the decryption key in seconds; capped at 100000000 (~3 years).
        """
        return self.__rpc.batch(["walletpassphrase", passphrase, timeout])

    def wallet_passphrase_change(self, oldpassphrase: str, newpassphrase: str) -> None:
        """
        Changes the wallet passphrase from ‘oldpassphrase’ to ‘newpassphrase’.

        Parameters
        -------
        oldpassphrase : str
            The current passphrase.

        newpassphrase : str
            The new passphrase.
        """
        return self.__rpc.batch(["walletpassphrasechange", oldpassphrase, newpassphrase])

    def wallet_process_psbt(self, psbt: str, sign=None, sighashtype=None, bip32derivs=None) -> dict:
        """
        Update a PSBT with input information from our wallet and then sign inputs that we can sign for.

        Parameters
        -------
        psbt : str
            The transaction base64 string.

        sign : bool
            Also sign the transaction when updating.

        sighashtype : str
            The signature hash type to sign with if not specified by the PSBT. Must be one of
            “ALL” “NONE” “SINGLE” “ALL|ANYONECANPAY” “NONE|ANYONECANPAY” “SINGLE|ANYONECANPAY”

        bip32derivs : bool
            If true, includes the BIP 32 derivation paths for public keys if we know them.

        Returns
        -------
        dict
            {
            "psbt" : "value",          (string) The base64-encoded partially signed transaction
            "complete" : true|false,   (boolean) If the transaction has a complete set of signatures
            }
        """
        return self.__rpc.batch(["walletprocesspsbt", psbt, sign, sighashtype, bip32derivs])