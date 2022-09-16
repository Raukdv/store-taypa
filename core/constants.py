from django.utils.translation import ugettext_lazy as _


DEFAULT_WIDGET_WELCOME_TEXT = (
    'Would you recommend us to your friends and family?'
)
DEFAULT_WIDGET_POSITIVE_TEXT = (
    'Thank you for your help! Please click below to share your experience '
    'on one of these sites:'
)
DEFAULT_WIDGET_NEGATIVE_TEXT = 'Tells us a little bit about your experience.'
DEFAULT_WIDGET_SUBMITTED_TITLE = 'Thank you!'
DEFAULT_WIDGET_SUBMITTED_TEXT = 'Your feedback has been send successfully.'


DIRECTION_INBOUND = 'inbound'
DIRECTION_OUTBOUND = 'outbound'
DIRECTION_CHOICES = (
    (DIRECTION_INBOUND, _("Inbound")),
    (DIRECTION_OUTBOUND, _("Outbound"))
)


MESSAGE_EMAIL = 'email'
MESSAGE_SMS = 'sms'
MESSAGE_CHOICES = (
    (MESSAGE_EMAIL, _("Email")),
    (MESSAGE_SMS, _("SMS"))
)

REVIEW_SMS = (
    '{{ customer }}, were you satisfied with your experience with '
    '{{ company }}? Please take 30 seconds to leave us feedback here '
    '{{ url }} Text STOP to stop.'
)

ORDER_STATUS = (
    ('pending', _("Pending")),
    ('declined', _("Declined")),
    ('cancelled', _("Cancelled")),
    ('failed', _("Failed")),
    ('accepted', _("Accepted")),
    ('inprogress', _("Inprogress")),
    ('accepted', _("Accepted")),
    ('paid', _("Paid")),
    ('successful', _("Successful")),
    ('delivered', _("Delivered")),
)

TYPE_PAYMENT = [
    ('paypal', 'Paypal'),
    ('stripe', 'Stripe'),
    ('culqui','Culqui'),
]