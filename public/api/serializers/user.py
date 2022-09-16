from rest_framework import serializers, reverse
from core.models import User

class UserCompaniesSerializer(serializers.ModelSerializer):
    companies = serializers.SerializerMethodField('get_companies')
    
    class Meta:
        fields = ('companies',)
        model = User

    def get_companies(self, user):
        companies = {company['name']: company for company in user.companies.values()}
        return companies