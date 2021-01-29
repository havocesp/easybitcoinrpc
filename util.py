class Util:
    def __init__(self, rpc):
        self.__rpc = rpc

    def create_multisig(self, nrequired: int, keys: list, address_type=None) -> dict:
        """
        Creates a multi-signature address with n signature of m keys required.
        It returns a json object with the address and redeemScript.

        Parameters
        -------
        nrequired : int
            The number of required signatures out of the n keys.

        keys : list
            A json array of hex-encoded public keys.

        address_type : str
            The address type to use. Options are “legacy”, “p2sh-segwit”, and “bech32”.

        Returns
        -------
        dict
            Object with wultisig address and script
        """
        return self.__rpc.batch(["createmultisig", nrequired, keys, address_type])

    def derive_addresses(self, descriptor: str, range=None) -> list:
        """
        Derives one or more addresses corresponding to an output descriptor.
        Examples of output descriptors are:
        pkh(<pubkey>) P2PKH outputs for the given pubkey wpkh(<pubkey>) Native segwit P2PKH outputs for the given
        pubkey sh(multi(<n>,<pubkey>,<pubkey>,…)) P2SH-multisig outputs for the given threshold and pubkeys
        raw(<hex script>) Outputs whose scriptPubKey equals the specified hex scripts

        In the above, <pubkey> either refers to a fixed public key in hexadecimal notation, or to an xpub/xprv
        optionally followed by one or more path elements separated by “/”, where “h” represents a hardened child key.

        For more information on output descriptors, see the documentation in the doc/descriptors.md file.

        Parameters
        -------
        descriptor : str
            The descriptor.

        range : list
            If a ranged descriptor is used, this specifies the end or the range (in [begin,end] notation) to derive.

        Returns
        -------
        list
            The derived addresses
        """
        return self.__rpc.batch(["deriveaddresses", descriptor, range])

    def estimate_smart_fee(self, conf_target: int, estimate_mode=None) -> dict:
        """
        Estimates the approximate fee per kilobyte needed for a transaction to begin confirmation within conf_target
        blocks if possible and return the number of blocks for which the estimate is valid. Uses virtual transaction
        size as defined in BIP 141 (witness data is discounted).

        Parameters
        -------
        conf_target : int
            Confirmation target in blocks (1 - 1008).

        estimate_mode : str
            The fee estimate mode. Whether to return a more conservative estimate which also satisfies a longer history.
            A conservative estimate potentially returns a higher feerate and is more likely to be sufficient for the
             desired target, but is not as responsive to short term drops in the prevailing fee market.
             Must be one of: “UNSET” “ECONOMICAL” “CONSERVATIVE”

        Returns
        -------
        dict
            Object with feerate, errors and blocks.
        """
        return self.__rpc.batch(["estimatesmartfee", conf_target, estimate_mode])

    def get_descriptor_info(self, descriptor: str) -> dict:
        """
        Analyses a descriptor.

        Parameters
        -------
        descriptor : str
            The descriptor.

        Returns
        -------
        dict
            {
            "descriptor" : "desc",         (string) The descriptor in canonical form, without private keys
            "isrange" : true|false,        (boolean) Whether the descriptor is ranged
            "issolvable" : true|false,     (boolean) Whether the descriptor is solvable
            "hasprivatekeys" : true|false, (boolean) Whether the input descriptor contained at least one private key
            }
        """
        return self.__rpc.batch(["getdescriptorinfo", descriptor])

    def sign_message_with_privkey(self, privkey: str, message: str) -> str:
        """
        Sign a message with the private key of an address.

        Parameters
        -------
        privkey : str
            The private key to sign the message with.

        message : str
            The message to create a signature of.

        Returns
        -------
        str
            The signature of the message encoded in base 64.
        """
        return self.__rpc.batch(["signmessagewithprivkey", privkey, message])

    def validate_address(self, address: str) -> dict:
        """
        Return information about the given bitcoin address.

        Parameters
        -------
        address : str
            The bitcoin address to validate

        Returns
        -------
        dict
            {
            "isvalid" : true|false,       (boolean) If the address is valid or not. If not, this is the only property returned.
            "address" : "address",        (string) The bitcoin address validated
            "scriptPubKey" : "hex",       (string) The hex-encoded scriptPubKey generated by the address
            "isscript" : true|false,      (boolean) If the key is a script
            "iswitness" : true|false,     (boolean) If the address is a witness address
            "witness_version" : version   (numeric, optional) The version number of the witness program
            "witness_program" : "hex"     (string, optional) The hex value of the witness program
            }

        """
        return self.__rpc.batch(["validateaddress", address])

    def verify_message(self, address: str, signature: str, message: str) -> bool:
        """
        Verify a signed message.

        Parameters
        -------
        address : str
            The bitcoin address to use for the signature.

        signature : str
            The signature provided by the signer in base 64 encoding (see signmessage).

        message : str
            The message that was signed.

        Returns
        -------
        bool
            The message that was signed.
        """
        return self.__rpc.batch(["verifymessage", address, signature, message])