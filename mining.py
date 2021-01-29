class Mining:
    def __init__(self, rpc):
        self.__rpc = rpc

    def get_block_template(self, template_request=None) -> dict:
        """
        If the request parameters include a ‘mode’ key, that is used to explicitly select between the default
        ‘template’ request or a ‘proposal’.
        It returns data needed to construct a block to work on.
        For full specification, see BIPs 22, 23, 9, and 145:

        Parameters
        -------
        template_request : dict
            A json object in the following spec
            “rules”: [ (json array, required) A list of strings “support”, (string) client side supported softfork
            deployment … ], }

        Returns
        -------
        dict
            Data needed to construct a block to work on.
        """
        return self.__rpc.batch(["getblocktemplate", template_request])

    def get_mining_info(self) -> dict:
        """
        Returns a json object containing mining-related information.

        Returns
        -------
        dict
            Dining-related information
        """
        return self.__rpc.batch(["getmininginfo"])

    def get_network_hash_ps(self, nblocks=None, height=None) -> int:
        """
        Returns the estimated network hashes per second based on the last n blocks.
        Pass in [blocks] to override # of blocks, -1 specifies since last difficulty change.
        Pass in [height] to estimate the network speed at the time when a certain block was found.

        Parameters
        -------
        nblocks : int
            The number of blocks, or -1 for blocks since last difficulty change.

        height : int
            To estimate at the time of the given height.

        Returns
        -------
        int
            Hashes per second estimated.
        """
        return self.__rpc.batch(["getnetworkhashps", nblocks, height])

    def prioritise_transaction(self, txid: str, dummy=None, fee_delta=None) -> bool:
        """
        Accepts the transaction into mined blocks at a higher (or lower) priority

        Parameters
        -------
        txid : int
            The transaction id.

        dummy : int
            API-Compatibility for previous API. Must be zero or null.
            DEPRECATED. For forward compatibility use named arguments and omit this parameter.

        fee_delta : int
            The fee value (in satoshis) to add (or subtract, if negative).
            Note, that this value is not a fee rate. It is a value to modify absolute fee of the TX.
            The fee is not actually paid, only the algorithm for selecting transactions into a block considers
            the transaction as it would have paid a higher (or lower) fee

        Returns
        -------
        bool
            Returns true
        """
        return self.__rpc.batch(["prioritisetransaction", txid, dummy, fee_delta])

    def submit_block(self, hexdata: str, dummy=None) -> None:
        """
        Attempts to submit new block to network.

        Parameters
        -------
        hexdata : str
            The hex-encoded block data to submit.

        dummy : str
            Dummy value, for compatibility with BIP22. This value is ignored..

        """
        return self.__rpc.batch(["submitblock", hexdata, dummy])

    def submit_header(self, hexdata: str) -> None:
        """
        Decode the given hexdata as a header and submit it as a candidate chain tip if valid.
        Throws when the header is invalid.

        Parameters
        -------
        hexdata : str
            The hex-encoded block header data.

        """
        return self.__rpc.batch(["submitheader", hexdata])