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
agreements_number = 1

status_no = 1
status_yes = 2

without_buyer = [buyer + 1, buyer + 2, buyer + 3]
without_seller = [seller - 1, seller - 2, seller - 3]


less_than_amount_sent = [amount_sent - 5, amount_sent - 6, amount_sent - 7]
more_than_amount_sent = [amount_sent + 10**2, amount_sent + 10**3, amount_sent + 10**4]


less_than_agreement_duration = [agreement_duration - 10**2, agreement_duration - 10**3, agreement_duration - 10**4]
more_than_agreement_duration = [agreement_duration + 10**5, agreement_duration + 10**6, agreement_duration + 10**7]

seconds_in_day = 60 * 60 * 24
negative_values = [-1, -10, -100]


@pytest.fixture(scope="module", autouse=True)
def deploy(TradeV1):
    return TradeV1.deploy( {'from': accounts[0]})

chain = Chain()
now = chain.time()

@pytest.fixture(scope="module", autouse=True)
def new_agreement(deploy):
    return deploy.buyProduct(accounts[seller], {'from': accounts[buyer], 'value': products_price})

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass



'''TESTING BUYPRODUCT'''


def test_buyProduct_id(deploy):
    '''test if the first id of the agreement is 1'''
    assert deploy.exactProduct(agreements_number)[0] == agreements_number

def test_buyProduct_price(deploy):
    '''test if the first price of the agreement is setted to the products_price'''
    assert deploy.exactProduct(agreements_number)[1] == products_price

def test_buyProduct_seller(deploy):
    '''test if the seller of the agreement is setted to the right address'''
    assert deploy.exactProduct(agreements_number)[2] == accounts[seller]

def test_buyProduct_buyer(deploy):
    '''test if the buyer of the agreement is setted to the right address'''
    assert deploy.exactProduct(agreements_number)[3] == accounts[buyer]

def test_buyProduct_deadline(deploy):
    '''test if the deadline of the agreement is setted to the right one'''
    assert deploy.exactProduct(agreements_number)[4] == now + 2419200 + 9

def test_buyProduct_dealEnded(deploy):
    '''test if the dealEnded of the agreement is setted to false'''
    assert deploy.exactProduct(agreements_number)[5] == False

def test_buyProduct_buyerApproves(deploy):
    '''test if the buyerApproves of the agreement is setted to false'''
    assert deploy.exactProduct(agreements_number)[6] == status_no

def test_buyProduct_sellerApproves(deploy):
    '''test if the sellerApproves of the agreement is setted to false'''
    assert deploy.exactProduct(agreements_number)[7] == status_no

def test_buyProduct_buyerProducts(deploy):
    '''test if the buyerproducts mapping is correctly changed'''
    assert deploy.buyerProducts(accounts[buyer], 0) == agreements_number

def test_buyProduct_sellerProducts(deploy):
    '''test if the sellerproducts mapping is correctly changed'''
    assert deploy.sellerProducts(accounts[seller], 0) == agreements_number

def test_buyProduct_fail_requirement(deploy):
    '''test if the buyProduct fails, because the msg.value isn't larger than 0'''
    try:
        deploy.buyProduct(accounts[seller], {'from': accounts[buyer], 'value': 0})
        pytest.fail("The try-except concept has failed in test_buyProduct_fail_requirement")
    except Exception as e:
        assert e.message[50:] == "You haven't sent ether"

def test_buyProduct_event_id(deploy):
    '''check if the id in the emitted event is correct when a new agreement is created'''
    function_initialize = deploy.buyProduct(accounts[seller], {'from': accounts[buyer], 'value': products_price})
    assert function_initialize.events[0][0]['productId'] == 2

def test_buyProduct_event_price(deploy):
    '''check if the price in the emitted event is correct when a new agreement is created'''
    function_initialize = deploy.buyProduct(accounts[seller], {'from': accounts[buyer], 'value': products_price})
    assert function_initialize.events[0][0]['productPrice'] == products_price

def test_buyProduct_event_seller(deploy):
    '''check if the seller in the emitted event is correct when a new agreement is created'''
    function_initialize = deploy.buyProduct(accounts[seller], {'from': accounts[buyer], 'value': products_price})
    assert function_initialize.events[0][0]['productSeller'] == accounts[seller]

def test_buyProduct_event_buyer(deploy):
    '''check if the buyer in the emitted event is correct when a new agreement is created'''
    function_initialize = deploy.buyProduct(accounts[seller], {'from': accounts[buyer], 'value': products_price})
    assert function_initialize.events[0][0]['productBuyer'] == accounts[buyer]

def test_buyProduct_event_deadline(deploy):
    '''check if the productDeadline in the emitted event is correct when a new agreement is created'''
    function_initialize = deploy.buyProduct(accounts[seller], {'from': accounts[buyer], 'value': products_price})
    assert function_initialize.events[0][0]['productDeadline'] == now + 2419200 + 9

def test_buyProduct_event_productDealEnded(deploy):
    '''check if the productDealEnded in the emitted event is correct when a new agreement is created'''
    function_initialize = deploy.buyProduct(accounts[seller], {'from': accounts[buyer], 'value': products_price})
    assert function_initialize.events[0][0]['productDealEnded'] == False 


'''TESTING NUMPRODUCT'''


def test_numProduct(deploy):
    '''test if the numProduct is 1, due to creating an agreement in the fixture'''
    assert deploy.numProduct() == 1

def test_numProduct_2(deploy):
    '''test if the numProduct is 2, due to creating an agreement in the fixture'''
    deploy.buyProduct(accounts[seller], {'from': accounts[buyer], 'value': products_price})
    assert deploy.numProduct() == 2


'''TESTING TOTALETHERTRADED'''

@pytest.mark.aaa
def test_totalEtherTraded(deploy):
    '''test of the totalEtherTraded is initialized to 0'''
    assert deploy.totalEtherTraded() == 0

'''TESTING BUYERPRODUCTS'''


'''TESTING SELLERPRODUCTS'''