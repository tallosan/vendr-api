from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, APIClient, APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status

from kproperty.models import *

from kuser.models import KUser
from ksearch.views import *

User = get_user_model()


'''   Tests for SearchList() view. '''
class TestPropertySearchList(APITestCase):

    def setUp(self):
        
        self.view = PropertySearch.as_view()
        self.factory = APIRequestFactory()

        # Owner: self.user. Condo Model 0.
        self.user = User.objects.create_user(email='test@kanga.xyz', password='test')
        self.user_condo_0 = Condo.objects.create(owner=self.user,
                n_bathrooms=4, n_bedrooms=4, price=250000, sqr_ftg=3000,
                unit_num=11, parking_spaces=1)
        Location.objects.create(kproperty=self.user_condo_0,
                address='Robarts', city="Toronto", country="Canada",
                province='Ontario', postal_code='M1P0B2',
                latitude=43.664486, longitude=-79.399689
        )
        TaxRecords.objects.create(kproperty=self.user_condo_0,
                assessment=4250000, assessment_year=2016)
        Historical.objects.create(kproperty=self.user_condo_0,
                last_sold_price=2000000, last_sold_date='2011-08-14',
                year_built=2010
        )
        Features.objects.create(kproperty=self.user_condo_0, feature='Oven')
        Features.objects.create(kproperty=self.user_condo_0, feature='Pool')

        # Owner: self.user. Condo Model 1.
        self.user_condo_1 = Condo.objects.create(owner=self.user,
                n_bathrooms=4, n_bedrooms=4, price=10500000, sqr_ftg=8000,
                unit_num=100, parking_spaces=1, corporation_name='Super Condos')
        Location.objects.create(kproperty=self.user_condo_1,
                address='CN Tower', city="Toronto", country="Canada",
                province='Ontario', postal_code='M1P0B2',
                latitude=43.773313, longitude=-79.258729
        )
        TaxRecords.objects.create(kproperty=self.user_condo_1)
        Historical.objects.create(kproperty=self.user_condo_1,
                last_sold_price=9500000, last_sold_date='2011-08-14',
                year_built=2010
        )
        Features.objects.create(kproperty=self.user_condo_1, feature='Private Balcony')
        Features.objects.create(kproperty=self.user_condo_1, feature='Heated Pool')

        # Owner: self.user. House Model 0.
        self.user_house_0 = House.objects.create(owner=self.user,
                n_bathrooms=3, n_bedrooms=3, price=4500000, sqr_ftg=4200)
        Location.objects.create(kproperty=self.user_house_0,
                address='18 Bay Street', city='Toronto', country='Canada',
                province='Ontario', postal_code='M230B3',
                latitude=43.773313, longitude=-79.258729
        )
        TaxRecords.objects.create(kproperty=self.user_house_0,
                assessment=4250000, assessment_year=2016)
        Historical.objects.create(kproperty=self.user_house_0,
                last_sold_price=3200500, last_sold_date='2012-11-03', year_built=2007)
        Features.objects.create(kproperty=self.user_house_0, feature='House Oven')
        Features.objects.create(kproperty=self.user_house_0, feature='Spa')

        # Owner: self.user_a. House Model 0.
        self.user_a = User.objects.create(email='alt@kangaa.xyz', password='alt')
        self.user_a_house_0 = House.objects.create(owner=self.user_a,
                n_bathrooms=3, n_bedrooms=3, price=4500000, sqr_ftg=4200)
        Location.objects.create(kproperty=self.user_a_house_0,
                address='18 Bay Street', city='Toronto', country='Canada',
                province='Ontario', postal_code='M230B3',
                latitude=43.773313, longitude=-79.258729
        )
        TaxRecords.objects.create(kproperty=self.user_a_house_0,
                assessment=4250000, assessment_year=2016)
        Historical.objects.create(kproperty=self.user_a_house_0,
                last_sold_price=3200500, last_sold_date='2012-11-03', year_built=2007)
        Features.objects.create(kproperty=self.user_a_house_0, feature='House Oven')
        Features.objects.create(kproperty=self.user_a_house_0, feature='Spa') 
        
        self.path = '/v1/search?stype=property'

    ''' (Helper Function) Search for a property with the given filters. '''
    def search_property(self, filters):
	
        request = self.factory.get(self.path + filters, format='json')
        request.GET._mutable = True; request.GET.pop('stype')[0]
        force_authenticate(self.view)
        response = self.view(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
	return response.data

    ''' Search on a standard (non-nested or foreign-key) value. '''
    def test_standard_value(self):
        
        filters = '&price=10500000'
	data    = self.search_property(filters=filters)
	self.assertEqual(len(data), 1)
	self.assertEqual(data[0]['id'], self.user_condo_1.id)

    ''' Complex search on a standard value. '''
    def test_complex_standard_value(self):

        filters = '&price__gt=0'
	data    = self.search_property(filters=filters)
	self.assertEqual(len(data), Property.objects.all().count())
	for kproperty in data:
		self.assertGreater(kproperty['price'], 0)

    ''' Search on multiple standard values. '''
    def test_multiple_standard_values(self):
        
	filters = '&n_bathrooms=3&n_bedrooms=3'
	data    = self.search_property(filters=filters)
	self.assertEqual(len(data), 2)
	for kproperty in data:
		self.assertEqual(kproperty['n_bathrooms'], 3)
		self.assertEqual(kproperty['n_bedrooms'], 3)

    ''' Complex search on multiple standard values. '''
    def test_complex_multiple_standard_values(self):
 
	filters = '&n_bathrooms__gt=3&price__lt=10500000'
	data    = self.search_property(filters=filters)
	self.assertEqual(len(data), 1)
	self.assertEqual(data[0]['id'], self.user_condo_0.id)
    
    ''' Search on a standard (non-nested or foreign-key) value that
        doesn't exist. '''
    def test_non_existent_standard_value(self):
	
	filters = '&penguins=0'
    	request = self.factory.get(self.path + filters, format='json')
        request.GET._mutable = True; request.GET.pop('stype')[0]
        force_authenticate(self.view)
        response = self.view(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
	
    ''' Search on a nested value. '''
    def test_nested_value(self):
        
	filters = '&location__city=Toronto'
	data    = self.search_property(filters=filters)
	for kproperty in data:
		self.assertEqual(kproperty['location']['city'], 'Toronto')

    ''' Complex search on a nested value. '''
    def test_complex_nested_value(self):
 	
        filters = '&history__year_built__gt=2000'
	data    = self.search_property(filters=filters)
	for kproperty in data:
		self.assertGreater(kproperty['history']['year_built'], 2000)

    ''' Search on multiple nested values. '''
    def test_multiple_nested_values(self):
         
	filters = '&location__city=Toronto&history__year_built=2007'
	data    = self.search_property(filters=filters)
	for kproperty in data:
		self.assertEqual(kproperty['location']['city'], 'Toronto')
		self.assertEqual(kproperty['history']['year_built'], 2007)
        
    ''' Complex search on multiple nested values. '''
    def test_complex_multiple_nested_values(self):
	
        filters = '&history__last_sold_price__lt=1000000&history__year_built__gt=2007'
	data    = self.search_property(filters=filters)
	for kproperty in data:
		self.assertLess(kproperty['history']['last_sold_price'], 1000000)
		self.assertGreater(kproperty['history']['year_built'], 2007)
 
    ''' Search on non-existent nested value. '''
    def test_non_existent_nested_values(self):
	
	filters = '&penguins__count=0'
    	request = self.factory.get(self.path + filters, format='json')
        request.GET._mutable = True; request.GET.pop('stype')[0]
        force_authenticate(self.view)
        response = self.view(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
	
    ''' Search on standard and nested values. '''
    def test_standard_and_nested_values(self):
     
	filters = '&price=4500000&location__city=Toronto'
	data    = self.search_property(filters=filters)
	for kproperty in data:
		self.assertEqual(kproperty['price'], 4500000)
		self.assertEqual(kproperty['location']['city'], 'Toronto')

    ''' Complex search on standard and nested values. '''
    def test_complex_standard_and_nested_values(self):
 	
        filters = '&price__lt=500000&history__last_sold_price__lt=500000'
	data    = self.search_property(filters=filters)
	for kproperty in data:
                self.assertLess(kproperty['price'], 500000)
		self.assertLess(kproperty['history']['last_sold_price'], 500000)

    ''' Search on multiple standard and nested values. '''
    def test_multiple_standard_and_nested_values(self):
 	
        filters = '&n_bedrooms=3&n_bathrooms=3&' + \
                  'location__city=Toronto&location__province=Ontario'
	data    = self.search_property(filters=filters)
	for kproperty in data:
            self.assertEqual(kproperty['n_bedrooms'], 3)
            self.assertEqual(kproperty['n_bathrooms'], 3)
            self.assertEqual(kproperty['location']['city'], 'Toronto')
            self.assertEqual(kproperty['location']['province'], 'Ontario')

    ''' Complex search on multiple standard, and multiple nested, values. '''
    def test_complex_multiple_standard_and_nested_values(self):

        filters = '&n_bedrooms__gt=1&n_bathrooms__gt=1&' + \
                  'history__year_built__gt=2007&history__last_sold_price__lt=500000'
        data    = self.search_property(filters=filters)
	for kproperty in data:
            self.assertGreater(kproperty['n_bedrooms'], 1)
            self.assertGreater(kproperty['n_bathrooms'], 1)
	    self.assertGreater(kproperty['history']['year_built'], 2007)
	    self.assertLess(kproperty['history']['last_sold_price'], 500000)

    ''' Test a standard Geo query. '''
    def test_standard_geoquery(self):

        filters = '&ne_lat=43.66710833569532&ne_lng=-79.39544247525657&sw_lat=43.65322290778837&sw_lng=-79.4123940362307'
        data = self.search_property(filters=filters)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['location']['address'], 'Robarts')
    
    ''' Test a Geo query chained with a standard filter. '''
    def test_multiple_standard_geoquery(self):

        filters = '&ne_lat=43.66710833569532&ne_lng=-79.39544247525657&sw_lat=43.65322290778837&sw_lng=-79.4123940362307&price__gt=0'
        data = self.search_property(filters=filters)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['location']['address'], 'Robarts')
    
    ''' Test a Geo query with a nested value. '''
    def test_nested_standard_geoquery(self):

        filters = '&ne_lat=43.66710833569532&ne_lng=-79.39544247525657&sw_lat=43.65322290778837&sw_lng=-79.4123940362307&location__address=Robarts'
        data = self.search_property(filters=filters)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['location']['address'], 'Robarts')

    ''' Test basic pagination. We should only get one result back. '''
    def test_basic_pagination(self):

        filters = '&limit=1&offset=0'
        data = self.search_property(filters=filters)
        self.assertEqual(len(data), 1)

    ''' Test invalid pagination, with limit == 0. This should raise an error. '''
    def test_invalid_pagination(self):

        filters = '&limit=0&offset=0'
        request = self.factory.get(self.path + filters, format='json')
        request.GET._mutable = True; request.GET.pop('stype')[0]
        force_authenticate(self.view)
        response = self.view(request)

        self.assertEqual(response.status_code, 401)
        
