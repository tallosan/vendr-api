from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, APIClient, APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status

from kuser.models import KUser
from kproperty.models import Condo, Location, TaxRecords, Historical, Features
from transaction.models import Transaction, Offer, Contract, AbstractContractFactory
from transaction.views import *

User = get_user_model()


'''   Tests for TransactionList() view. '''
class TestTransactionPost(APITestCase):

    def setUp(self):
        
        self.view = TransactionList.as_view()
        self.factory = APIRequestFactory()
        
        # Create the buyer, and seller.
        self.buyer = User.objects.create_user(email='buyer@kangaa.xyz',
                        password='buyer_pwd')
        self.seller = User.objects.create_user(email='seller@kangaa.xyz',
                        password='seller_pwd')
        
        # Create the property, and set up the necessary sub-models.
        self.kproperty = Condo.objects.create(owner=self.seller, n_bathrooms=1,
                            n_bedrooms=2, price=250000, sqr_ftg=3000, unit_num=11)
        Location.objects.create(kproperty=self.kproperty, address='74 Ulster St',
                    city="Toronto", country="Canada", province='Ontario',
                    postal_code='M1P0B2', latitude=43.773313, longitude=-79.258729)
        TaxRecords.objects.create(kproperty=self.kproperty)
        Historical.objects.create(kproperty=self.kproperty, last_sold_price=2000000,
                    last_sold_date='2011-08-14', year_built=2010)
        Features.objects.create(kproperty=self.kproperty, feature='Oven')

        # The transaction data.
        self.transaction_data = {
                "seller": self.seller.id,
                "kproperty": self.kproperty.id,
                "offers": [
                    {	
		        "offer": 350000,
		        "deposit": 20000,
		        "comment": "Please consider this offer!"
	            }
                ] 
        }

        self.path = '/v1/transactions/'

    ''' (Helper Function) Create a transaction. '''
    def create_transaction(self, kuser, expected_status):
        
        request = self.factory.post(self.path, self.transaction_data, format='json')
        force_authenticate(request, user=kuser)
        response = self.view(request)
        self.assertEqual(response.status_code, expected_status)
        
        return response
        
    ''' Create a transaction. '''
    def test_create_transaction(self):
        
        data = self.create_transaction(expected_status=status.HTTP_201_CREATED,
                kuser=self.buyer)

    ''' Attempt to create a transaction w/out authentication. '''
    def test_create_transaction_no_auth(self):

        self.create_transaction(expected_status=401, kuser=None)

    ''' Create a transaction on a property with the wrong seller given.
        N.B. -- We're returning an error code of 500 here. This test scenario
        is only possible if a malicious user is sending their own custom API call.
        Thus, I think it's acceptable to simply return a 500 and not reveal any
        of the internal details, as we'd like to hide them from bad actors. '''
    def test_create_transaction_with_wrong_seller(self):
        
        self.transaction_data['seller'] = self.buyer.pk
        with self.assertRaises(ValueError):
            request = self.factory.post(self.path, self.transaction_data,
                        format='json')
            force_authenticate(request, user=self.buyer)
            response = self.view(request)

    ''' Attempt to create a transaction without the necessary fields: kproperty,
        and seller. '''
    def test_create_transaction_without_necesssary_fields(self):

        # Leave out seller info.
        no_seller_data = self.transaction_data; no_seller_data.pop('seller')
        request = self.factory.post(self.path, no_seller_data, format='json')
        force_authenticate(request, user=self.buyer)
        response = self.view(request)
        self.assertEquals(response.status_code, 400)
        
        # Leave out property info.
        no_property_data = self.transaction_data; no_seller_data.pop('kproperty')
        request = self.factory.post(self.path, no_property_data, format='json')
        force_authenticate(request, user=self.buyer)
        response = self.view(request)
        self.assertEquals(response.status_code, 400)
       
    ''' Ensure that no more than one offer is used to create the transaction. '''
    def test_create_transaction_with_multiple_offers(self):

        self.transaction_data['offers'].append(self.transaction_data['offers'][0])
        self.create_transaction(expected_status=400, kuser=self.buyer)

    ''' Attempt to create a duplicate transaction. '''
    def test_duplicate_transaction(self):

        self.create_transaction(expected_status=201, kuser=self.buyer)
        self.create_transaction(expected_status=400, kuser=self.buyer)

    ''' Attempt to start a transaction on your own property. '''
    def test_create_transaction_on_owned_property(self):

        with self.assertRaises(ValueError):
            self.create_transaction(expected_status=400, kuser=self.seller)

    ''' Ensure that GET (LIST) requests are not permitted. '''
    def test_get_request(self):
        
        request = self.factory.get(self.path, kuser=self.buyer, format='json')
        force_authenticate(request, user=self.buyer)
        response = self.view(request)
        self.assertEquals(response.status_code, 405)

