from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse


class Mail:

    @staticmethod
    def get_absolute_url(url, company):
        if settings.DEBUG:
            return 'http://127.0.0.1:8080{}'.format(reverse(url, args=[company.slug]))

    @staticmethod
    def send_complete_order(company, order, user):
        subject = 'Tu pedido ha sido enviado'
        template = get_template('complete.html')
        url = 'public:orders_list'
        content = template.render({
            'user': user,
            'next_url': Mail.get_absolute_url(url, company)
            })

        message = EmailMultiAlternatives(subject,
                                         'Mensaje importante',
                                         settings.EMAIL_BACKEND,
                                         [user.email])

        message.attach_alternative(content, 'text/html')
        message.send()