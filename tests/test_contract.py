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
not_seller_not_buyer = 2
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


def test_totalEtherTraded(deploy):
    '''test of the totalEtherTraded is initialized to 0'''
    assert deploy.totalEtherTraded() == 0


'''TESTING TOTALETHERBURNT'''


def test_totalEtherBurnt(deploy):
    '''test of the totalEtherTraded is initialized to 0'''
    assert deploy.totalEtherBurnt() == 0


'''TESTING BUYERPRODUCTS'''


def test_buyerProducts(deploy):
    '''check if the mapping buyerProducts emits correct productId for the first element'''
    assert deploy.buyerProducts(accounts[buyer], 0) == 1

def test_buyerProducts_2(deploy):
    '''check if the mapping buyerProducts emits correct productId for the second element'''
    deploy.buyProduct(accounts[seller], {'from': accounts[buyer], 'value': products_price})
    assert deploy.buyerProducts(accounts[buyer], 1) == 2

def test_buyerProducts_3(deploy):
    '''check if the mapping buyerProducts emits correct productId for the third element'''
    deploy.buyProduct(accounts[seller], {'from': accounts[buyer], 'value': products_price})
    deploy.buyProduct(accounts[seller], {'from': accounts[buyer], 'value': products_price})
    assert deploy.buyerProducts(accounts[buyer], 2) == 3


'''TESTING SELLERPRODUCTS'''


def test_sellerProducts(deploy):
    '''check if the mapping buyerProducts emits correct productId for the first element'''
    assert deploy.sellerProducts(accounts[seller], 0) == 1

def test_sellerProducts_2(deploy):
    '''check if the mapping buyerProducts emits correct productId for the second element'''
    deploy.buyProduct(accounts[seller], {'from': accounts[buyer], 'value': products_price})
    assert deploy.sellerProducts(accounts[seller], 1) == 2

def test_sellerProducts_3(deploy):
    '''check if the mapping buyerProducts emits correct productId for the third element'''
    deploy.buyProduct(accounts[seller], {'from': accounts[buyer], 'value': products_price})
    deploy.buyProduct(accounts[seller], {'from': accounts[buyer], 'value': products_price})
    assert deploy.sellerProducts(accounts[seller], 2) == 3


'''TESTING REJECTSELLING'''  

'''DOESN'T WORK'''
def test_rejectSelling_first_reuqirement_fail(deploy):
    '''test if the first requirement fails'''
    deploy.payOut(1, {'from': accounts[seller]})
    try:
        chain = Chain()
        chain.sleep(604800 + now + 1000000000)
        deploy.rejectSelling(1, {'from': accounts[seller]})
        pytest.fail("The try-except concept has failed in test_rejectSelling_first_reuqirement_fail")
    except Exception as e:
        assert e.message[50:] == "The deal has already ended"

def test_rejectSelling_second_reuqirement_fail(deploy):
    '''test if the second requirement fails'''
    try:
        chain = Chain()
        chain.sleep(604800 + now + 1000000000)
        deploy.rejectSelling(1, {'from': accounts[buyer]})
        pytest.fail("The try-except concept has failed in test_rejectSelling_second_reuqirement_fail")
    except Exception as e:
        assert e.message[50:] == "You aren't the seller of this product"

def test_rejectSelling_withdraw_buyer(deploy):
    '''test if the price of the product is returned to the buyer'''
    amount = deploy.getWithdrawalBuyer({'from': accounts[buyer]})
    deploy.rejectSelling(1, {'from': accounts[seller]})
    assert deploy.getWithdrawalBuyer({'from': accounts[buyer]}) == amount + deploy.exactProduct(agreements_number)[1] 
'''DOESN'T WORK'''
def test_rejectSelling_dealEnded(deploy):
    '''test if the deal has ended after rejectSelling'''
    deploy.rejectSelling(1, {'from': accounts[seller]})
    assert deploy.exactProduct(1)[5] == True    


'''TESTING BUYERTICKSYES'''