'''   Tests for TransactionDetail() view. '''
class TestTransactionDetail(APITestCase):

    def setUp(self):
        
        self.view = TransactionDetail.as_view()
        self.factory = APIRequestFactory()
        
        # Create the buyer, and seller.
        self.buyer = User.objects.create_user(email='buyer@kangaa.xyz',
                        password='buyer_pwd')
        self.seller = User.objects.create_user(email='seller@kangaa.xyz',
                        password='seller_pwd')
        self.wrong_user = User.objects.create_user(email='wronguser@kangaa.xyz',
                        password='wronguser')

        # Create the property, and set up the necessary sub-models.
        self.kproperty = Condo.objects.create(owner=self.seller, n_bathrooms=1,
                            n_bedrooms=2, price=250000, sqr_ftg=3000, unit_num=11)
        Location.objects.create(kproperty=self.kproperty, address='74 Ulster St',
                    city="Toronto", country="Canada", province='Ontario',
                    postal_code='M1P0B2', latitude=43.773313, longitude=-79.258729)
        TaxRecords.objects.create(kproperty=self.kproperty)
        Historical.objects.create(kproperty=self.kproperty, last_sold_price=2000000,
                    last_sold_date='2011-08-14', year_built=2010)
        Features.objects.create(kproperty=self.kproperty, feature='Oven')
 
        # The transaction data.
        offer_data = {	
                        "offer": 350000,
		        "deposit": 20000,
		        "comment": "Please consider this offer!"
	}
        
        self.transaction = Transaction.objects.create(buyer=self.buyer,
                seller=self.seller, kproperty=self.kproperty)
        self.offer = Offer.objects.create(owner=self.buyer,
                transaction=self.transaction, **offer_data)
        
        self.path = '/v1/transactions/{}/'.format(self.transaction.pk)
   
    ''' Get a transaction with the proper auth. Note, we need to ensure that
        this works for both the buyer & seller. '''
    def test_get_owned_transaction_with_auth(self):

        b_request = self.factory.get(self.path, format='json')
        force_authenticate(b_request, user=self.buyer)
        response = self.view(b_request, self.transaction.pk)
        self.assertEquals(response.status_code, 200)
        
        s_request = self.factory.get(self.path, format='json')
        force_authenticate(s_request, user=self.seller)
        response = self.view(s_request, self.transaction.pk)
        self.assertEquals(response.status_code, 200)
 
    ''' Get a transaction with the wrong auth. I.e. Get a transaction that
        we don't own / are not part of. '''
    def test_get_transaction_with_wrong_auth(self):

        request = self.factory.get(self.path, format='json')
        force_authenticate(request, user=self.wrong_user)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 403)
       
    ''' Get a transaction with no auth. '''
    def test_get_transaction_with_no_auth(self):

        request = self.factory.get(self.path, format='json')
        force_authenticate(request, user=None)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 401)
    
    ''' Update a transaction field with the correct auth. '''
    def test_update_transaction_with_auth(self):

        request = self.factory.put(self.path,
                data={'buyer_accepted_contract': True}, format='json')
        force_authenticate(request, user=self.buyer)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['buyer_accepted_contract'], True)
   
    ''' Ensure that buyers and sellers can update their own protected fields,
        and that, conversely, they cannot update one-another's. '''
    def test_update_transaction_protected_fields_with_auth(self):
    
        # Buyer updates their protected fields.
        buyer_data = {
                'buyer_accepted_contract': True,
                'buyer_accepted_offer': self.offer.pk
        }
        request = self.factory.put(self.path, data=buyer_data, format='json')
        force_authenticate(request, user=self.buyer)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 200)

        # Seller updates their protected fields.
        seller_data = {
                'seller_accepted_contract': True,
                'seller_accepted_offer': self.offer.pk
        }
        request = self.factory.put(self.path, data=seller_data, format='json')
        force_authenticate(request, user=self.seller)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 200)

        # Buyer attempts to update seller's protected fields.
        request = self.factory.put(self.path, data=seller_data, format='json')
        force_authenticate(request, user=self.buyer)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 403)

        # Seller attempts to update buyer's protected fields.
        request = self.factory.put(self.path, data=buyer_data, format='json')
        force_authenticate(request, user=self.seller)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 403)

        # Ensure that neither can update the 'contracts_equal' field.
        request = self.factory.put(self.path, data={'contracts_equal': True},
                    format='json')
        force_authenticate(request, user=self.buyer)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 403)
        request = self.factory.put(self.path, data={'contracts_equal': True},
                    format='json')
        force_authenticate(request, user=self.seller)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 403)

    ''' Ensure transactions in stage 0 can be updated. '''
    def test_update_advance_stage_0(self):

        self.transaction.buyer_accepted_offer = self.offer.pk
         
        # Attempt to advance stage when accepted offers are not equal.
        request = self.factory.put(self.path, data={'stage': 1}, format='json')
        force_authenticate(request, user=self.buyer)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(self.transaction.stage, 0)

        self.transaction.seller_accepted_offer = self.offer.pk
        self.transaction.save()
        
        # Advance stage when accepted offers are equal.
        request = self.factory.put(self.path, data={'stage': 1}, format='json')
        force_authenticate(request, user=self.buyer)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['stage'], 1)

    ''' Ensure transactions in stage 1 can be updated. '''
    def test_update_advance_stage_1(self):

        self.transaction.buyer_accepted_offer = self.offer.pk
        self.transaction.seller_accepted_offer = self.offer.pk
        self.transaction.stage = 1; self.transaction.save()
        
        # Attempt to advance stage when contracts are not equal.
        request = self.factory.put(self.path, data={'stage': 2}, format='json')
        force_authenticate(request, user=self.buyer)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(self.transaction.stage, 1)
        
        # Advance stage when contracts are equal.
        self.transaction.buyer_accepted_contract = True
        self.transaction.seller_accepted_contract = True
        self.transaction.contracts_equal = True
        self.transaction.save()

        request = self.factory.put(self.path, data={'stage': 2}, format='json')
        force_authenticate(request, user=self.buyer)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['stage'], 2)

    ''' Ensure transactions in stage 2 can be updated. '''
    def test_update_advance_stage_2(self):
        
        #TODO: Implement this once Closing has been completed.
        pass

    ''' Update a transaction with the wrong auth. I.e. Update a transaction that
        we don't own / are not part of. '''
    def test_update_transaction_with_wrong_auth(self):
        
        request = self.factory.put(self.path,
                data={'buyer_accepted_contract': True}, format='json')
        force_authenticate(request, user=self.wrong_user)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 403)
    
    ''' Update a transaction with no auth. '''
    def test_update_transaction_with_no_auth(self):
        
        request = self.factory.put(self.path,
                data={'buyer_accepted_contract': True}, format='json')
        force_authenticate(request, user=None)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 401)
    
    ''' Delete a transaction with the wrong auth. I.e. Delete a transaction that
        we don't own / are not part of. '''
    def test_delete_transaction_with_wrong_auth(self):

        request = self.factory.delete(self.path, format='json')
        force_authenticate(request, user=self.wrong_user)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 403)
    
    ''' Delete a transaction with no auth. '''
    def test_delete_transaction_with_no_auth(self):

        request = self.factory.delete(self.path, format='json')
        force_authenticate(request, user=None)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 401)


