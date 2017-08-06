from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, APIClient, APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status

from kuser.models import KUser
from kproperty.models import Condo, Location, TaxRecords, Historical, Features
from transaction.models import Transaction, Offer, Contract
from transaction.views import *

User = get_user_model()


'''   Tests for UserList() view. '''
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
                            n_bedrooms=2, price=250000, sqr_ftg=3000, floor_num=11)
        Location.objects.create(kproperty=self.kproperty, address='60 Brian Harrison',
                            city="Toronto", country="Canada", province='Ontario',
                            postal_code='M1P0B2', latitude=43.773313, longitude=-79.258729)
        TaxRecords.objects.create(kproperty=self.kproperty)
        Historical.objects.create(kproperty=self.kproperty, last_sold_price=2000000,
                            last_sold_date='2011-08-14', year_built=2010)
        Features.objects.create(kproperty=self.kproperty, feature='Oven')

        self.transaction_data = {
                            "seller": self.seller.id,
                            "kproperty": self.kproperty.id,
        }

        self.path = '/v1/transactions/'

    ''' (Helper Function) Create a transaction. '''
    def create_transaction(self, expected_status):
       
        request = self.factory.post(self.path, self.transaction_data, format='json')
        force_authenticate(self.view)
        response = self.view(request)

        self.assertEqual(response.status_code, expected_status)
        
    ''' Create a transaction. '''
    def test_create_transaction(self):
        
        self.create_transaction(expected_status=status.HTTP_201_CREATED)

