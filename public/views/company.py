from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView

from core.models import Company
class CompanyDetailView(DetailView):
   model = Company
   template_name = 'public/company/detail.html'

   def get(self, request, *args, **kwargs):
        if 'last_feedback' in self.request.session:
            last_feedback = datetime.strptime(self.request.session['last_feedback'], '%Y-%m-%d %H:%M:%S')
            if datetime.now() < last_feedback + timedelta(minutes=30):
                return HttpResponseRedirect(reverse_lazy('public:index'))
            else:
                self.request.session['last_feedback'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
                return super().get(request, *args, **kwargs)
        else:
            self.request.session['last_feedback'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            return super().get(request, *args, **kwargs)


class CompanyMerchantDetailView(DetailView):
    model = Company
    template_name = 'public/company/merchant_detail.html'

class CompanyLinkView(DetailView):
    model = Company

    def get_link(self):
        try:
            service = self.kwargs['service']
            return self.object.link_set.get(
                service__slug=service
            )
        except (KeyError, TypeError, ObjectDoesNotExist):
            raise Http404

    def get_message(self):
        try:
            mid = self.request.session['message_id']
        except KeyError:
            return

        try:
            return self.object.message_set.get(id=mid)
        except ObjectDoesNotExist:
            return

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        link = self.get_link()
        message = self.get_message()

        self.object.feedback_set.create(
            customer=message.customer if message else None,
            service=link.service
        )
        return HttpResponseRedirect(link.url)
