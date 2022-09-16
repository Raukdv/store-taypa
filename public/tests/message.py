from django import test
from django.conf import settings
from django.urls import reverse
from django.test import Client

from core.models import Company, Phone, User

class MessageViewTestCase(test.TestCase):
    def setUp(self):
        user = User.objects.create(
            email='test@test.com', first_name='Test', last_name='Case'
        )
        self.company = Company.objects.create(
            name='Test Company', user=user,
        )
        self.phone = Phone.objects.create(
            phone='+18183214321', api_id='Test1234', company=self.company
        )
        self.customer = self.company.customer_set.create(
            first_name='Test',
            last_name='Case',
            phone='+18181231234'
        )

    def test_stop_message(self):
        url = reverse('public:message_sms')
        c = Client()
        c.post(url, {
            'AccountSid': settings.TWILIO_ACCOUNT_SID,
            'From': self.customer.phone,
            'To': self.phone.phone,
            'Body': 'stop',
            'MessageSid': 'Test1234'
        })

        customer = self.company.customer_set.get()

        self.assertFalse(customer.send_sms)
        self.assertEqual(self.company.message_set.count(), 2)