def test_buyerTicksYes_first_requirement_fails(deploy):
    '''test if the first requirement works as planned'''
    try:
        chain = Chain()
        chain.sleep(604800 + now + 1000000000)
        deploy.buyerTicksYes(1, {'from': accounts[buyer]})
        pytest.fail("The try-except concept has failed in test_buyerTicksYes_first_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "The changing status deadline has expired"

def test_buyerTicksYes_second_requirement_fails(deploy):
    '''test if the second requirement works as planned'''
    try:
        deploy.buyerTicksYes(1, {'from': accounts[seller]})
        pytest.fail("The try-except concept has failed in test_buyerTicksYes_second_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "You are not the product's buyer"

def test_buyerTicksYes_third_requirement_fails(deploy):
    '''test if the third requirement works as planned'''
    deploy.buyerTicksYes(1, {'from': accounts[buyer]})
    try:
        deploy.buyerTicksYes(1, {'from': accounts[buyer]})
        pytest.fail("The try-except concept has failed in test_buyerTicksYes_third_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "The status is already set to Yes"

def test_buyerTicksyes_increment_ticks(deploy):
    '''test if the ticks do increment'''
    deploy.buyerTicksYes(1, {'from': accounts[buyer]})
    assert deploy.exactProduct(agreements_number)[6] == status_yes


'''TESTING BUYERTICKSNO'''


def test_buyerTicksNo_first_requirement_fails(deploy):
    '''test if the first requirement works as planned'''
    try:
        chain = Chain()
        chain.sleep(604800 + now + 1000000000)
        deploy.buyerTicksNo(1, {'from': accounts[buyer]})
        pytest.fail("The try-except concept has failed in test_buyerTicksNo_first_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "The changing status deadline has expired"

def test_buyerTicksNo_second_requirement_fails(deploy):
    '''test if the second requirement works as planned'''
    try:
        deploy.buyerTicksNo(1, {'from': accounts[seller]})
        pytest.fail("The try-except concept has failed in test_buyerTicksNo_second_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "You are not the product's buyer"

def test_buyerTicksNo_third_requirement_fails(deploy):
    '''test if the third requirement works as planned'''
    try:
        deploy.buyerTicksNo(1, {'from': accounts[buyer]})
        pytest.fail("The try-except concept has failed in test_buyerTicksNo_third_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "The status is already set to No"

def test_buyerTicksyes_increment_ticks(deploy):
    '''test if the ticks do increment'''
    deploy.buyerTicksYes(1, {'from': accounts[buyer]})
    deploy.buyerTicksNo(1, {'from': accounts[buyer]})
    assert deploy.exactProduct(agreements_number)[6] == status_no


'''TESTING SELLERTICKSYES'''


def test_sellerTicksYes_first_requirement_fails(deploy):
    '''test if the first requirement works as planned'''
    try:
        chain = Chain()
        chain.sleep(604800 + now + 1000000000)
        deploy.sellerTicksYes(1, {'from': accounts[seller]})
        pytest.fail("The try-except concept has failed in test_sellerTicksYes_first_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "The changing status deadline has expired"

def test_sellerTicksYes_second_requirement_fails(deploy):
    '''test if the second requirement works as planned'''
    try:
        deploy.sellerTicksYes(1, {'from': accounts[buyer]})
        pytest.fail("The try-except concept has failed in test_sellerTicksYes_second_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "You are not the product's seller"

def test_sellerTicksYes_third_requirement_fails(deploy):
    '''test if the third requirement works as planned'''
    deploy.sellerTicksYes(1, {'from': accounts[seller]})
    try:
        deploy.sellerTicksYes(1, {'from': accounts[seller]})
        pytest.fail("The try-except concept has failed in test_sellerTicksYes_third_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "The status is already set to Yes"

def test_sellerTicksyes_increment_ticks(deploy):
    '''test if the ticks do increment'''
    deploy.sellerTicksYes(1, {'from': accounts[seller]})
    assert deploy.exactProduct(1)[7] == status_yes


'''TESTING SELLERTICKSNO'''


def test_sellerTicksNo_first_requirement_fails(deploy):
    '''test if the first requirement works as planned'''
    try:
        chain = Chain()
        chain.sleep(604800 + now + 1000000000)
        deploy.sellerTicksNo(1, {'from': accounts[seller]})
        pytest.fail("The try-except concept has failed in test_sellerTicksNo_first_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "The changing status deadline has expired"

def test_sellerTicksNo_second_requirement_fails(deploy):
    '''test if the second requirement works as planned'''
    try:
        deploy.sellerTicksNo(1, {'from': accounts[buyer]})
        pytest.fail("The try-except concept has failed in test_sellerTicksNo_second_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "You are not the product's seller"

def test_sellerTicksNo_third_requirement_fails(deploy):
    '''test if the third requirement works as planned'''
    try:
        deploy.sellerTicksNo(1, {'from': accounts[seller]})
        pytest.fail("The try-except concept has failed in test_sellerTicksNo_third_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "The status is already set to No"

def test_sellerTicksNo_increment_ticks(deploy):
    '''test if the ticks do increment'''
    deploy.sellerTicksYes(1, {'from': accounts[seller]})
    deploy.sellerTicksNo(1, {'from': accounts[seller]})
    assert deploy.exactProduct(agreements_number)[7] == status_no


'''TESTING FORCEDENDDEAL'''


def test_forcedEndDeal_first_requirement_fail(deploy):
    '''test if the first requirement fails'''
    try:
        deploy.forcedEndDeal(1, {'from': accounts[buyer]})
        pytest.fail("The try-except concept has failed in test_forcedEndDeal_first_requirement_fail")
    except Exception as e:
        assert e.message[50:] == "You aren't the seller of this product"

def test_forcedEndDeal_second_requirement_fails(deploy):
    '''test if the second requirement works as planned'''
    try:
        chain = Chain()
        chain.sleep(604800 + now + 1000000000)
        deploy.forcedEndDeal(1, {'from': accounts[seller]})
        pytest.fail("The try-except concept has failed in test_forcedEndDeal_second_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "The deadline has expired"

'''DOESN'T WORK'''
def test_forcedEndDeal_third_requirement_fails(deploy):
    '''test if the third requirement works as planned'''
    deploy.payOut(1, {'from': accounts[seller]})
    try:
        deploy.forcedEndDeal(1, {'from': accounts[seller]})
        pytest.fail("The try-except concept has failed in test_forcedEndDeal_third_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "The deadline has already ended"

def test_forcedEndDeal_buyer_seller_no(deploy):
    '''test if the transaction is reverted, because the buyer and the seller didn't ticked'''
    try:
        deploy.forcedEndDeal(1, {'from': accounts[seller]})
        pytest.fail("The try-except concept has failed in test_forcedEndDeal_buyer_seller_no")
    except Exception as e:
        assert e.message[50:] == "Both seller and the buyer have to approve"

def test_forcedEndDeal_seller_no(deploy):
    '''test if the transaction is reverted, because the seller didn't ticked'''
    deploy.buyerTicksYes(1, {'from': accounts[buyer]})
    try:
        deploy.forcedEndDeal(1, {'from': accounts[seller]})
        pytest.fail("The try-except concept has failed in test_forcedEndDeal_buyer_seller_no")
    except Exception as e:
        assert e.message[50:] == "Both seller and the buyer have to approve"

def test_forcedEndDeal_buyer_seller_no(deploy):
    '''test if the transaction is reverted, because the buyer didn't ticked'''
    deploy.sellerTicksYes(1, {'from': accounts[seller]})
    try:
        deploy.forcedEndDeal(1, {'from': accounts[seller]})
        pytest.fail("The try-except concept has failed in test_forcedEndDeal_buyer_seller_no")
    except Exception as e:
        assert e.message[50:] == "Both seller and the buyer have to approve"

def test_forcedEndDeal_withdraw_seller(deploy):
    '''test if the seller gets back the price'''
    deploy.buyerTicksYes(1, {'from': accounts[buyer]})
    deploy.sellerTicksYes(1, {'from': accounts[seller]})
    amount = deploy.getWithdrawalSeller({'from': accounts[seller]})
    deploy.forcedEndDeal(1, {'from': accounts[seller]})
    assert deploy.getWithdrawalSeller({'from': accounts[seller]}) == amount + deploy.exactProduct(agreements_number)[1]

def test_forcedEndDeal_totalEtherTraded(deploy):
    '''test if the totalEtherTraded increases'''
    deploy.buyerTicksYes(1, {'from': accounts[buyer]})
    deploy.sellerTicksYes(1, {'from': accounts[seller]})
    amount = deploy.totalEtherTraded()
    deploy.forcedEndDeal(1, {'from': accounts[seller]})
    assert deploy.totalEtherTraded() == amount + deploy.totalEtherTraded()

def test_forcedEndDeal_totalEtherTraded(deploy):
    '''test if the totalEtherTraded increases'''
    deploy.buyerTicksYes(1, {'from': accounts[buyer]})
    deploy.sellerTicksYes(1, {'from': accounts[seller]})
    amount = deploy.totalEtherTraded()
    deploy.forcedEndDeal(1, {'from': accounts[seller]})
    assert deploy.totalEtherTraded() == amount + deploy.totalEtherTraded()
'''DOESN'T WORK'''
def test_forcedEndDeal_dealEnded(deploy):
    '''test if the dealEnded is set to true'''
    deploy.buyerTicksYes(1, {'from': accounts[buyer]})
    deploy.sellerTicksYes(1, {'from': accounts[seller]})
    deploy.forcedEndDeal(1, {'from': accounts[seller]})
    assert deploy.exactProduct(agreements_number)[5] == True


'''TESTING PAYOUT'''


def test_payOut_first_requirement_fails(deploy):
    '''test if the first requirement works'''
    try:
        deploy.payOut(1, {'from': accounts[not_seller_not_buyer]})
        pytest.fail("The try-except concept has failed in test_payOut_first_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "You aren't the seller or the buyer of this product"
'''DOESN'T WORK'''
@pytest.mark.parametrize("buyer_or_seller", [buyer, seller])
def test_payOut_second_requirement_fails(deploy, buyer_or_seller):
    '''test if the second requirement works'''
    deploy.payOut(1, {'from': accounts[buyer_or_seller]})
    try:
        deploy.payOut(1, {'from': accounts[buyer_or_seller]})
        pytest.fail("The try-except concept has failed in test_payOut_second_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "This deal was already paid out"

@pytest.mark.parametrize("buyer_or_seller", [buyer, seller])
def test_forcedEndDeal_third_requirement_fails(deploy, buyer_or_seller):
    '''test if the third requirement works'''
    try:
        chain = Chain()
        chain.sleep(604800 + now + 1000000000)
        deploy.payOut(1, {'from': accounts[buyer_or_seller]})
        pytest.fail("The try-except concept has failed in test_payOut_third_requirement_fails")
    except Exception as e:
        assert e.message[50:] == "The deadline has expired"

@pytest.mark.parametrize("buyer_or_seller", [buyer, seller])
def test_payout_both_status_no_withdraw_buyer(deploy, buyer_or_seller):
    '''test if the buyer gets back the product's cost'''
    amount = deploy.getWithdrawalBuyer({'from': accounts[buyer]})
    deploy.payOut(1, {'from': accounts[buyer_or_seller]})
    assert deploy.getWithdrawalBuyer({'from': accounts[buyer]}) == amount + deploy.exactProduct(agreements_number)[1]

'''DOESN'T WORK'''
@pytest.mark.parametrize("buyer_or_seller", [buyer, seller])
def test_payout_both_status_no_change_status(deploy, buyer_or_seller):
    '''test if the product's status is set to True'''
    deploy.payOut(1, {'from': accounts[buyer_or_seller]})
    assert deploy.exactProduct(agreements_number)[5] == True

@pytest.mark.parametrize("buyer_or_seller", [buyer, seller])
def test_payout_seller_status_yes_totalEtherBurnt(deploy, buyer_or_seller):
    '''test if the totalEtherBurnt increases'''
    amount = deploy.totalEtherBurnt()
    deploy.sellerTicksYes(1, {'from': accounts[seller]})
    deploy.payOut(1, {'from': accounts[buyer_or_seller]})
    assert deploy.totalEtherBurnt() == amount + deploy.exactProduct(agreements_number)[1]

'''DOESN'T WORK'''
@pytest.mark.parametrize("buyer_or_seller", [buyer, seller])
def test_payout_seller_status_yes_change_status(deploy, buyer_or_seller):
    '''test if the product's status is set to True'''
    deploy.sellerTicksYes(1, {'from': accounts[seller]})
    deploy.payOut(1, {'from': accounts[buyer_or_seller]})
    assert deploy.exactProduct(agreements_number)[5] == True

@pytest.mark.parametrize("buyer_or_seller", [buyer, seller])
def test_payout_buyer_status_yes_totalEtherBurnt(deploy, buyer_or_seller):
    '''test if the totalEtherBurnt increases'''
    amount = deploy.totalEtherBurnt()
    deploy.buyerTicksYes(1, {'from': accounts[buyer]})
    deploy.payOut(1, {'from': accounts[buyer_or_seller]})
    assert deploy.totalEtherBurnt() == amount + deploy.exactProduct(agreements_number)[1]

'''DOESN'T WORK'''
@pytest.mark.parametrize("buyer_or_seller", [buyer, seller])
def test_payout_buyer_status_yes_change_status(deploy, buyer_or_seller):
    '''test if the product's status is set to True'''
    deploy.buyerTicksYes(1, {'from': accounts[buyer]})
    deploy.payOut(1, {'from': accounts[buyer_or_seller]})
    assert deploy.exactProduct(agreements_number)[5] == True

@pytest.mark.parametrize("buyer_or_seller", [buyer, seller])
def test_payout_both_status_yes_withdraw_seller(deploy, buyer_or_seller):
    '''test if the seller gets the product's cost'''
    deploy.buyerTicksYes(1, {'from': accounts[buyer]})
    deploy.sellerTicksYes(1, {'from': accounts[seller]})
    amount = deploy.getWithdrawalSeller({'from': accounts[seller]})
    deploy.payOut(1, {'from': accounts[buyer_or_seller]})
    assert deploy.getWithdrawalSeller({'from': accounts[seller]}) == amount + deploy.exactProduct(agreements_number)[1]

@pytest.mark.parametrize("buyer_or_seller", [buyer, seller])
def test_payout_both_status_yes_totalEtherTraded(deploy, buyer_or_seller):
    '''test if the totalEtherTraded increases'''
    amount = deploy.totalEtherTraded()
    deploy.buyerTicksYes(1, {'from': accounts[buyer]})
    deploy.sellerTicksYes(1, {'from': accounts[seller]})
    deploy.payOut(1, {'from': accounts[buyer_or_seller]})
    assert deploy.totalEtherTraded() == amount + deploy.exactProduct(agreements_number)[1]
'''DOESN'T WORK'''
@pytest.mark.parametrize("buyer_or_seller", [buyer, seller])
def test_payout_both_status_yes_change_status(deploy, buyer_or_seller):
    '''test if the product's status is set to True'''
    deploy.buyerTicksYes(1, {'from': accounts[buyer]})
    deploy.sellerTicksYes(1, {'from': accounts[seller]})
    deploy.payOut(1, {'from': accounts[buyer_or_seller]})
    assert deploy.exactProduct(agreements_number)[5] == True


'''TESTING GETWITHDRAWALBUYER'''


@pytest.mark.parametrize("users", [1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_getWithdrawalBuyer_initialization(deploy, users):
    '''test if the getWithdrawalBuyer returns 0 when initialized'''
    assert deploy.getWithdrawalBuyer({'from': accounts[users]}) == 0


'''TESTING GETWITHDRAWALSELLER'''


@pytest.mark.parametrize("users", [1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_getWithdrawalSeller_initialization(deploy, users):
    '''test if the getWithdrawalSeller returns 0 when initialized'''
    assert deploy.getWithdrawalSeller({'from': accounts[users]}) == 0

'''TESTING BUYERPRODUCTS'''

'''TESTING SELLERPRODUCTS'''

'''TESTING WITHDRAWASTHEBUYER'''

@pytest.mark.aaa
@pytest.mark.parametrize("users", [1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_withdrawAsTheBuyer_first_reqirements(deploy, users):
    '''test if the first requirement works'''
    try:
        deploy.withdrawAsTheBuyer({'from': accounts[users]})
        pytest.fail("The try-except concept has failed in test_withdrawAsTheBuyer_first_reqirements")
    except Exception as e:
        assert e.message[50:] == "There aren't any funds to withdraw"

'''TESTING WITHDRAWASTHESELLER'''