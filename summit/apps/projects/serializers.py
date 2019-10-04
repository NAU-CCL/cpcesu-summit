from summit.libs.auth.models import UserGroup, UserProfile, Partner, FederalAgency
from summit.apps.projects.models import Location
from rest_framework import serializers


class FederalAgencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FederalAgency
        fields = ('pk', 'name')


class PartnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Partner
        fields = ('pk', 'name')


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('pk', 'name', 'abbrv')


class UserProfileSerializer(serializers.ModelSerializer):
    assigned_group_pk = serializers.ReadOnlyField(source='assigned_group.pk')
    assigned_group_name = serializers.ReadOnlyField(source='assigned_group.name')

    class Meta:
        model = UserProfile
        fields = ('pk', 'first_name', 'last_name', 'assigned_group_pk', 'assigned_group_name')