'''   Tests for OfferList() view. '''
class TestOfferList(APITestCase):

    def setUp(self):
        
        self.view = OfferList.as_view()
        self.factory = APIRequestFactory()
        
        # Create the buyer, and seller.
        self.buyer = User.objects.create_user(email='buyer@kangaa.xyz',
                        password='buyer_pwd')
        self.seller = User.objects.create_user(email='seller@kangaa.xyz',
                        password='seller_pwd')
        self.wrong_user = User.objects.create_user(email='wronguser@kangaa.xyz',
                        password='wronguser')

        # Create the property, and set up the necessary sub-models.
        self.kproperty = Condo.objects.create(owner=self.seller, n_bathrooms=1,
                            n_bedrooms=2, price=250000, sqr_ftg=3000, unit_num=11)
        Location.objects.create(kproperty=self.kproperty, address='74 Ulster St',
                    city="Toronto", country="Canada", province='Ontario',
                    postal_code='M1P0B2', latitude=43.773313, longitude=-79.258729)
        TaxRecords.objects.create(kproperty=self.kproperty)
        Historical.objects.create(kproperty=self.kproperty, last_sold_price=2000000,
                    last_sold_date='2011-08-14', year_built=2010)
        Features.objects.create(kproperty=self.kproperty, feature='Oven')
 
        # The transaction data.
        self.offer_data = {	
                        "offer": 350000,
		        "deposit": 20000,
		        "comment": "Please consider this offer!"
	}
        
        self.transaction = Transaction.objects.create(buyer=self.buyer,
                seller=self.seller, kproperty=self.kproperty)
        self.offer = Offer.objects.create(owner=self.buyer,
                transaction=self.transaction, **self.offer_data)
        
        self.path = '/v1/transactions/{}/offers/'.format(self.transaction.pk)

    ''' Create an offer on a transaction that the user is part of.
        N.B. -- We need to ensure both buyer and seller can create offers. '''
    def test_create_offer(self):

        # Buyer creates offer.
        request = self.factory.post(self.path, self.offer_data, format='json')
        force_authenticate(request, user=self.buyer)
        response = self.view(request, self.transaction.pk)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['comment'], self.offer_data['comment'])

        # Seller creates offer.
        request = self.factory.post(self.path, self.offer_data, format='json')
        force_authenticate(request, user=self.seller)
        response = self.view(request, self.transaction.pk)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['comment'], self.offer_data['comment'])
    
    ''' Attempt to create an offer with the wrong auth. '''
    def test_create_offer_with_wrong_auth(self):

        request = self.factory.post(self.path, self.offer_data, format='json')
        force_authenticate(request, user=self.wrong_user)
        response = self.view(request, self.transaction.pk)

        self.assertEquals(response.status_code, 403)

    ''' Attempt to create an offer with no auth. '''
    def test_create_offer_with_no_auth(self):

        request = self.factory.post(self.path, self.offer_data, format='json')
        force_authenticate(request, user=None)
        response = self.view(request, self.transaction.pk)

        self.assertEquals(response.status_code, 401)

    ''' Ensure that transaction participants can access the offers list. '''
    def test_get_offers(self):

        offer = Offer.objects.create(owner=self.buyer,
                transaction=self.transaction, **self.offer_data)

        # Buyer views offers.
        request = self.factory.get(self.path, format='json')
        force_authenticate(request, user=self.buyer)
        response = self.view(request, self.transaction.pk)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 2)

        # Seller views offers.
        request = self.factory.get(self.path, format='json')
        force_authenticate(request, user=self.seller)
        response = self.view(request, self.transaction.pk)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 2)
    
    ''' Attempt to get an offer with the wrong auth. '''
    def test_get_offers_with_wrong_auth(self):

        request = self.factory.get(self.path, format='json')
        force_authenticate(request, user=self.wrong_user)
        response = self.view(request, self.transaction.pk)

        self.assertEquals(response.status_code, 403)

    ''' Attempt to get an offer with no auth. '''
    def test_get_offers_with_no_auth(self):

        request = self.factory.get(self.path, format='json')
        force_authenticate(request, user=None)
        response = self.view(request, self.transaction.pk)

        self.assertEquals(response.status_code, 401)


