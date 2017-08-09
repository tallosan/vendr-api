from django.contrib.auth import get_user_model

from oauth2_provider.models import Application, AccessToken

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.test import force_authenticate

from kproperty.views import *
from kproperty.models import *
from kproperty.serializers import *

User = get_user_model()


''' Generate an OAuth2 access token for user 'user'. '''
def get_access_token(user):

    application = Application.objects.get(name='test_kangaa')
    access_token = AccessToken.objects.create(user=user,
                    application=application, expires=None)

    return access_token


'''   Tests for the PropertyList() view. '''
class TestPropertyList(APITestCase):
    
    ''' Setup the view we're working with, the API path, and the data types. '''
    def setUp(self):

        self.view = PropertyList.as_view()
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(email='test@kanga.xyz', password='test')
        
        self.condo_path = '/v1/properties/?ptype=condo'
        self.house_path = '/v1/properties/?ptype=house'
        self.condo_data = {
                            "location": {
                                "address": "60 Brian Harrison", 
                                "city": "Toronto", 
                                "country": "Canada", 
                                "latitude": "43.773313", 
                                "longitude": "-79.258729", 
                                "postal_code": "M1P0B2", 
                                "province": "Ontario"
                            }, 
                            "n_bathrooms": 1, 
                            "n_bedrooms": 2, 
                            "price": 250000.0, 
                            "sqr_ftg": 3000.0,
                            "unit_num": 11,
                            "tax_records": [
                             ],
                             "history": {
                                 "last_sold_price": 20000,
                                 "last_sold_date": "2011-08-14",
                                 "year_built": 2010
                             },
                             "features": [
                                 { "feature": "Oven" },
                                 { "feature": "Pool" }
                             ],
                            "images": []
        }

        self.house_data = {
                            "location": {
                                "address": "18 Bay Street", 
                                "city": "Toronto", 
                                "country": "Canada", 
                                "latitude": "43.773313", 
                                "longitude": "-79.258729", 
                                "postal_code": "M230B3", 
                                "province": "Ontario"
                            }, 
                            "n_bathrooms": 3, 
                            "n_bedrooms": 3, 
                            "price": 4500000.0, 
                            "sqr_ftg": 4200.0,
                            "tax_records": [
                                {
                                        "assessment": 4250000,
                                        "assessment_year": 2016
                                }
                            ],
                            "history": {
                                "last_sold_price": 3200500,
                                "last_sold_date": "2012-11-03",
                                "year_built": 2007
                            },
                            "features": [],
                            "images": []
        }

    ''' POST: Create a condo model with authentication. '''
    def test_create_condo_with_auth(self):

        request = self.factory.post(self.condo_path, self.condo_data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        
        # Ensure that object is created.
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        
        # Ensure that 'owner' is set.
        self.assertEquals(response.data['owner'], self.user.id)

        #  Ensure that standard values are set propery.
        self.assertEquals(response.data['price'], self.condo_data['price'])

        # Ensure that condo specific values are set propery.
        self.assertEquals(response.data['unit_num'], self.condo_data['unit_num'])

        # Ensure that nested one-to-one values are set properly.
        self.assertEquals(response.data['location'], self.condo_data['location'])

        # Ensure that nested foreign key values are set properly.
        self.assertEquals(response.data['features'], self.condo_data['features'])

        # Ensure that empty foreign keys can be passed safely.
        self.assertEquals(len(response.data['tax_records']), 0)
    
    ''' POST: Create a house model with authentication. '''
    def test_create_house_with_auth(self):
 
        request = self.factory.post(self.house_path, self.house_data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        
        # Ensure that object is created.
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        
        # Ensure that 'owner' is set.
        self.assertEquals(response.data['owner'], self.user.id)

        #  Ensure that standard values are set propery.
        self.assertEquals(response.data['price'], self.house_data['price'])

        # Ensure that nested one-to-one values are set properly.
        self.assertEquals(response.data['location'], self.house_data['location'])

        # Ensure that nested foreign key values are set properly.
        self.assertEquals(response.data['features'], self.house_data['features'])
        self.assertEquals(len(response.data['tax_records']), 1)

    ''' POST: Create a property without authentication. '''
    def test_create_property_no_auth(self):
 
        request = self.factory.post(self.condo_path, self.condo_data, format='json')
        condo_response = self.view(request)
 
        request = self.factory.post(self.house_path, self.house_data, format='json')
        house_response = self.view(request)

        # Ensure that this fails due to a lack of authentication credentials.
        expected = { "detail": "Authentication credentials were not provided." }
        self.assertEqual(condo_response.data, expected)
        self.assertEqual(condo_response.status_code, 401)
        
        self.assertEqual(house_response.data, expected)
        self.assertEqual(house_response.status_code, 401)


'''   Tests for the PropertyDetail() view. '''
class TestPropertyDetail(APITestCase):

    def setUp(self):

        self.view = PropertyDetail.as_view()
        self.factory = APIRequestFactory()
        
        # Condo model owned by user 1.
        self.user = User.objects.create_user(email='test@kanga.xyz', password='test')
        condo = Condo.objects.create(owner=self.user,
                n_bathrooms=1, n_bedrooms=2, price=250000, sqr_ftg=3000, unit_num=11)
        Location.objects.create(kproperty=condo,
                address='60 Brian Harrison', city="Toronto", country="Canada",
                province='Ontario', postal_code='M1P0B2',
                latitude=43.773313, longitude=-79.258729
        )
        TaxRecords.objects.create(kproperty=condo)
        Historical.objects.create(kproperty=condo,
                last_sold_price=2000000, last_sold_date='2011-08-14',
                year_built=2010
        )
        Features.objects.create(kproperty=condo, feature='Oven')
        Features.objects.create(kproperty=condo, feature='Pool')

        # House model owned by alt user.
        self.user_a = User.objects.create(email='alt@kangaa.xyz', password='alt')
        house = House.objects.create(owner=self.user_a,
                n_bathrooms=3, n_bedrooms=3, price=4500000, sqr_ftg=4200)
        Location.objects.create(kproperty=house,
                address='18 Bay Street', city='Toronto', country='Canada',
                province='Ontario', postal_code='M230B3',
                latitude=43.773313, longitude=-79.258729
        )
        TaxRecords.objects.create(kproperty=house,
                assessment=4250000, assessment_year=2016)
        Historical.objects.create(kproperty=house,
                last_sold_price=3200500, last_sold_date='2012-11-03', year_built=2007)
        Features.objects.create(kproperty=house, feature='House Oven')
        Features.objects.create(kproperty=house, feature='Spa')

        self.condo_id = Condo.objects.all()[0].id
        self.house_id = House.objects.all()[0].id
    
        self.condo_path = '/v1/properties/' + str(self.condo_id)
        self.house_path = '/v1/properties/' + str(self.house_id)

    ''' PUT: Update a property model with authentication. '''
    def update_property_with_auth(self, property_path, property_id, p_user):
        
        # Test standard value updates.
        standard_update = { 'price' : 5000000 }
        request = self.factory.put(property_path, standard_update, format='json')
        force_authenticate(request, user=p_user)
        response = self.view(request, property_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], 5000000)

        # Test one-to-one key updates.
        one_to_one_update = {
                                'location': {
                                    'city': 'Amsterdam',
                                    'country': 'Holland'
                                }
        }
        request = self.factory.put(property_path, one_to_one_update, format='json')
        force_authenticate(request, user=p_user)
        response = self.view(request, property_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['location']['city'], 
                         one_to_one_update['location']['city'])
        self.assertEqual(response.data['location']['country'], 
                         one_to_one_update['location']['country'])
         
        # Test foreign key updates.
        foreign_key_update = {
                                'features': [
                                    { 'feature': 'Test1' },
                                    { 'feature': 'Test2' }
                                ]
        }
        request = self.factory.put(property_path, foreign_key_update, format='json')
        force_authenticate(request, user=p_user)
        response = self.view(request, property_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['features'][2],
                foreign_key_update['features'][0])
        self.assertEqual(response.data['features'][3],
                foreign_key_update['features'][1])

        # Test foreign key empty update.
        foreign_key_empty_update = { 'features': [] }
        request = self.factory.put(property_path, foreign_key_empty_update,
                format='json')
        force_authenticate(request, user=p_user)
        response = self.view(request, property_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['features'], foreign_key_empty_update['features'])

    ''' PUT: Update a condo model with authentication. '''
    def test_update_condo_with_auth(self):

        self.update_property_with_auth(self.condo_path, self.condo_id, self.user)

    ''' PUT: Update a house model with authentication. '''
    def test_update_house_with_auth(self):
        
        self.update_property_with_auth(self.house_path, self.house_id, self.user_a)

    ''' (Helper Function) Attempt a bad Update. '''
    def update_property_with_bad_auth(self, user, path, pid, expected_status):

        # Test standard value updates.
        standard_update = { 'price' : 0 }
        
        request = self.factory.put(path, standard_update, format='json')
        force_authenticate(request, user=user)
        response = self.view(request, pid)

        self.assertEqual(response.status_code, expected_status)

    ''' PUT: Attempt to update a model with the wrong auth. '''
    def test_update_property_wrong_auth(self):
        
        # user does not own this House  property. Ensure the update fails.
        self.update_property_with_bad_auth(user=self.user,
                path=self.house_path, pid=self.house_id,
                expected_status=status.HTTP_403_FORBIDDEN)

        # user_a does not own this Condo property. Ensure the update fails.
        self.update_property_with_bad_auth(user=self.user_a,
        path=self.condo_path, pid=self.condo_id,
        expected_status=status.HTTP_403_FORBIDDEN)

    ''' PUT: Update a property without authentication. '''
    def test_update_property_no_auth(self):

        # Attempt to update Condo model with no authentication details.
        self.update_property_with_bad_auth(user=None,
                path=self.condo_path, pid=self.condo_id,
                expected_status=status.HTTP_401_UNAUTHORIZED)

        # Attempt to update House model with no authentication details.
        self.update_property_with_bad_auth(user=None,
                path=self.house_path, pid=self.house_id,
                expected_status=status.HTTP_401_UNAUTHORIZED)

    ''' (Helper Function) Delete a property and ensure tha the response is
        what we're expecting. '''
    def delete_property(self, user, path, pid, expected_status):
         
        request = self.factory.delete(path)
        force_authenticate(request, user=user)
        response = self.view(request, pid)

        self.assertEqual(response.status_code, expected_status)

    ''' Delete a Condo model with the correct authentication. '''
    def test_delete_condo_with_auth(self):

        self.delete_property(user=self.user,
                path=self.condo_path, pid=self.condo_id,
                expected_status=status.HTTP_204_NO_CONTENT)

    ''' Delete a House model with the correct authentication. '''
    def test_delete_house_with_auth(self):

         self.delete_property(user=self.user_a,
                path=self.house_path, pid=self.house_id,
                expected_status=status.HTTP_204_NO_CONTENT)

    ''' Attempt to delete a Condo with the wrong authentication details. '''
    def test_delete_condo_with_wrong_auth(self):
 
         self.delete_property(user=self.user_a,
                path=self.condo_path, pid=self.condo_id,
                expected_status=status.HTTP_403_FORBIDDEN)

    ''' Attempt to delete a House with the wrong authentication details. '''
    def test_delete_house_with_auth(self):
 
         self.delete_property(user=self.user,
                path=self.house_path, pid=self.house_id,
                expected_status=status.HTTP_403_FORBIDDEN)

    ''' Attempt to delete a condo with no authentication details. '''
    def test_delete_property_no_auth(self):
      
        # Attempt to delete a Condo without any authentication.
        self.delete_property(user=None,
                path=self.condo_path, pid=self.condo_id,
                expected_status=status.HTTP_401_UNAUTHORIZED)
         
        # Attempt to delete a House without any authentication.
        self.delete_property(user=None,
                path=self.house_path, pid=self.house_id,
                expected_status=status.HTTP_401_UNAUTHORIZED)


'''   Tests on the OpenHouseList view. '''
class TestOpenHouseList(APITestCase):

    def setUp(self):

        self.view = OpenHouseList.as_view()
        self.factory = APIRequestFactory()
        
        # Test user.
        self.user = User.objects.create_user(email='test@kanga.xyz', password='test')
        self.user_a = User.objects.create(email='alt@kangaa.xyz', password='alt')
        
        # Condo model owned by user 1.
        self.condo = Condo.objects.create(owner=self.user,
                n_bathrooms=1, n_bedrooms=2, price=250000, sqr_ftg=3000, unit_num=11)
        Location.objects.create(kproperty=self.condo,
                address='60 Brian Harrison', city="Toronto", country="Canada",
                province='Ontario', postal_code='M1P0B2',
                latitude=43.773313, longitude=-79.258729
        )
        TaxRecords.objects.create(kproperty=self.condo)
        Historical.objects.create(kproperty=self.condo,
                last_sold_price=2000000, last_sold_date='2011-08-14',
                year_built=2010
        )
        Features.objects.create(kproperty=self.condo, feature='Oven')
        Features.objects.create(kproperty=self.condo, feature='Pool')

        # House model owned by alt user.
        self.house = House.objects.create(owner=self.user_a,
                n_bathrooms=3, n_bedrooms=3, price=4500000, sqr_ftg=4200)
        Location.objects.create(kproperty=self.house,
                address='18 Bay Street', city='Toronto', country='Canada',
                province='Ontario', postal_code='M230B3',
                latitude=43.773313, longitude=-79.258729
        )
        TaxRecords.objects.create(kproperty=self.house,
                assessment=4250000, assessment_year=2016)
        Historical.objects.create(kproperty=self.house,
                last_sold_price=3200500, last_sold_date='2012-11-03', year_built=2007)
        Features.objects.create(kproperty=self.house, feature='House Oven')
        Features.objects.create(kproperty=self.house, feature='Spa')

        self.condo_oh_path = '/v1/properties/{}/openhouses/'.format(self.condo.pk)
        self.house_oh_path = '/v1/properties/{}/openhouses/'.format(self.house.pk)

        # Open house data.
        self.oh_data = {
                "start": "2017-08-06T18:38:39.069638Z",
                "end": "2017-08-06T20:38:39.069638Z"
        }
 
    ''' Ensure users can create open houses on properties they own. '''
    def test_create_openhouse_on_owned_property(self):

        request = self.factory.post(self.condo_oh_path, self.oh_data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request, self.condo.pk)
        
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['start'], self.oh_data['start'])
        self.assertEquals(response.data['end'], self.oh_data['end'])

    ''' Ensure that users cannot create opne houses on properties they don't own. '''
    def test_create_openhouse_on_unowned_property(self):

        request = self.factory.post(self.house_oh_path, self.oh_data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request, self.house.pk)

        self.assertEquals(response.status_code, 403)

    ''' Ensure that anyone can access a property's open houses. '''
    def test_get_openhouse_on_owned_property(self):

        request = self.factory.get(self.condo_oh_path, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request, self.condo.pk)

        self.assertEquals(response.status_code, 200)
    
    ''' Ensure that anyone can access a property's open houses. '''
    def test_get_openhouse_on_unowned_property(self):

        request = self.factory.get(self.house_oh_path, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request, self.house.pk)

        self.assertEquals(response.status_code, 200)
     
    ''' Ensure that anonymous users cannot create open houses. '''
    def test_anon_create_openhouse(self):

        request = self.factory.post(self.house_oh_path, self.oh_data, format='json')
        force_authenticate(request, user=None)
        response = self.view(request, self.house.pk)

        self.assertEquals(response.status_code, 401)

    ''' Ensure that anonymous users can access a property's open houses. '''
    def test_anon_get_openhouse(self):

        request = self.factory.get(self.house_oh_path, format='json')
        force_authenticate(request, user=None)
        response = self.view(request, self.house.pk)

        self.assertEquals(response.status_code, 200)


