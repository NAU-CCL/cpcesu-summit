from summit.libs.auth.models import UserGroup, UserProfile, Partner, FederalAgency
from rest_framework import serializers


class FederalAgencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FederalAgency
        fields = ('pk', 'name')


class PartnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Partner
        fields = ('pk', 'name')