'''   Tests for OfferDetail() view. '''
class TestOfferDetail(APITestCase):

    def setUp(self):
        
        self.view = OfferDetail.as_view()
        self.factory = APIRequestFactory()
        
        # Create the buyer, and seller.
        self.buyer = User.objects.create_user(email='buyer@kangaa.xyz',
                        password='buyer_pwd')
        self.seller = User.objects.create_user(email='seller@kangaa.xyz',
                        password='seller_pwd')
        self.wrong_user = User.objects.create_user(email='wronguser@kangaa.xyz',
                        password='wronguser')

        # Create the property, and set up the necessary sub-models.
        self.kproperty = Condo.objects.create(owner=self.seller, n_bathrooms=1,
                            n_bedrooms=2, price=250000, sqr_ftg=3000, unit_num=11)
        Location.objects.create(kproperty=self.kproperty, address='74 Ulster St',
                    city="Toronto", country="Canada", province='Ontario',
                    postal_code='M1P0B2', latitude=43.773313, longitude=-79.258729)
        TaxRecords.objects.create(kproperty=self.kproperty)
        Historical.objects.create(kproperty=self.kproperty, last_sold_price=2000000,
                    last_sold_date='2011-08-14', year_built=2010)
        Features.objects.create(kproperty=self.kproperty, feature='Oven')
 
        # The transaction data.
        self.offer_data = {	
                        "offer": 350000,
		        "deposit": 20000,
		        "comment": "Please consider this offer!"
	}
        
        self.transaction = Transaction.objects.create(buyer=self.buyer,
                seller=self.seller, kproperty=self.kproperty)
        self.offer = Offer.objects.create(owner=self.buyer,
                transaction=self.transaction, **self.offer_data)
        
        self.path = '/v1/transactions/{}/offers/{}/'.\
                    format(self.transaction.pk, self.offer.pk)


    ''' Ensure that transaction participants can access a transaction offer. '''
    def test_get_offer(self):

        # Buyer gets the offer.
        request = self.factory.get(self.path, format='json')
        force_authenticate(request, self.buyer)
        response = self.view(request, self.transaction.pk, self.offer.pk)

        self.assertEquals(response.status_code, 200)
 
        # Seller gets the offer.
        request = self.factory.get(self.path, format='json')
        force_authenticate(request, self.seller)
        response = self.view(request, self.transaction.pk, self.offer.pk)

        self.assertEquals(response.status_code, 200)
    
    ''' Attempt to get an offer with the wrong auth. '''
    def test_get_offer_with_wrong_auth(self):

        # Buyer gets the offer.
        request = self.factory.get(self.path, format='json')
        force_authenticate(request, self.wrong_user)
        response = self.view(request, self.transaction.pk, self.offer.pk)

        self.assertEquals(response.status_code, 403)
    
    ''' Attempt to get an offer with no auth. '''
    def test_get_offer_with_no_auth(self):

        # Buyer gets the offer.
        request = self.factory.get(self.path, format='json')
        force_authenticate(request, None)
        response = self.view(request, self.transaction.pk, self.offer.pk)

        self.assertEquals(response.status_code, 401)

    ''' Ensure that updates are not permitted. '''
    def test_update_offer(self):
        
        request = self.factory.put(self.path, data={'deposit':'0'}, format='json')
        force_authenticate(request, self.buyer)
        response = self.view(request, self.transaction.pk, self.offer.pk)

        self.assertEquals(response.status_code, 405)

    ''' Ensure that transaction participants can delete offers. Note, we'll
        also want to ensure that each participant cannot delete the
        other participant's offer. '''
    def test_delete_offer(self):
        
        self.seller_offer = Offer.objects.create(owner=self.seller,
                transaction=self.transaction, **self.offer_data)
        self.seller_path = '/v1/transactions/{}/offers/{}/'.\
                    format(self.transaction.pk, self.seller_offer.pk)
        
        # Buyer attempts to delete seller's offer.
        request = self.factory.delete(self.seller_path, format='json')
        force_authenticate(request, self.buyer)
        response = self.view(request, self.transaction.pk, self.seller_offer.pk)
        self.assertEquals(response.status_code, 403)
 
        # Seller attempts to delete buyer's offer.
        request = self.factory.delete(self.path, format='json')
        force_authenticate(request, self.seller)
        response = self.view(request, self.transaction.pk, self.offer.pk)
        self.assertEquals(response.status_code, 403)
         
        # Buyer deletes their offer.
        request = self.factory.delete(self.path, format='json')
        force_authenticate(request, self.buyer)
        response = self.view(request, self.transaction.pk, self.offer.pk)
        self.assertEquals(response.status_code, 204)
 
        # Seller deletes their offer.
        request = self.factory.delete(self.seller_path, format='json')
        force_authenticate(request, self.seller)
        response = self.view(request, self.transaction.pk, self.seller_offer.pk)
        self.assertEquals(response.status_code, 204)
       
    ''' Attempt to get an offer with the wrong auth. '''
    def test_delete_offer_with_wrong_auth(self):

        # Buyer gets the offer.
        request = self.factory.delete(self.path, format='json')
        force_authenticate(request, self.wrong_user)
        response = self.view(request, self.transaction.pk, self.offer.pk)

        self.assertEquals(response.status_code, 403)
    
    ''' Attempt to get an offer with no auth. '''
    def test_delete_offer_with_no_auth(self):

        # Buyer gets the offer.
        request = self.factory.delete(self.path, format='json')
        force_authenticate(request, None)
        response = self.view(request, self.transaction.pk, self.offer.pk)

        self.assertEquals(response.status_code, 401)


