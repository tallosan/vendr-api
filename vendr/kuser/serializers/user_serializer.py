from django.contrib.auth import get_user_model

from rest_framework import serializers

from kproperty.models import Property
from kuser.models import KUser, Profile
from kuser.models import TransactionNotification, OfferNotification#, ContractNotification
from transaction.models import Transaction
from transaction.serializers import TransactionSerializer

User = get_user_model()


'''   Serializer for Profile models. '''
class ProfileSerializer(serializers.ModelSerializer):

    prof_pic = serializers.ReadOnlyField(source='prof_pic.name')
    
    class Meta:
        model   = Profile
        fields  = ('first_name', 'last_name',
                   'location',
                   'prof_pic',
                   'bio')


'''   Serializer for User models. '''
class UserSerializer(serializers.ModelSerializer):

    profile    = ProfileSerializer(required=False)
    #TODO: Send password in plaintext.
    properties = serializers.PrimaryKeyRelatedField(many=True, required=False,
                    queryset=Property.objects.select_subclasses())
    
    # Custom notification queryset.
    notification_qs  = []
    #notification_qs += OfferNotification.objects.all()
    #notification_qs += ContractNotification.objects.all()
    
    notifications = serializers.PrimaryKeyRelatedField(many=True, required=False,
                        queryset=notification_qs)
    
    class Meta:
        model   = KUser
        fields  = ('id',
                   'email', 'password',
                   'profile',
                   'properties',
                   'favourites',
                   'notifications',
                   'join_date')
    
    ''' Handles the creation of a Kangaa User object.
        Args:
            validated_data: The request data we create the new model from.
    '''
    def create(self, validated_data):

        email       = validated_data.pop('email')
        password    = validated_data.pop('password')
        
        kuser       = User.objects.create_user(email=email, password=password)
        
        # Create the user profile if any data is given.
        try:
            prof = validated_data.pop('profile')
            if self.context: validated_data.update(self.get_file_data())
            for key in prof.keys():
                setattr(kuser.profile, key, prof.pop(key))
            
            kuser.profile.save()

        except KeyError: pass
        
        return kuser

    ''' Update all target fields.
        Args:
            instance: The actual user object to be updated.
            validated_data: Fields to be updated, and their updates.
    '''
    def update(self, instance, validated_data):
        
        # Files are passed through the context.
        if self.context:
            validated_data.update(self.get_file_data())

        for term in validated_data.keys():
            target_data = validated_data.pop(term)
            target = getattr(instance, term)
            
            # One-to-one relation update.
            if issubclass(target_data.__class__, dict):
                for field in target_data.keys():
                    setattr(target, field, target_data[field])
                
                target.save()
            
            # Handle password updates.
            elif term == 'password':
                instance.set_password(target_data)
 
            # Regular field update.
            else:
                setattr(instance, term, target_data)
        
            instance.save()

        return instance

    ''' Get file objects from the context. N.B. -- only the Profile object
        contains a file (image) field.
    '''
    def get_file_data(self):

        file_data = { 'profile': {} }
        for file_key in self.context.keys():
            file_data['profile'][file_key] = self.context[file_key]

        return file_data

    ''' User representation. Returns the transaction data, with the incoming
        and outgoing transactions separated.
        Args:
            instance: The Transaction model being serialized.
    '''
    def to_representation(self, instance):

        kuser = super(UserSerializer, self).to_representation(instance)
        kuser['transactions'] = self.format_transactions(instance)
        
        return kuser

    def format_transactions(self, instance):

        user_id  = instance.pk
        incoming = Transaction.objects.filter(seller=user_id).values_list('pk', flat=True)
        outgoing = Transaction.objects.filter(buyer=user_id).values_list('pk', flat=True)

        transactions = { "incoming": incoming, "outgoing": outgoing }

        return transactions

