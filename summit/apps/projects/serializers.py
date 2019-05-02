from summit.libs.auth.models import UserGroup, UserProfile, Partner, FederalAgency
from rest_framework import serializers


class FederalAgencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FederalAgency
        fields = ('pk', 'name')
