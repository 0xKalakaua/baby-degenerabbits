import pytest
import brownie
from brownie import network, accounts, Degenebabies, MockERC721

@pytest.fixture
def rabbits():
    dev = accounts[0]
    max_supply = 10
    rabbits = MockERC721.deploy("Rabbits Test", "RABBITS", max_supply, dev, {'from': dev})
    for i in range(max_supply):
        if i == max_supply - 1:
            rabbits.mint(accounts[2], f"Rabbit #{i+1}", {'from': dev})
        elif i >= max_supply - 3:
            rabbits.mint(accounts[1], f"Rabbit #{i+1}", {'from': dev})
        else:
            rabbits.mint(dev, f"Rabbit #{i+1}", {'from': dev})

    return rabbits

@pytest.fixture
def lolas():
    dev = accounts[0]
    max_supply = 10
    lolas = MockERC721.deploy("Lolas Test", "LOLAS", max_supply, dev, {'from': dev})
    for i in range(max_supply):
        if i == max_supply - 1:
            lolas.mint(accounts[2], f"Rabbit #{i+1}", {'from': dev})
        elif i >= max_supply - 3:
            lolas.mint(accounts[1], f"Rabbit #{i+1}", {'from': dev})
        else:
            lolas.mint(dev, f"Rabbit #{i+1}", {'from': dev})

    return lolas

@pytest.fixture
def contracts(rabbits, lolas):
    dev = accounts[0]
    name = "Test Rabbits"
    symbol = "BABYRABBIT"
    base_uri = "base_uri/"
    base_extension = ".json"
    not_revealed_uri = "not_revealed_uri"
    max_supply = 10
    admin = accounts[9]

    babies = Degenebabies.deploy(
                            name,
                            symbol,
                            base_uri,
                            base_extension,
                            not_revealed_uri,
                            max_supply,
                            rabbits.address,
                            lolas.address,
                            admin,
                            {'from': dev}
              )
    return rabbits, lolas, babies


def test_initial_state(contracts):
    rabbits, lolas, babies = contracts

    assert rabbits.balanceOf(accounts[0]) == 7
    assert rabbits.balanceOf(accounts[1]) == 2
    assert rabbits.balanceOf(accounts[2]) == 1

    assert lolas.balanceOf(accounts[0]) == 7
    assert lolas.balanceOf(accounts[1]) == 2
    assert lolas.balanceOf(accounts[2]) == 1

    assert babies.name() == "Test Rabbits"
    assert babies.symbol() == "BABYRABBIT"
    assert babies.MAX_SUPPLY() == 10


def test_set_uri(contracts):
    dev = accounts[0]
    alice = accounts[1]
    rabbits, lolas, babies = contracts

    # not admin
    with brownie.reverts("caller is not admin"):
        babies.mintSwitch({'from': alice})
        babies.revealBabies({'from': alice})
        babies.setBaseExtension(".gif", {'from': alice})
        babies.setBaseURI("new_uri/", {'from': alice})
        babies.setTokenURI(1, "custom_token_uri", {'from': alice})

    # test tokenURI
    with brownie.reverts("URI query for nonexistent token"):
        babies.tokenURI(1)

    babies.mintSwitch({'from': dev})
    babies.makeBaby(1, 2, {'from': dev})
    babies.makeBabyToWallet(dev, 2, 1, {'from': dev})

    assert babies.tokenURI(1) == "not_revealed_uri"
    assert babies.tokenURI(2) == "not_revealed_uri"

    babies.revealBabies({'from': dev})
    assert babies.tokenURI(1) == "base_uri/1.json"
    assert babies.tokenURI(2) == "base_uri/2.json"

    with brownie.reverts("ERC721URIStorage: URI query for nonexistent token"):
        babies.tokenURI(3)

    # test setBaseExtension
    babies.setBaseExtension(".gif", {'from': dev})
    assert babies.tokenURI(1) == "base_uri/1.gif"
    assert babies.tokenURI(2) == "base_uri/2.gif"

    # test setBaseURI
    babies.setBaseURI("new_uri/", {'from': dev})
    assert babies.tokenURI(1) == "new_uri/1.gif"
    assert babies.tokenURI(2) == "new_uri/2.gif"

    # test setTokenURI
    babies.setTokenURI(1, "custom_token_uri", {'from': accounts[9]})
    assert babies.tokenURI(1) == "new_uri/custom_token_uri.gif"
    babies.setTokenURI(2, "custom_token_uri_2")
    assert babies.tokenURI(2) == "new_uri/custom_token_uri_2.gif"


def test_make_baby(contracts):
    dev = accounts[0]
    alice = accounts[1]
    bob = accounts[2]
    admin = accounts[9]
    rabbits, lolas, babies = contracts

    # minting not open
    with brownie.reverts("minting is currently not open"):
        babies.makeBaby(1, 1, {'from': dev})
        babies.makeBabyToWallet(dev, 1, 1, {'from': dev})
    
    babies.mintSwitch({'from': dev})

    # not owner of rabbit
    with brownie.reverts("caller is not owner of that rabbit"):
        babies.makeBaby(3, 8, {'from': alice})
        babies.makeBabyToWallet(alice, 3, 8, {'from': dev})

    # not owner of lolasgirl
    with brownie.reverts("caller is not owner of that lolasGirl"):
        babies.makeBaby(8, 3, {'from': alice})
        babies.makeBabyToWallet(alice, 8, 3, {'from': dev})

    # not admin
    with brownie.reverts("caller is not admin"):
        babies.makeBabyToWallet(alice, 8, 8, {'from': bob})

    # normal mint
    babies.makeBabyToWallet(alice, 9, 9, {'from': dev})
    babies.makeBaby(1, 1, {'from': dev})
    assert babies.ownerOf(1) == alice
    assert babies.ownerOf(2) == dev

    # rabbit has baby already
    with brownie.reverts("rabbit has a baby already"):
        babies.makeBabyToWallet(alice, 9, 8, {'from': dev})
        babies.makeBaby(1, 2, {'from': dev})

    # lolasgirl has baby already
    with brownie.reverts("lolasGirl has a baby already"):
        babies.makeBabyToWallet(alice, 8, 9, {'from': dev})
        babies.makeBaby(2, 1, {'from': dev})

    for i in range(1, 10):
        if not babies.rabbitHasBaby(i):
            if i == 8:
                babies.makeBaby(i, i, {'from': alice})
            else:
                babies.makeBaby(i, i, {'from': dev})
    babies.makeBabyToWallet(bob, 10, 10, {'from': admin})

    assert babies.balanceOf(dev) == 7
    assert babies.balanceOf(alice) == 2
    assert babies.balanceOf(bob) == 1

    # all tokens have been minted
    with brownie.reverts("all tokens have been minted"):
        babies.makeBabyToWallet(alice, 9, 8, {'from': dev})
        babies.makeBaby(1, 2, {'from': dev})
