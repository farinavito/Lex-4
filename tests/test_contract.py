from itertools import chain
import pytest
import brownie
from brownie import *
from brownie import accounts
from brownie.network import rpc
from brownie.network.state import Chain

#new agreement
buyer = 1
seller = 9
amount_sent = 10**10
products_price = 100
agreement_duration = 2629743 + 1749185494

without_buyer = [buyer + 1, buyer + 2, buyer + 3]
without_seller = [seller - 1, seller - 2, seller - 3]


less_than_amount_sent = [amount_sent - 5, amount_sent - 6, amount_sent - 7]
more_than_amount_sent = [amount_sent + 10**2, amount_sent + 10**3, amount_sent + 10**4]


less_than_agreement_duration = [agreement_duration - 10**2, agreement_duration - 10**3, agreement_duration - 10**4]
more_than_agreement_duration = [agreement_duration + 10**5, agreement_duration + 10**6, agreement_duration + 10**7]

seconds_in_day = 60 * 60 * 24
negative_values = [-1, -10, -100]


@pytest.fixture(scope="module", autouse=True)
def deploy(productTrade):
    return productTrade.deploy( {'from': accounts[0]})

@pytest.fixture(scope="module", autouse=True)
def new_agreement(deploy):
    return deploy.buyProduct(accounts[seller], {'from': accounts[buyer], 'value': products_price})

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass