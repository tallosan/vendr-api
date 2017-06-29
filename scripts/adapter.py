#
# Site Adapter
#
# ========================================================================


import requests
from lxml import html


class BaseAdapter(object):

    ''' Create an adapter for the given URL.
        Args:
            url -- The URL of the page we're adapting.
    '''
    def __init__(self, url):
        
        self.url     = url
        self.listing = {}

    ''' Parse a listing. Each child adapter should implement their own get_x()
        methods for each necessary attribute. '''
    def parse_listing(self):

        request = requests.get(self.url)
        tree = html.fromstring(request.content)

        self.listing = {
                            # Location.
                            'city': self.get_city(tree),
                            'province': self.get_province(tree),
                            'country': self.get_country(tree),
                            'address': self.get_address(tree),
                            'postal_code': self.get_postal_code(tree),
                            'longitude': self.get_geocoordinates(tree)['lng'],
                            'latitude': self.get_geocoordinates(tree)['lat'],
                     
                            # Financial.
                            'price': self.get_price(tree),

                            # Property Info.
                            'n_bedrooms': self.get_bedrooms(tree),
                            'n_bathrooms': self.get_bathrooms(tree),
                            'description': self.get_description(tree),
                            'images': self.get_images(tree)
        }
    
    ''' [Abstract] Get the city from the given HTML tree. '''
    def get_city(self, tree):
        raise NotImplementedError('error: all children must implement this.')

    ''' [Abstract] Get the province from the given HTML tree. '''
    def get_province(self, tree):
        raise NotImplementedError('error: all children must implement this.')

    ''' [Abstract] Get the country from the given HTML tree. '''
    def get_country(self, tree):
        raise NotImplementedError('error: all children must implement this.')

    ''' [Abstract] Get the address from the given HTML tree. '''
    def get_address(self, tree):
        raise NotImplementedError('error: all children must implement this.')

    ''' [Abstract] Get the postal code from the given HTML tree. '''
    def get_postal_code(self, tree):
        raise NotImplementedError('error: all children must implement this.')

    ''' [Abstract] Get the longitude and latitude from the given HTML tree. '''
    def get_geocoordinates(self, tree):
        raise NotImplementedError('error: all children must implement this.')

    ''' [Abstract] Get the asking price from the given HTML tree. '''
    def get_price(self, tree):
        raise NotImplementedError('error: all children must implement this.')

    ''' [Abstract] Get the number of bedrooms from the given HTML tree. '''
    def get_bedrooms(self, tree):
        raise NotImplementedError('error: all children must implement this.')

    ''' [Abstract] Get the number of bathrooms from the given HTML tree. '''
    def get_bathrooms(self, tree):
        raise NotImplementedError('error: all children must implement this.')

    ''' [Abstract] Get the property description from the given HTML tree. '''
    def get_description(self, tree):
        raise NotImplementedError('error: all children must implement this.')

    ''' Format the listing data into the Zapp listing JSON structure. '''
    def zapp_format(self):

        json = {}
        json['location'] = {
                "address": self.listing['address'],
                "city": self.listing['city'],
                "country": self.listing['country'],
                "province": self.listing['province'],
                "longitude": self.listing['longitude'],
                "latitude": self.listing['latitude'],
                "postal_code": self.listing['postal_code']
        }
        
        json['n_bedrooms'] = self.listing['n_bedrooms']
        json['n_bathrooms'] = self.listing['n_bathrooms']
        json['price'] = self.listing['price']
        json['description'] = self.listing['description']

        json['images'] = self.listing['images']
        
        return json


'''   Adapter for ComFree.com listings. '''
class ComFreeAdapter(BaseAdapter):

    def get_city(self, tree):

        city = tree.xpath('/html/body/div[6]/div[2]/header/div[1]/'
                          'div[1]/div[2]/meta[4]')[0]
        return city.attrib['content']

    def get_province(self, tree):

        province = tree.xpath('/html/body/div[6]/div[2]/header/div[1]/'
                              'div[1]/div[2]/meta[2]')[0]
        return province.attrib['content']

    def get_country(self, tree):

        country = tree.xpath('/html/body/div[6]/div[2]/header/div[1]/'
                             'div[1]/div[2]/meta[1]')[0]
        return country.attrib['content']

    def get_address(self, tree):

        address = tree.xpath('/html/body/div[6]/div[2]/header/div[1]/div[1]/'
                             'div[2]/meta[3]')[0]
        return address.attrib['content']

    def get_postal_code(self, tree):

        postal_code = tree.xpath('/html/body/div[6]/div[2]/header/div[1]/div[1]/'
                                 'div[2]/meta[5]')[0]
        return postal_code.attrib['content']

    def get_geocoordinates(self, tree):

        lng = tree.xpath('/html/body/div[6]/div[2]/header/div[1]/div[1]/'
                         'div[3]/meta[1]')[0]
        lat = tree.xpath('/html/body/div[6]/div[2]/header/div[1]/div[1]/'
                         'div[3]/meta[2]')[0]

        return {
                    'lng': lng.attrib['content'],
                    'lat': lat.attrib['content']
        }

    def get_price(self, tree):

        price = tree.xpath('/html/body/div[6]/div[2]/header/div[1]/div[2]/div[1]'
                           '/div[1]/div/meta[2]')[0]
        return price.attrib['content']

    def get_bedrooms(self, tree):
        
        bedrooms = tree.xpath('/html/body/div[6]/div[2]/section[1]/article/div[1]/'
                              'div[1]/span[1]')[0]
        return bedrooms.text_content()

    def get_bathrooms(self, tree):

        bathrooms = tree.xpath('/html/body/div[6]/div[2]/section[1]/article/div[1]/'
                               'div[2]/span[2]')[0]
        return bathrooms.text_content()

    def get_description(self, tree):

        description = tree.xpath('/html/body/div[6]/div[2]/section[1]/article/div[2]/'
                                 'div[1]')[0]
        return description.text_content().strip()

    def get_images(self, tree):

        from selenium import webdriver
        path = '/home/john/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
        driver = webdriver.PhantomJS(path)

        driver.get(self.url)
        images_wrapper = driver.find_elements_by_class_name('photo-viewer__slide')

        images = []
        for element in images_wrapper:
            index = int(element.get_attribute('data-slick-index'))
            wrap = element.find_element_by_xpath(
                        ".//div[@class='photo-viewer__slide__image-container']")
            image_element = wrap.find_element_by_class_name('photo-viewer__image')
            image = image_element.get_attribute('data-lazy')
            if not image:
                image = image_element.get_attribute('src')

            if image not in images:
                order = -1
                if index == 0: order = 0
                
                images.insert(order, image)

        return images

        
#
# ============================================================================

adapter_a = ComFreeAdapter(url='https://comfree.com/on/toronto-york-region-durham/'
                               'east-york/home-for-sale/hab-17-machockie-road-d18287416'
                               '#description')
adapter_b = ComFreeAdapter(url='https://comfree.com/on/toronto-york-region-durham/'
                               'maple/home-for-sale/hab-71-chayna-crescent-d18287459'
                               '#description')

listing_a = adapter_a.parse_listing()
listing_b = adapter_b.parse_listing()

zapp_a = adapter_a.zapp_format()
zapp_b = adapter_b.zapp_format()

print zapp_a
print
print zapp_b
print

