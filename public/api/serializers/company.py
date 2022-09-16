from rest_framework import serializers, reverse

from core.models import Company, Feedback, Link, Message


class LinkSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_name')
    slug = serializers.StringRelatedField(source='service.slug')
    icon = serializers.SerializerMethodField(method_name='get_icon')
    url = serializers.SerializerMethodField(method_name='get_url')

    class Meta:
        fields = ('name', 'slug', 'icon', 'url', 'order')
        model = Link

    def get_name(self, obj):
        return obj.name if obj.name else obj.service.name

    def get_icon(self, obj):
        if obj.icon:
            url = obj.icon.url
        elif obj.service.icon:
            url = obj.service.icon.url
        else:
            return None

        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url

    def get_url(self, obj):
        return reverse.reverse(
            'public:company_link',
            args=[obj.company.slug, obj.service.slug],
            request=self.context['request']
        )


class CompanySerializer(serializers.ModelSerializer):
    link_set = LinkSerializer(many=True)

    class Meta:
        exclude = (
            'id', 'parent_company', 'user', 'users', 'email',
            'phone', 'address', 'address_2', 'city', 'state', 'country',
            'sms_template'
        )
        model = Company


class CompanyFeedbackSerializer(serializers.ModelSerializer):
    detail = serializers.CharField(
        required=True
    )

    class Meta:
        fields = ('detail',)
        model = Feedback

    def get_message(self):
        try:
            mid = self.context['request'].session['message_id']
        except KeyError:
            return

        try:
            return Message.objects.get(id=mid)
        except (TypeError, Message.DoesNotExist):
            return

    def save(self, **kwargs):
        message = self.get_message()
        return super().save(
            customer=message.customer if message else None,
            **kwargs
        )