'''   Tests for ContractList() view. '''
class TestContractList(APITestCase):

    def setUp(self):
        
        self.view = ContractList.as_view()
        self.factory = APIRequestFactory()
        
        # Create the buyer, and seller.
        self.buyer = User.objects.create_user(email='buyer@kangaa.xyz',
                        password='buyer_pwd')
        self.seller = User.objects.create_user(email='seller@kangaa.xyz',
                        password='seller_pwd')
        self.wrong_user = User.objects.create_user(email='wronguser@kangaa.xyz',
                        password='wronguser')

        # Create the property, and set up the necessary sub-models.
        self.kproperty = Condo.objects.create(owner=self.seller, n_bathrooms=1,
                            n_bedrooms=2, price=250000, sqr_ftg=3000, unit_num=11)
        Location.objects.create(kproperty=self.kproperty, address='74 Ulster St',
                    city="Toronto", country="Canada", province='Ontario',
                    postal_code='M1P0B2', latitude=43.773313, longitude=-79.258729)
        TaxRecords.objects.create(kproperty=self.kproperty)
        Historical.objects.create(kproperty=self.kproperty, last_sold_price=2000000,
                    last_sold_date='2011-08-14', year_built=2010)
        Features.objects.create(kproperty=self.kproperty, feature='Oven')
 
        self.transaction = Transaction.objects.create(buyer=self.buyer,
                seller=self.seller, kproperty=self.kproperty)
        
        # The contract types.
        self.contract_types = ['coop', 'condo', 'house', 'townhouse', \
                'manufactured', 'vacant_land']
    
        self.path = '/v1/transactions/{}/contracts/'.format(self.transaction.pk)

    ''' Create each type of Contract. Note, we will want to ensure that both
        transaction participants can do this. '''
    def test_create_contracts(self):
        
        # Create contracts.
        for user in [self.buyer, self.seller]:
            for ctype in self.contract_types:
                request = self.factory.post(self.path, data={'ctype': ctype},
                            format='json')
                force_authenticate(request, user=user)
                response = self.view(request, self.transaction.pk)
                self.assertEquals(response.status_code, 201)
                
                # Reset, as we can only have one contract / user.
                Contract.objects.all().delete()
        
    ''' Ensure the same user cannot create more than one contract / transaction. '''
    def test_create_two_contracts_same_user(self):

        for i in range(2):
            request = self.factory.post(self.path, data={'ctype': 'condo'},
                        format='json')
            force_authenticate(request, user=self.buyer)
            response = self.view(request, self.transaction.pk)
            
        self.assertEquals(response.status_code, 400)

    ''' Attempt to create a contract on a transaction the user is not part of. '''
    def test_create_contract_wrong_transaction(self):

        request = self.factory.post(self.path, data={'ctype': 'condo'},
                    format='json')
        force_authenticate(request, user=self.wrong_user)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 403)
    
    ''' Attempt to create a contract without auth. '''
    def test_create_contract_no_auth(self):

        request = self.factory.post(self.path, data={'ctype': 'condo'},
                    format='json')
        force_authenticate(request, user=None)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 401)

    ''' Ensure transaction participants can GET (LIST) contracts. '''
    def test_get_contract(self):
        
        request = self.factory.post(self.path, data={'ctype': 'condo'},
                    format='json')
        force_authenticate(request, user=self.buyer)
        response = self.view(request, self.transaction.pk)

        request = self.factory.post(self.path, data={'ctype': 'condo'},
                    format='json')
        force_authenticate(request, user=self.seller)
        response = self.view(request, self.transaction.pk)

        for user in [self.buyer, self.seller]:
            request = self.factory.get(self.path, format='json')
            force_authenticate(request, user=user)
            response = self.view(request, self.transaction.pk)
            self.assertEquals(response.status_code, 200)
            self.assertEquals(len(response.data), 2)

    ''' Attempt to view a transaction the user is not part of. '''
    def test_get_contract_wrong_transaction(self):

        request = self.factory.get(self.path, format='json')
        force_authenticate(request, user=self.wrong_user)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 403)

    ''' Attempt to view a transaction without auth. '''
    def test_get_contract_no_auth(self):

        request = self.factory.get(self.path, format='json')
        force_authenticate(request, user=None)
        response = self.view(request, self.transaction.pk)
        self.assertEquals(response.status_code, 401)