'''   Tests on the OpenHouseDetail view. '''
class TestOpenHouseDetail(APITestCase):

    def setUp(self):

        self.view = OpenHouseDetail.as_view()
        self.factory = APIRequestFactory()
        
        # Test user.
        self.user = User.objects.create_user(email='test@kanga.xyz', password='test')
        self.user_a = User.objects.create(email='alt@kangaa.xyz', password='alt')
        
        # Condo model owned by user 1.
        self.condo = Condo.objects.create(owner=self.user,
                n_bathrooms=1, n_bedrooms=2, price=250000, sqr_ftg=3000, unit_num=11)
        Location.objects.create(kproperty=self.condo,
                address='60 Brian Harrison', city="Toronto", country="Canada",
                province='Ontario', postal_code='M1P0B2',
                latitude=43.773313, longitude=-79.258729
        )
        TaxRecords.objects.create(kproperty=self.condo)
        Historical.objects.create(kproperty=self.condo,
                last_sold_price=2000000, last_sold_date='2011-08-14',
                year_built=2010
        )
        Features.objects.create(kproperty=self.condo, feature='Oven')
        Features.objects.create(kproperty=self.condo, feature='Pool')

        # House model owned by alt user.
        self.house = House.objects.create(owner=self.user_a,
                n_bathrooms=3, n_bedrooms=3, price=4500000, sqr_ftg=4200)
        Location.objects.create(kproperty=self.house,
                address='18 Bay Street', city='Toronto', country='Canada',
                province='Ontario', postal_code='M230B3',
                latitude=43.773313, longitude=-79.258729
        )
        TaxRecords.objects.create(kproperty=self.house,
                assessment=4250000, assessment_year=2016)
        Historical.objects.create(kproperty=self.house,
                last_sold_price=3200500, last_sold_date='2012-11-03', year_built=2007)
        Features.objects.create(kproperty=self.house, feature='House Oven')
        Features.objects.create(kproperty=self.house, feature='Spa')

        # Open house data.
        self.oh_data = {
                "start": "2017-08-06T18:38:39.069638Z",
                "end": "2017-08-06T20:38:39.069638Z"
        }
        self.oh_a = OpenHouse.objects.create(owner=self.user,
                kproperty=self.condo, **self.oh_data)
        self.oh_b = OpenHouse.objects.create(owner=self.user_a,
                kproperty=self.house, **self.oh_data)
        
        self.condo_oh_path = '/v1/properties/{}/openhouse/{}/'.\
                             format(self.condo.pk, self.oh_a.pk)
        self.house_oh_path = '/v1/properties/{}/openhouses/{}/'.\
                             format(self.house.pk, self.oh_b.pk)

    ''' Ensure the open house owner can view their open house. '''
    def test_get_oh_on_owned_property(self):
        
        request = self.factory.get(self.condo_oh_path, format='json')
        force_authenticate(request, self.user)
        response = self.view(request, self.condo.pk, self.oh_a.pk)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['start'], self.oh_data['start'])
        self.assertEquals(response.data['end'], self.oh_data['end'])

    ''' Ensure that users can view open houses that they don't own. '''
    def test_get_oh_on_unowned_property(self):
        
        request = self.factory.get(self.house_oh_path, format='json')
        force_authenticate(request, self.user)
        response = self.view(request, self.house.pk, self.oh_b.pk)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['start'], self.oh_data['start'])
        self.assertEquals(response.data['end'], self.oh_data['end'])

    ''' Ensure that anyone can view an open house. '''
    def test_anonymous_oh_get(self):
        
        request = self.factory.get(self.house_oh_path, format='json')
        force_authenticate(request, None)
        response = self.view(request, self.house.pk, self.oh_b.pk)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['start'], self.oh_data['start'])
        self.assertEquals(response.data['end'], self.oh_data['end'])

    ''' Ensure that open house owners can update their open houses. '''
    def test_update_on_owned_openhouse(self):
        
        oh_update = {'start': '2017-08-06T20:38:39.069638Z'}
        request = self.factory.put(self.condo_oh_path, oh_update, format='json')
        force_authenticate(request, self.user)
        response = self.view(request, self.condo.pk, self.oh_a.pk)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['start'], oh_update['start'])

    ''' Ensure that users cannot update open houses they don't own. '''
    def test_update_on_unowned_openhouse(self):
        
        oh_update = {'start': '2017-08-06T20:38:39.069638Z'}
        request = self.factory.put(self.house_oh_path, oh_update, format='json')
        force_authenticate(request, self.user)
        response = self.view(request, self.house.pk, self.oh_b.pk)

        self.assertEquals(response.status_code, 403)

    ''' Ensure that anonymous users cannot update open houses. '''
    def test_anon_openhouse_update(self):
        
        oh_update = {'start': '2017-08-06T20:38:39.069638Z'}
        request = self.factory.put(self.house_oh_path, oh_update, format='json')
        force_authenticate(request, None)
        response = self.view(request, self.house.pk, self.oh_b.pk)

        self.assertEquals(response.status_code, 401)

    ''' Ensure open house owners can delete their own open house. '''
    def test_delete_on_owned_openhouse(self):
        
        request = self.factory.delete(self.condo_oh_path, format='json')
        force_authenticate(request, self.user)
        response = self.view(request, self.condo.pk, self.oh_a.pk)

        self.assertEquals(response.status_code, 204)

    ''' Ensure that users cannot delete open houses that they do not own. '''
    def test_delete_on_unowned_openhouse(self):
        
        request = self.factory.delete(self.house_oh_path, format='json')
        force_authenticate(request, self.user)
        response = self.view(request, self.house.pk, self.oh_b.pk)

        self.assertEquals(response.status_code, 403)

    ''' Ensure that anonymous users cannot delete open houses. '''
    def test_anon_openhouse_delete(self):
        
        request = self.factory.delete(self.house_oh_path, format='json')
        force_authenticate(request, None)
        response = self.view(request, self.house.pk, self.oh_b.pk)

        self.assertEquals(response.status_code, 401)


