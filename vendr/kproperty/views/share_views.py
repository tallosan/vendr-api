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
import textwrap
import itertools
import base64

from django.apps import apps
from django.conf import settings

from rest_framework.views import APIView

from kproperty.models import Property


"""   This class is essentially a C struct. We're using this because
      it gives us a cleaner design and more flexibility when it comes to
      resolving the Craigslist area and subarea abbreviatins. """
class Area(object):

    def __init__(self, city, area_abv, subareas, subarea_abvs):

        self.city = city
        self.area_abv = area_abv
        self.subareas = subareas
        self.subarea_abvs = subarea_abvs

    def __str__(self):

        return 'city: {}, area_abv: {}, subareas: {}, subarea_abvs: {}'.\
                format(self.city, self.area_abv,
                    self.subareas, self.subarea_abvs)


class VendrShare(APIView):

    clist_url = 'https://post.craigslist.org/bulk-rss/post'

    """ POST a Vendr property to Craigslist. """
    def post(self, request, pk, *args, **kwargs):

        # Get the property.
        model_type = Property.objects.filter(pk=pk).\
                        values_list('_type', flat=True)[0]
        model = apps.get_model(app_label='kproperty', model_name=model_type)
        kproperty = model.objects.get(pk=pk)

        self.username = 'andrew.tallos@gmail.com'
        self.password = 'iZappNewton77'
        self.account_id = ''

        self.resource = 'vendr-share-{}'.format(kproperty.pk)
        self.href = '{}{}'.format(settings.BASE_URL,
                request.path.replace('/share', '').replace('/v1/', ''))
        self.vendr_descr = ('For more information about this property'
                'visit: {}').format(self.href)

        # POST to RSS feed.
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        self.post_body = self._format_listing(kproperty)
        r = requests.post(self.clist_url,
                data=self.post_body,
                headers=headers
        )

        #TODO: Get an account ID!

    """ Formats a Vend property's details into a valid Craigslist
        RSS posting.
        Args:
            kproperty (Property) -- The property we're posting.
    """
    def _format_listing(self, kproperty):

        # Note, it is imperative to understand how Craigslist parses
        # the RSS, as they also use their own craigslist-specific
        # elements (which unfortunately are not well documented).
        # If a tag has values inside it, then it will be closed with:
        # `</tag>`
        # For example: <tag attra="attra">Hello, world!</tag>
        # If not, then it will be closed with:
        # `/>`
        # For example: <tag attra="attra"  attrb="attrb"/>
        clist = {}

        # Craigslist RSS header.
        clist['header'] = (
            """
            <rdf:RDF xmlns="http://purl.org/rss/1.0/"
                     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                     xmlns:cl="http://www.craigslist.org/about/cl-bulk-ns/1.0">
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
        descr = kproperty.description + self.vendr_descr
        clist['item_meta'] = (
            """
                    <title>{}</title>
                    <description><![CDATA[
                        {}
                    ]]></description>
            """
        ).format(title, descr)

        # Listing locational info.
        clist['item_location'] = (
            """
                    <cl:mapLocation city="{}"
                                    postal="{}"
                                    latitude="{}"
                                    longitude="{}"
                    />
            """
        ).format(kproperty.location.city, kproperty.location.postal_code,
                 kproperty.location.latitude, kproperty.location.longitude)

        # Listing details.
        clist['item_property_info'] = (
            """
                    <cl:housingInfo price="{}"
                                    bedrooms="{}"
                                    sqft="{}"
                    />
                    <cl:housing_basics bathrooms="{}"
                                    housing_type="{}"
                    />
            """
        ).format(kproperty.price, kproperty.n_bedrooms, kproperty.sqr_ftg,
                kproperty.n_bathrooms, kproperty._type)

        # Listing contact info.
        clist['item_contact_info'] = (
            """
                    <cl:replyEmail privacy="A"
                                   outsideContactOK="0"
                                   otherContactInfo="To contact the owner, visit: {}"
                   />
            """
        ).format(self.href)

        # Listing images.
        assert kproperty.images.all().count() > 0, (
                'error: property must have images.'
        )
        clist['item_images'] = ''
        images = self._format_images(kproperty.images, kproperty.display_pic)
        for image in images:
            clist['item_images'] += (
                """
                    <cl:image position="{}">{}
                    </cl:image>
                """
            ).format(image[0], image[1])

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
            </rdf:RDF>
            """
        ).format(self.resource, area, subarea, neighborhood, kproperty.price,
                clist['item_meta'], clist['item_location'],
                clist['item_property_info'], clist['item_contact_info'],
                clist['item_images']
        )

        return textwrap.dedent(
                clist['header'] + clist['channel'] + clist['item']
        )

    """ Craigslist needs images to be base 64 encoded. We don't do
        this by default on Vendr, so it's necessary to manually
        step through and generate these strings ourselves.
        Args:
            images (Image) -- The images associated with the property.
            display_pic (int) -- The image to use as the display pic.
    """
    def _format_images(self, images, display_pic):

        # Note, we want to be careful w/the image position. By setting
        # the position to `i + 1` we can ensure that only one element
        # is has position == 0.
        image_data = []
        for i in range(len(images.all())):
            image = requests.get(images.all()[i].image.name).content
            image_b64 = base64.b64encode(image)

            pos = i + 1
            if i == display_pic:
                pos = 0

            image_data.append([pos, image_b64])
        
        return image_data

    """ Takes the Property city & address & returns the closest
        match/s from the Craigslist `Areas and Subareas` list. The
        return value is a tuple formatted like (area_abv, addr_abv).
        Args:
            target_city (str) -- The property city.
            target_address (str) -- The property address.
    """
    def _resolve_area(self, target_city, target_address):
        
        # Dummy data.
        data = [
                'tor, toronto, bra, brampton-caledon'.split(', '),
                'tor, toronto, drh, durham region'.split(', '),
                'tor, toronto, mss, mississauga'.split(', '),
                'tor, toronto, yrk, york'.split(', '),
                'tpa, tamp bay area, tmp, tampa'.split(', '),
                'trn, torino, ita, italy'.split(', ')
        ]

        # Format the data into a hashmap, where they key is the city,
        # and the value is an `Area` object.
        clist_location_rss = {}
        for entry in data:
            city = entry[1]; area_abv = entry[0]
            subarea = entry[3]; subarea_abv = entry[2]
            if city in clist_location_rss.keys():
                clist_location_rss[city].subareas.append(subarea)
                clist_location_rss[city].subarea_abvs.append(subarea_abv)
            else:
                cl_city = Area(city=city, area_abv=area_abv,
                            subareas=[subarea], subarea_abvs=[subarea_abv])
                clist_location_rss[city] = cl_city

        # Get the closest match for our target city and its address
        # (if any) in the Craigslist city & subarea list.
        # Note, we're using Levenshtein distance to do this.
        clist_city_key = self._get_closest_match(target_city.lower(),
                clist_location_rss.keys())
        clist_location = clist_location_rss[clist_city_key]
        area_abv = clist_location.area_abv
        subarea_abv = self._get_closest_match(target_address.lower(),
                clist_location.subareas) if target_address else None

        return (area_abv, subarea_abv)

    """ Returns the closest match from a target string, and a list
        of potential string matches. Note, we're using the
        Levenshtein distance to determine string proximity.
        Args:
            target (str) -- The string we're trying to match.
            potential_matches (list of str) -- Potential matches.
    """
    def _get_closest_match(self, target, potential_matches):

        ld_min = (float('inf'), '')
        target = target.lower().replace(' ', '')
        for match in potential_matches:
            city_ld = get_levenshtein(target, match.lower())
            if city_ld < ld_min[0]:
                ld_min = (city_ld, match)

        return ld_min[1]

    
""" Calculate the Levenshtein distance between two strings.
    Note, we're not using the Damerau-Levenshtein distance here,
    because transposing can possibly lead to very poor results. No
    results is better than a poor result here; imagine posting a
    property in Toronto to the Ottawa section!
    Also worth noting is that we're after efficiency here, and don't
    much care for the rearranged string. Thus, we can achieve a
    runtime of O(N) by using two matrices for each string instead of
    constructing one large N x M matrix ala Wagner-Fischer.
    Args:
        `n` (str) -- The first string to compare.
        `m` (str) -- The second string to compare.
"""
def get_levenshtein(n, m):
    
    # Zip the two strings together into a set of pairs.
    # If one string is longer than the other, we'll get a pair of
    # (longer_str_char, None) tuples.
    levenshtein_distance = 0
    for _n, _m in itertools.izip_longest(n, m):

        # Substitution.
        if (_n and _m) and (_n != _m):
            levenshtein_distance += 1

        # Insertion & Deletion.
        if (_n is None) or (_m is None):
            levenshtein_distance += 1

    return levenshtein_distance

