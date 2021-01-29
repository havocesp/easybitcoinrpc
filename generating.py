class Generating:
    def __init__(self, rpc):
        self.__rpc = rpc

    def generate(self, nblocks: int, maxtries=None) -> list:
        """
        Mine up to nblocks blocks immediately (before the RPC call returns) to an address in the wallet.

        Parameters
        -------
        nblocks : int
            How many blocks are generated immediately.

        maxtries : int
            How many iterations to try.
            default=1000000

        Returns
        -------
        list
            hashes of blocks generated
        """
        return self.__rpc.batch(["generate", nblocks, maxtries])

    def generate_to_address(self, nblocks: int, address: str, maxtries=None) -> list:
        """
        Mine blocks immediately to a specified address (before the RPC call returns)

        Parameters
        -------
        nblocks : int
            How many blocks are generated immediately.

        address : str
            The address to send the newly generated bitcoin to.

        maxtries : int
            How many iterations to try.
            default=1000000

        Returns
        -------
        list
            Hashes of blocks generated
        """
        return self.__rpc.batch(["generatetoaddress", nblocks, address, maxtries])