'''   Tests on the RSVPList view. '''
class TestRSVPList(APITestCase):

    def setUp(self):

        self.view = RSVPList.as_view()
        self.factory = APIRequestFactory()
        
        # Test user.
        self.user = User.objects.create_user(email='test@kanga.xyz', password='test')
        self.user_a = User.objects.create(email='alt@kangaa.xyz', password='alt')
        
        # Create a property
        self.condo = Condo.objects.create(owner=self.user,
                n_bathrooms=1, n_bedrooms=2, price=250000, sqr_ftg=3000, unit_num=11)
        Location.objects.create(kproperty=self.condo,
                address='60 Brian Harrison', city="Toronto", country="Canada",
                province='Ontario', postal_code='M1P0B2',
                latitude=43.773313, longitude=-79.258729
        )
        TaxRecords.objects.create(kproperty=self.condo)
        Historical.objects.create(kproperty=self.condo,
                last_sold_price=2000000, last_sold_date='2011-08-14',
                year_built=2010
        )
        Features.objects.create(kproperty=self.condo, feature='Oven')
        Features.objects.create(kproperty=self.condo, feature='Pool')
        
        # Open house data.
        self.oh_data = {
                "start": "2017-08-06T18:38:39.069638Z",
                "end": "2017-08-06T20:38:39.069638Z"
        }
        self.oh_a = OpenHouse.objects.create(owner=self.user,
                kproperty=self.condo, **self.oh_data)

        self.rsvp_data = {}
        self.rsvp_path = '/v1/properties/{}/openhouse/{}/rsvp/'.\
                             format(self.condo.pk, self.oh_a.pk)

    ''' Ensure that open house owners cannot RSVP to their own event. '''
    def test_create_rsvp_on_owned_property(self):

        request = self.factory.post(self.rsvp_path, self.rsvp_data, format='json')
        force_authenticate(request, self.user)
        response = self.view(request, self.condo.pk, self.oh_a.pk)

        self.assertEquals(response.status_code, 403)

    ''' Ensure that users can RSVP to other open houses. '''
    def test_create_rsvp_on_unowned_property(self):

        request = self.factory.post(self.rsvp_path, self.rsvp_data, format='json')
        force_authenticate(request, self.user_a)
        response = self.view(request, self.condo.pk, self.oh_a.pk)
        self.assertEquals(response.status_code, 201)

    ''' Ensure that anonymous users cannot RSVP to their own event. '''
    def test_anon_rsvp_create(self):

        request = self.factory.post(self.rsvp_path, self.rsvp_data, format='json')
        force_authenticate(request, None)
        response = self.view(request, self.condo.pk, self.oh_a.pk)

        self.assertEquals(response.status_code, 401)

    ''' Ensure the open house owner can view their open house. '''
    def test_get_rsvp_list_on_owned_property(self):
        
        request = self.factory.get(self.rsvp_path, format='json')
        force_authenticate(request, self.user)
        response = self.view(request, self.condo.pk, self.oh_a.pk)
        
        self.assertEquals(response.status_code, 200)
    
    ''' Ensure that users cannot view RSVP lists on open houses they don't own. '''
    def test_get_rsvp_list_on_unowned_property(self):
        
        request = self.factory.get(self.rsvp_path, format='json')
        force_authenticate(request, self.user_a)
        response = self.view(request, self.condo.pk, self.oh_a.pk)
        
        self.assertEquals(response.status_code, 403)

    ''' Ensure that anonymous users cannot access RSVP lists. '''
    def test_get_rsvp_list(self):
        
        request = self.factory.get(self.rsvp_path, format='json')
        force_authenticate(request, None)
        response = self.view(request, self.condo.pk, self.oh_a.pk)
        
        self.assertEquals(response.status_code, 401)


