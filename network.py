class Network:
    def __init__(self, rpc):
        self.__rpc = rpc

    def add_node(self, node: str, command: str) -> None:
        """
        Attempts to add or remove a node from the addnode list. Or try a connection to a node once.
        Nodes added using addnode (or -connect) are protected from DoS disconnection and are not required to be
        full nodes/support SegWit as other outbound peers are (though such peers will not be synced from)

        Parameters
        -------
        node : str
            The node (see getpeerinfo for nodes)

        command : st
            ‘add’ to add a node to the list, ‘remove’ to remove a node from the list, ‘onetry’ to try a connection to
            the node once
        """
        return self.__rpc.batch(["addnode", node, command])

    def clear_banned(self) -> None:
        """
        Clear all banned IPs.
        """
        return self.__rpc.batch(["clearbanned"])

    def disconnect_node(self, address=None, nodeid=None) -> None:
        """
        Immediately disconnects from the specified peer node.
        Strictly one out of ‘address’ and ‘nodeid’ can be provided to identify the node.
        To disconnect by nodeid, either set ‘address’ to the empty string, or call using the named ‘nodeid’ argument
        only.

        Parameters
        -------
        address : str
            The IP address/port of the node.

        nodeid : int
            The node ID (see getpeerinfo for node IDs)
        """
        return self.__rpc.batch(["disconnectnode", address, nodeid])

    def get_added_node_info(self, node=None) -> dict:
        """
        Returns information about the given added node, or all added nodes (note that onetry addnodes are not listed
        here)

        Parameters
        -------
        node : str
            If provided, return information about this specific node, otherwise all nodes are returned.

        Returns
        -------
        dict
             Information about the given added node.
        """
        return self.__rpc.batch(["getaddednodeinfo", node])

    def get_connection_count(self) -> int:
        """
        Returns the number of connections to other nodes.

        Returns
        -------
        int
            The connection count
        """
        return self.__rpc.batch(["getconnectioncount"])

    def get_net_totals(self) -> dict:
        """
        Returns information about network traffic, including bytes in, bytes out, and current time.

        Returns
        -------
        dict
            Information about network traffic.
        """
        return self.__rpc.batch(["getnettotals"])

    def get_network_info(self) -> dict:
        """
        Returns an object containing various state info regarding P2P networking.

        Returns
        -------
        dict
            Object containing various state info regarding P2P networking.
        """
        return self.__rpc.batch(["getnetworkinfo"])

    def get_node_addresses(self, count=None) -> list:
        """
        Return known addresses which can potentially be used to find new nodes in the network.

        Parameters
        -------
        count : int
            How many addresses to return. Limited to the smaller of 2500 or 23% of all known addresses.

        Returns
        -------
        list
            Addresses which can potentially be used to find new nodes in the network.
        """
        return self.__rpc.batch(["getnodeaddresses", count])

    def get_peer_info(self) -> list:
        """
        Returns data about each connected network node as a json array of objects.

        Returns
        -------
        list
            Data about each connected network node as a json array of objects.
        """
        return self.__rpc.batch(["getpeerinfo"])

    def list_banned(self) -> list:
        """
        List all banned IPs/Subnets.

        Returns
        -------
        list
            List of all banned IPs/Subnets.
        """
        return self.__rpc.batch(["listbanned"])

    def ping(self) -> None:
        """
        Requests that a ping be sent to all other nodes, to measure ping time.
        Results provided in getpeerinfo, pingtime and pingwait fields are decimal seconds.
        Ping command is handled in queue with all other commands, so it measures processing backlog, not just network
        ping.
        """
        return self.__rpc.batch(["ping"])

    def set_ban(self, subnet: str, command: str, bantime=None, absolute=None) -> None:
        """
        Attempts to add or remove an IP/Subnet from the banned list.

        Parameters
        -------
        subnet : str
            The IP/Subnet (see getpeerinfo for nodes IP) with an optional netmask (default is /32 = single IP)

        command : str
            ‘add’ to add an IP/Subnet to the list,
            ‘remove’ to remove an IP/Subnet from the list

        bantime : int
            time in seconds how long (or until when if [absolute] is set) the IP is banned (0 or empty means
            using the default time of 24h which can also be overwritten by the -bantime startup argument)

        absolute : bool
            If set, the bantime must be an absolute timestamp in seconds since epoch (Jan 1 1970 GMT)
        """
        return self.__rpc.batch(["setban", subnet, command, bantime, absolute])

    def set_network_active(self, state: bool) -> None:
        """
        Disable/enable all p2p network activity.

        Parameters
        -------
        state : bool
            true to enable networking, false to disable
        """
        return self.__rpc.batch(["setnetworkactive", state])