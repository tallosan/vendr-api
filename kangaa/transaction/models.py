from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from kproperty.models import Property


'''   Trasaction model. '''
class Transaction(models.Model):

    # The buyer, seller, and the property this transaction is on.
    buyer       = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='buyer')
    seller      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='seller')
    kproperty   = models.ForeignKey(Property, related_name='property')

    # Stage 1: Offer Stage.
    b_offer     = models.IntegerField()
    s_offer     = models.IntegerField()

    # Stage 2: Negotiation Stage.
    b_contract  = models.FileField(blank=True)
    s_contract  = models.FileField(blank=True)

    # Stage 3: Closing Stage.

    # The transaciton stage we're in.
    STAGES      = (
                    (0, 'OFFER_STAGE'),
                    (1, 'NEGOTIATION_STAGE'),
                    (2, 'CLOSING_STAGE')
    )
    
    stage       = models.IntegerField(choices=STAGES, default=0)

    #TODO: Mutex.

    ''' Move the transaction stage up, assuming we aren't already in the final stage. '''
    def next_stage(self):

        # Final stage.
        if self.stage == 2:
            raise Http404('error: transaction is at final stage already.')

        self.stage += 1

    ''' String representation for Transaction models. '''
    def __str__(self):

        return 'buyer ' + str(self.buyer) + \
                ' and seller ' + str(self.seller) + \
                ' on property ' + str(self.kproperty)

