#!/usr/bin/python3
import os
from brownie import Degenebabies, accounts, network, config

def main():
    dev = accounts.load("dev")
    admin = "0x52B1C5809ae80beE83103AE49034fcED2aeCBB3d"
    print(network.show_active())
    publish_source = False # Not supported on Testnet
    name = "The Degenebabies"
    symbol = "DEGENEBABY"
    base_uri = ""
    base_extension = ".json"
    not_revealed_uri = "ipfs://bafkreidixdn4jj2vdbtzkq6xnl3v2egbc5nqznbdmhgy3cmlqandj25ua4"
    max_supply = 1117

    # TESTING ONLY ##################################################
    rabbits_address = "0xbC9fd959e4551a9e4665C9D117c56F8636a555C5"  #
    lolas_address = "0x258E9E7cae048B19863BACd73fE6Ae083596B5ce"    #
    # TESTING ONLY ##################################################

    # PROD VALUES
    # rabbits_address = "0x8E7c434B248d49D873D0F8448E0FcEc895b1b92D"
    # lolas_address = "0xa17CCe73e11400623c900EB18E294Dc0318b86cf"
    Degenebabies.deploy(
                name,
                symbol,
                base_uri,
                base_extension,
                not_revealed_uri,
                max_supply,
                rabbits_address,
                lolas_address,
                admin,
                {"from": dev},
                publish_source=publish_source
    )
