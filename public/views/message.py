from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import Http404
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import DetailView, View
from twilio.twiml.messaging_response import MessagingResponse

from core.models import Message


class MessageRedirectView(DetailView):
    model = Message

    def get_object(self):
        uidb64 = self.kwargs.get('uidb64')

        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            message = self.model.objects.get(pk=uid)
        except (
            TypeError, ValueError, OverflowError, self.model.DoesNotExist,
            ValidationError
        ):
            self.session_clean()
            raise Http404
        return message

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.session_set(self.object.id)

        url = reverse_lazy(
            'public:company_detail', args=[self.object.company.slug]
        )

        return HttpResponseRedirect(url)

    def session_clean(self):
        try:
            del self.request.session['message_id']
        except KeyError:
            pass

    def session_set(self, mid):
        self.request.session['message_id'] = mid

class MessageSMSView(View):
    def post(self, request, *args, **kwargs):
        twilio_account = request.POST.get('AccountSid')
        if twilio_account != settings.TWILIO_ACCOUNT_SID:
            raise Http404

        Message.objects.create_or_update_from_api(data=request.POST)

        resp = MessagingResponse()
        return HttpResponse(resp.to_xml(), content_type='application/xml')