'''   Tests on the RSVPDetail view. '''
class TestRSVPDetail(APITestCase):

    def setUp(self):

        self.view = RSVPDetail.as_view()
        self.factory = APIRequestFactory()
        
        # Test user.
        self.user = User.objects.create_user(email='test@kanga.xyz', password='test')
        self.user_a = User.objects.create(email='alt@kangaa.xyz', password='alt')
        
        # Create a property
        self.condo = Condo.objects.create(owner=self.user,
                n_bathrooms=1, n_bedrooms=2, price=250000, sqr_ftg=3000, unit_num=11)
        Location.objects.create(kproperty=self.condo,
                address='60 Brian Harrison', city="Toronto", country="Canada",
                province='Ontario', postal_code='M1P0B2',
                latitude=43.773313, longitude=-79.258729
        )
        TaxRecords.objects.create(kproperty=self.condo)
        Historical.objects.create(kproperty=self.condo,
                last_sold_price=2000000, last_sold_date='2011-08-14',
                year_built=2010
        )
        Features.objects.create(kproperty=self.condo, feature='Oven')
        Features.objects.create(kproperty=self.condo, feature='Pool')
        
        # Open house data.
        self.oh_data = {
                "start": "2017-08-06T18:38:39.069638Z",
                "end": "2017-08-06T20:38:39.069638Z"
        }
        self.oh_a = OpenHouse.objects.create(owner=self.user,
                kproperty=self.condo, **self.oh_data)

        self.rsvp = RSVP.objects.create(open_house=self.oh_a, owner=self.user_a)
        self.rsvp_path = '/v1/properties/{}/openhouse/{}/rsvp/{}/'.\
                         format(self.condo.pk, self.oh_a.pk, self.rsvp.pk)

    ''' Ensure that open house owners can view any RSVP on their event. '''
    def test_get_on_unowned_rsvp_on_owned_open_house(self):

        request = self.factory.get(self.rsvp_path, format='json')
        force_authenticate(request, self.user)
        response = self.view(request, self.condo.pk, self.oh_a.pk, self.rsvp.pk)
        
        self.assertEquals(response.status_code, 200)

    ''' Ensure that users can view their own RSVPs. '''
    def test_get_on_owned_rsvp_on_unowned_open_house(self):

        request = self.factory.get(self.rsvp_path, format='json')
        force_authenticate(request, self.user_a)
        response = self.view(request, self.condo.pk, self.oh_a.pk, self.rsvp.pk)

        self.assertEquals(response.status_code, 200)

    ''' Ensure that anonymous users cannot view any RSVPs. '''
    def test_get_on_owned_rsvp_on_unowned_open_house(self):

        request = self.factory.get(self.rsvp_path, format='json')
        force_authenticate(request, None)
        response = self.view(request, self.condo.pk, self.oh_a.pk, self.rsvp.pk)

        self.assertEquals(response.status_code, 401)

    ''' Ensure that updates are not allowed on this endpoint. '''
    def test_update_on_rsvp(self):

        request = self.factory.put(self.rsvp_path, {}, format='json')
        for user in [self.user, self.user_a, None]:
            force_authenticate(request, user)
            response = self.view(request, self.condo.pk, self.oh_a.pk, self.rsvp.pk)

    ''' Ensure that open house owners can delete any RSVP on their event. '''
    def test_delete_on_unowned_rsvp_on_owned_open_house(self):

        request = self.factory.delete(self.rsvp_path, format='json')
        force_authenticate(request, self.user)
        response = self.view(request, self.condo.pk, self.oh_a.pk, self.rsvp.pk)
        
        self.assertEquals(response.status_code, 204)

    ''' Ensure that users can delete their own RSVPs. '''
    def test_delete_on_owned_rsvp_on_unowned_open_house(self):

        request = self.factory.delete(self.rsvp_path, format='json')
        force_authenticate(request, self.user_a)
        response = self.view(request, self.condo.pk, self.oh_a.pk, self.rsvp.pk)

        self.assertEquals(response.status_code, 204)

    ''' Ensure that anonymous users cannot delete any RSVPs. '''
    def test_get_on_owned_rsvp_on_unowned_open_house(self):

        request = self.factory.delete(self.rsvp_path, format='json')
        force_authenticate(request, None)
        response = self.view(request, self.condo.pk, self.oh_a.pk, self.rsvp.pk)

        self.assertEquals(response.status_code, 401)

