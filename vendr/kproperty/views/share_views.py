#
# Script that shares Vendr listings.
#
# Inspired by:
# https://www.quora.com/How-does-Airbnb-automatically-post-on-Craigslist
#
# Gives a user the ability to post their Vendr listing on any of the major
# FSBO sites, simply with the click of a button.
#
# Note, users on these FSBO sites cannot interact with the listing there;
# instead, they will need to visit Vendr.
#
# Craigslist 'API' reference:
# https://www.craigslist.org/about/bulk_posting_interface#submission_format
#
# ====================================================================

import requests
import feedparser
from lxml import etree

from django.apps import apps
from django.conf import settings

from rest_framework.views import APIView

from kproperty.models import Property


"""   This class is essentially a C struct. We're using this because
      it gives us a cleaner design and more flexibility when it comes to
      resolving the Craigslist area and subarea abbreviatins. """
class Area(object):
    def __init__(self, city, areas, subareas):
        self.city = city
        self.areas = areas
        self.subareas = subareas


class VendrShare(APIView):

    url = 'https://post.craigslist.org/bulk-rss/post'

    """ POST a Vendr property to Craigslist. """
    def post(self, request, pk, *args, **kwargs):

        # Get the property.
        model_type = Property.objects.filter(pk=pk).\
                        values_list('_type', flat=True)[0]
        model = apps.get_model(app_label='kproperty', model_name=model_type)
        kproperty = model.objects.get(pk=pk)

        self.username = 'andrew.tallos@mail.utoronto.ca'
        self.password = '_'
        self.account_id = ''

        self.resource = 'vendr-share-{}'.format(kproperty.pk)
        self.href = '{}{}'.format(settings.BASE_URL,
                request.path.replace('/share', '').replace('/v1/', ''))

        self.post_body = self._format_listing(kproperty)

    """ Formats a Vend property's details into a valid Craigslist
        RSS posting.
        Args:
            kproperty (Property) -- The property we're posting.
    """
    def _format_listing(self, kproperty):

        # Craigslist RSS header.
        clist = {}
        clist['header'] = (
            """
            <?xml version="1.0"?>
               <rdf:RDF xmlns="http://purl.org/rss/1.0/"
                    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                    xmlns:cl="http://www.craigslist.org/about/cl-bulk-ns/1.0">
                </rdf:RDF>
            """
        )

        # Property PK, username, password, account ID.
        clist['channel'] = (
            """
            <channel>
                <items>
                    <rdf:li rdf:resource="{}"/>
                </items>
                <cl:auth username="{}"
                         password="{}"
                         accountID="{}"/>
            </channel>
            """
        ).format(self.resource,
                self.username, self.password, self.account_id
        )
    
        # Listing title and description.
        title = 'FSBO: {}'.format(kproperty.location.address)
        clist['item_meta'] = (
            """
                <title>Spacious Sunny Studio in Upper West Side</title>
                <description><![CDATA[
                    {}
                ]]></description>
            """
        ).format(title, kproperty.description)

        # Listing locational info.
        clist['item_location'] = (
            """
                <cl:mapLocation city={}
                                postal={}
                                latitude={}
                                longitude={}
                </cl:mapLocation>
            """
        ).format(kproperty.location.city, kproperty.location.postal_code,
                 kproperty.location.latitude, kproperty.location.longitude)

        # Listing details.
        clist['item_property_info'] = (
            """
                <cl:housingInfo price="{}"
                                bedrooms="{}"
                                sqft="{}"/>
                <cl:housing_basics bathrooms={}
                                   housing_type={}
                </cl:housing_basics>
            """
        ).format(kproperty.price, kproperty.n_bedrooms, kproperty.sqr_ftg,
                kproperty.n_bathrooms, kproperty._type)

        # Listing contact info.
        clist['item_contact_info'] = (
            """
                <cl:replyEmail privacy="A"
                               outsideContactOK="0"
                               otherContactInfo="To contact the owner, visit: {}"
                </cl:replyEmail>
            """
        ).format(self.href)

        # Listing images.
        clist['item_images'] = (
            """
                <cl:image position="{}">
                    {}
                </cl:image>
            """
        ).format(kproperty.display_pic, kproperty.images)

        # The property we're uploading.
        # Note, we're hardcoding the category to `nfb`, which is
        # the Craigslist FSBO category.
        # Also, we'll need to resolve the property area and subarea
        # to match those listed by Craigslist.
        area, subarea = self._resolve_area(
                kproperty.location.city, kproperty.location.address
        )
        neighborhood = kproperty.location.address
        clist['item'] = (
            """
            <item rdf:about="{}">
                <cl:category>nfb</cl:category>
                <cl:area>{}</cl:area>
                <cl:subarea>{}</cl:subarea>
                <cl:neighborhood>{}</cl:neighborhood>
                <cl:price>{}</cl:price>
                {}
                {}
                {}
                {}
                {}
            </item>
            """
        ).format(self.resource, area, subarea, neighborhood, kproperty.price,
                clist['item_meta'], clist['item_location'],
                clist['item_property_info'], clist['item_contact_info'],
                clist['item_images']
        )

        return clist['header'] + clist['item']

    """ Takes the Property city & address & returns the closest
        match from the Craigslist `Areas and Subareas` list.
        Args:
            city (str) -- The property city.
            address (str) -- The property address.
    """
    def _resolve_area(self, city, address):
        
        # Dummy data.
        data = [
                'tor, toronto, bra, brampton-caledon'.split(', '),
                'tor, toronto, drh, durham region'.split(', '),
                'tor, toronto, mss, mississauga'.split(', '),
                'tpa, tamp bay area, , '.split(', ')
        ]

        # Format the data into a hashmap, where they key is the city,
        # and the value is an `Area` object.
        areas_and_subareas = {}
        for entry in data:
            city = entry[1]; area = entry[0]
            subareas = (entry[2], entry[3])
            if city in areas_and_subareas.keys():
                areas_and_subareas[city].areas.append(area)
                areas_and_subareas[city].subareas.append(subareas)
            else:
                cl_city = Area(city=city, areas=[area], subareas=[subareas])
                areas_and_subareas[city] = cl_city

        area_abv = None; subarea_abv = None

        # TODO:
        # 1. Get the area abbrevation.
        #
        # Use the Damerau-Levenshtein Distance to determine the
        # closest `Area` match for our city. This will be the entry with the
        # min Damerau-Levenshtein distance.
        #
        # Once we have the `Area` match, we can easily access its
        # `area` field to get the desired abbreviation.
        #
        # 2. Get the subarea abbreveation (if any).
        #
        # Using the same `Area` object, we again apply the L-D distance
        # algorithm to find (if any) the closest match for our subarea.
        return (area_abv, subarea_abv)