'''   Tests for ContractDetail() view. '''
class TestContractList(APITestCase):

    def setUp(self):
        
        self.view = ContractDetail.as_view()
        self.factory = APIRequestFactory()
        
        # Create the buyer, and seller.
        self.buyer = User.objects.create_user(email='buyer@kangaa.xyz',
                        password='buyer_pwd')
        self.seller = User.objects.create_user(email='seller@kangaa.xyz',
                        password='seller_pwd')
        self.wrong_user = User.objects.create_user(email='wronguser@kangaa.xyz',
                        password='wronguser')

        # Create the property, and set up the necessary sub-models.
        self.kproperty = Condo.objects.create(owner=self.seller, n_bathrooms=1,
                            n_bedrooms=2, price=250000, sqr_ftg=3000, unit_num=11)
        Location.objects.create(kproperty=self.kproperty, address='74 Ulster St',
                    city="Toronto", country="Canada", province='Ontario',
                    postal_code='M1P0B2', latitude=43.773313, longitude=-79.258729)
        TaxRecords.objects.create(kproperty=self.kproperty)
        Historical.objects.create(kproperty=self.kproperty, last_sold_price=2000000,
                    last_sold_date='2011-08-14', year_built=2010)
        Features.objects.create(kproperty=self.kproperty, feature='Oven')
 
        self.transaction = Transaction.objects.create(buyer=self.buyer,
                seller=self.seller, kproperty=self.kproperty)
        
        ctype = 'condo'
        self.contract = AbstractContractFactory.create_contract(ctype,
                            self.buyer, self.transaction)
  
        self.path = '/v1/transactions/{}/contracts/{}'.\
                    format(self.transaction.pk, self.contract.pk)

    ''' Ensure that transaction participants can read Contract objects. '''
    def test_get_contract(self):

        for user in [self.buyer, self.seller]:
            request = self.factory.get(self.path, format='json')
            force_authenticate(request, self.buyer)
            response = self.view(request, self.transaction.pk, self.contract.pk)
            
            self.assertEquals(response.status_code, 200)
    
    ''' Attempt to get a contract on a transaction the user is not part of. '''
    def test_get_contract_wrong_transaction(self):

        request = self.factory.get(self.path, format='json')
        force_authenticate(request, self.wrong_user)
        response = self.view(request, self.transaction.pk, self.contract.pk)
        self.assertEquals(response.status_code, 403)
    
    ''' Attempt to get a contract without any auth. '''
    def test_get_contract_no_auth(self):

        request = self.factory.get(self.path, format='json')
        force_authenticate(request, None)
        response = self.view(request, self.transaction.pk, self.contract.pk)
        self.assertEquals(response.status_code, 401)

    ''' Ensure that updates are not allowed on contracts. '''
    def test_update_contract(self):

        request = self.factory.put(self.path, format='json')
        force_authenticate(request, self.buyer)
        response = self.view(request, self.transaction.pk, self.contract.pk)
        self.assertEquals(response.status_code, 405)
    
    ''' Ensure that transaction participants can delete Contract objects,
        but only if they are the owner. '''
    def test_get_contract(self):

        ctype = 'condo'
        seller_contract = AbstractContractFactory.create_contract(ctype,
                            self.seller, self.transaction)
        seller_path = '/v1/transactions/{}/contracts/{}'.\
                      format(self.transaction.pk, seller_contract.pk)
        
        # Buyer attempts to delete seller's contract.
        request = self.factory.delete(seller_path, format='json')
        force_authenticate(request, self.buyer)
        response = self.view(request, self.transaction.pk, seller_contract.pk)
        self.assertEquals(response.status_code, 403)
        
        # Seller attempts to delete seller's contract.
        request = self.factory.delete(self.path, format='json')
        force_authenticate(request, self.seller)
        response = self.view(request, self.transaction.pk, self.contract.pk)
        self.assertEquals(response.status_code, 403)

        # Buyer deletes their own contract. 
        request = self.factory.delete(self.path, format='json')
        force_authenticate(request, self.buyer)
        response = self.view(request, self.transaction.pk, self.contract.pk)
        self.assertEquals(response.status_code, 204)

        # Seller deletes their own contract.
        request = self.factory.delete(seller_path, format='json')
        force_authenticate(request, self.seller)
        response = self.view(request, self.transaction.pk, seller_contract.pk)
        self.assertEquals(response.status_code, 204)
        
    ''' Attempt to delete a contract on a transaction the user is not part of. '''
    def test_get_contract_wrong_transaction(self):

        request = self.factory.delete(self.path, format='json')
        force_authenticate(request, self.wrong_user)
        response = self.view(request, self.transaction.pk, self.contract.pk)
        self.assertEquals(response.status_code, 403)
    
    ''' Attempt to delete a contract without any auth. '''
    def test_get_contract_no_auth(self):

        request = self.factory.delete(self.path, format='json')
        force_authenticate(request, None)
        response = self.view(request, self.transaction.pk, self.contract.pk)
        self.assertEquals(response.status_code, 401)

'''   Tests for ClauseList() view. '''
class TestClauseList(APITestCase):

    def setUp(self):
        
        self.view = ClauseList.as_view()
        self.factory = APIRequestFactory()
        
        # Create the buyer, and seller.
        self.buyer = User.objects.create_user(email='buyer@kangaa.xyz',
                        password='buyer_pwd')
        self.seller = User.objects.create_user(email='seller@kangaa.xyz',
                        password='seller_pwd')
        self.wrong_user = User.objects.create_user(email='wronguser@kangaa.xyz',
                        password='wronguser')

        # Create the property, and set up the necessary sub-models.
        self.kproperty = Condo.objects.create(owner=self.seller, n_bathrooms=1,
                            n_bedrooms=2, price=250000, sqr_ftg=3000, unit_num=11)
        Location.objects.create(kproperty=self.kproperty, address='74 Ulster St',
                    city="Toronto", country="Canada", province='Ontario',
                    postal_code='M1P0B2', latitude=43.773313, longitude=-79.258729)
        TaxRecords.objects.create(kproperty=self.kproperty)
        Historical.objects.create(kproperty=self.kproperty, last_sold_price=2000000,
                    last_sold_date='2011-08-14', year_built=2010)
        Features.objects.create(kproperty=self.kproperty, feature='Oven')
 
        self.transaction = Transaction.objects.create(buyer=self.buyer,
                seller=self.seller, kproperty=self.kproperty)
        
        ctype = 'condo'
        self.contract = AbstractContractFactory.create_contract(ctype,
                            self.buyer, self.transaction)
  
        self.path = '/v1/transactions/{}/contracts/{}/clauses/'.\
                    format(self.transaction.pk, self.contract.pk)

    ''' Ensure that transaction participants can read (LIST) clauses. '''
    def test_get_clauses(self):
        
        for user in [self.buyer, self.seller]:
            request = self.factory.get(self.path, format='json')
            force_authenticate(request, user)
            response = self.view(request, self.transaction.pk, self.contract.pk)
            self.assertEquals(response.status_code, 200)
            self.assertGreater(len(response.data['static_clauses']), 0)

    ''' Attempt to read clauses on a transaction the user isn't part of. '''
    def test_get_clauses_on_wrong_transaction(self):

        request = self.factory.get(self.path, format='json')
        force_authenticate(request, self.wrong_user)
        response = self.view(request, self.transaction.pk, self.contract.pk)
        self.assertEquals(response.status_code, 403)

    ''' Attempt to read clauses without any auth. '''
    def test_get_clauses_no_auth(self):

        request = self.factory.get(self.path, format='json')
        force_authenticate(request, None)
        response = self.view(request, self.transaction.pk, self.contract.pk)
        self.assertEquals(response.status_code, 401)

'''   Tests for ClauseDetail() view. '''
class TestClauseDetail(APITestCase):

    def setUp(self):
        
        self.view = ClauseDetail.as_view()
        self.factory = APIRequestFactory()
        
        # Create the buyer, and seller.
        self.buyer = User.objects.create_user(email='buyer@kangaa.xyz',
                        password='buyer_pwd')
        self.seller = User.objects.create_user(email='seller@kangaa.xyz',
                        password='seller_pwd')
        self.wrong_user = User.objects.create_user(email='wronguser@kangaa.xyz',
                        password='wronguser')

        # Create the property, and set up the necessary sub-models.
        self.kproperty = Condo.objects.create(owner=self.seller, n_bathrooms=1,
                            n_bedrooms=2, price=250000, sqr_ftg=3000, unit_num=11)
        Location.objects.create(kproperty=self.kproperty, address='74 Ulster St',
                    city="Toronto", country="Canada", province='Ontario',
                    postal_code='M1P0B2', latitude=43.773313, longitude=-79.258729)
        TaxRecords.objects.create(kproperty=self.kproperty)
        Historical.objects.create(kproperty=self.kproperty, last_sold_price=2000000,
                    last_sold_date='2011-08-14', year_built=2010)
        Features.objects.create(kproperty=self.kproperty, feature='Oven')
 
        self.transaction = Transaction.objects.create(buyer=self.buyer,
                seller=self.seller, kproperty=self.kproperty)
        
        ctype = 'condo'
        self.contract = AbstractContractFactory.create_contract(ctype,
                            self.buyer, self.transaction)
        
        self.text_clause = self.contract.dynamic_clauses.\
                get(title='Deposit Deadline')
        self.toggle_clause = self.contract.dynamic_clauses.\
                get(title='Equipment').actual_type
        self.date_clause = self.contract.dynamic_clauses.\
                get(title='Completion Date').actual_type
        self.chip_clause = self.contract.dynamic_clauses.\
                get(title='Chattels Included')
        self.dropdown_clause = self.contract.dynamic_clauses.\
                get(title='Payment Method').actual_type
        self.static_clause = self.contract.static_clauses.all()[0]
        self.clauses = [(self.text_clause, 1), (self.toggle_clause, True),
                (self.date_clause, '2017-08-21'), (self.chip_clause, ['a', 'b']),
                (self.dropdown_clause, 'Cheque'), (self.static_clause, None)
        ]
  
    ''' Ensure that transaction participants can read clauses. '''
    def test_get_clause(self):

        for user in [self.buyer, self.seller]:
            for clause in self.clauses:
                clause = clause[0]
                clause_path = '/v1/transactions/{}/contracts/{}/clauses/{}/'.\
                    format(self.transaction.pk, self.contract.pk, clause.pk)
                request = self.factory.get(clause_path, format='json')
                force_authenticate(request, user)
                response = self.view(request, self.transaction.pk,
                        self.contract.pk, clause.pk)
                self.assertEquals(response.status_code, 200)

    ''' Attempt to read a clause on a transaction the user isn't part of. '''
    def test_get_clause_wrong_transaction(self):

        clause = self.clauses[0][0]
        clause_path = '/v1/transactions/{}/contracts/{}/clauses/{}/'.\
            format(self.transaction.pk, self.contract.pk, clause.pk)

        request = self.factory.get(clause_path, format='json')
        force_authenticate(request, self.wrong_user)
        response = self.view(request, self.transaction.pk, self.contract.pk, \
                    clause.pk)

        self.assertEquals(response.status_code, 403)
    
    ''' Attempt to read a clause on a transaction without auth. '''
    def test_get_clauses_no_auth(self):

        clause = self.clauses[0][0]
        clause_path = '/v1/transactions/{}/contracts/{}/clauses/{}/'.\
            format(self.transaction.pk, self.contract.pk, clause.pk)

        request = self.factory.get(clause_path, format='json')
        force_authenticate(request, None)
        response = self.view(request, self.transaction.pk, self.contract.pk, \
                    clause.pk)

        self.assertEquals(response.status_code, 401)

    ''' Ensure that only the clause / contract owner can edit the clause.
        We'll also want to make sure that the 'contracts_equal' field on
        our Transaction is updated accordingly. '''
    def test_update_clause(self):

        # Remove the static clause, as we can't update it.
        static_clause = self.clauses.pop()

        # Create a seller contract, and create a list of clauses. Note, we
        # want both contracts to have the same clauses in them.
        ctype = 'condo'
        seller_contract = AbstractContractFactory.create_contract(ctype,
                            self.seller, self.transaction)
        seller_text_clause = seller_contract.dynamic_clauses.\
                get(title='Deposit Deadline')
        seller_toggle_clause = seller_contract.dynamic_clauses.\
                get(title='Equipment').actual_type
        seller_date_clause = seller_contract.dynamic_clauses.\
                get(title='Completion Date').actual_type
        seller_chip_clause = seller_contract.dynamic_clauses.\
                get(title='Chattels Included')
        seller_dropdown_clause = seller_contract.dynamic_clauses.\
                get(title='Payment Method').actual_type
        seller_static_clause = seller_contract.static_clauses.all()[0]
        seller_clauses = [(seller_text_clause, 1), (seller_toggle_clause, True),
                (seller_date_clause, '2017-08-21'),
                (seller_chip_clause, ['a', 'b']),
                (seller_dropdown_clause, 'Cheque'),
        ]
    
        # Buyer attempts to update seller's clause.
        clause_path = '/v1/transactions/{}/contracts/{}/clauses/{}/'.\
            format(self.transaction.pk, seller_contract.pk, seller_clauses[0][0].pk)
        request = self.factory.put(
                clause_path, data={'value': seller_clauses[0][1]})
        force_authenticate(request, self.buyer)
        response = self.view(request, self.transaction.pk, seller_contract.pk,
                seller_clauses[0][0].pk)
        self.assertEquals(response.status_code, 403)

        # Seller attempts to update buyer's clause.
        clause_path = '/v1/transactions/{}/contracts/{}/clauses/{}/'.\
            format(self.transaction.pk, self.contract.pk, self.clauses[0][0].pk)
        request = self.factory.put(
                clause_path, data={'value': self.clauses[0][1]})
        force_authenticate(request, self.seller)
        response = self.view(request, self.transaction.pk, self.contract.pk,
                self.clauses[0][0].pk)
        self.assertEquals(response.status_code, 403)

        # Buyer updates clause.
        for clause in self.clauses:
            clause_path = '/v1/transactions/{}/contracts/{}/clauses/{}/'.\
                format(self.transaction.pk, self.contract.pk, clause[0].pk)
            request = self.factory.put(clause_path, data={"value": clause[1]},
                    format='json')
            force_authenticate(request, self.buyer)
            response = self.view(request, self.transaction.pk, self.contract.pk, \
                        clause[0].pk)
            
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.data['generator']['value'], clause[1])
        
        #TODO: Sort this out.
        #self.assertEquals(self.transaction.contracts_equal, False)

        # Seller updates corresponding clause on their contract to match
        for clause in seller_clauses:
            clause_path = '/v1/transactions/{}/contracts/{}/clauses/{}/'.\
                format(self.transaction.pk, seller_contract.pk, clause[0].pk)
            request = self.factory.put(clause_path, data={'value': clause[1]},
                    format='json')
            force_authenticate(request, self.seller)
            response = self.view(request, self.transaction.pk, seller_contract.pk, \
                        clause[0].pk)

            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.data['generator']['value'], clause[1])
        
        self.assertEquals(self.transaction.contracts_equal, True)
    
    ''' Attempt to update a clause on a transaction the user isn't part of. '''
    def test_update_clause_wrong_transaction(self):
        
        for clause in self.clauses:
            clause_path = '/v1/transactions/{}/contracts/{}/clauses/{}/'.\
                format(self.transaction.pk, self.contract.pk, clause[0].pk)
            request = self.factory.put(clause_path, data={'value': clause[1]},
                    format='json')
            force_authenticate(request, self.wrong_user)
            response = self.view(request, self.transaction.pk, self.contract.pk, \
                        clause[0].pk)
            self.assertEquals(response.status_code, 403)

    ''' Attempt to update without auth. '''
    def test_update_clause_no_auth(self):
        
        for clause in self.clauses:
            clause_path = '/v1/transactions/{}/contracts/{}/clauses/{}/'.\
                format(self.transaction.pk, self.contract.pk, clause[0].pk)
            request = self.factory.put(clause_path, data={'value': clause[1]},
                    format='json')
            force_authenticate(request, None)
            response = self.view(request, self.transaction.pk, self.contract.pk, \
                        clause[0].pk)
            self.assertEquals(response.status_code, 401)
    
    def test_delete_clause(self):
        
        # Remove the static clause, as we can't update it.
        self.clauses.pop()

        ctype = 'condo'
        seller_contract = AbstractContractFactory.create_contract(ctype,
                            self.seller, self.transaction)
        
        buyer_clause = self.clauses[0][0]
        seller_clause = seller_contract.dynamic_clauses.\
                get(title='Deposit Deadline')
        
        clause_path = '/v1/transactions/{}/contracts/{}/clauses/{}/'.\
            format(self.transaction.pk, self.contract.pk, buyer_clause.pk)
        seller_clause_path = '/v1/transactions/{}/contracts/{}/clauses/{}/'.\
            format(self.transaction.pk, seller_contract.pk, seller_clause.pk)

        # Buyer attempts to delete seller's clause.
        request = self.factory.delete(seller_clause_path, format='json')
        force_authenticate(request, self.buyer)
        response = self.view(request, self.transaction.pk, seller_contract.pk, \
                    seller_clause.pk)
        self.assertEquals(response.status_code, 403)
        
        # Seller attempts to delete seller's clause.
        request = self.factory.delete(clause_path, format='json')
        force_authenticate(request, self.seller)
        response = self.view(request, self.transaction.pk, self.contract.pk, \
                    buyer_clause.pk)
        self.assertEquals(response.status_code, 403)
    
        # Buyer deletes their clause.
        request = self.factory.delete(clause_path, format='json')
        force_authenticate(request, self.buyer)
        response = self.view(request, self.transaction.pk, self.contract.pk, \
                    buyer_clause.pk)
        self.assertEquals(response.status_code, 204)

        # Seller deletes their clause.
        request = self.factory.delete(seller_clause_path, format='json')
        force_authenticate(request, self.seller)
        response = self.view(request, self.transaction.pk, seller_contract.pk, \
                    seller_clause.pk)
        self.assertEquals(response.status_code, 204)

    ''' Attempt to delete a clause on a transaction the user isn't part of. '''
    def test_delete_clause_wrong_auth(self):
        
        clause = self.clauses.pop(0)
        clause_path = '/v1/transactions/{}/contracts/{}/clauses/{}/'.\
                    format(self.transaction.pk, self.contract.pk, clause[0].pk)
        request = self.factory.delete(clause_path, format='json')
        force_authenticate(request, self.wrong_user)
        response = self.view(request, self.transaction.pk, self.contract.pk, \
                    clause[0].pk)
        self.assertEquals(response.status_code, 401) 

    ''' Attempt to delete a clause without auth. '''
    def test_delete_clause_wrong_auth(self):
        
        clause = self.clauses.pop(0)
        clause_path = '/v1/transactions/{}/contracts/{}/clauses/{}/'.\
                    format(self.transaction.pk, self.contract.pk, clause[0].pk)
        request = self.factory.delete(clause_path, format='json')
        force_authenticate(request, None)
        response = self.view(request, self.transaction.pk, self.contract.pk, \
                    clause[0].pk)
        self.assertEquals(response.status_code, 401)
