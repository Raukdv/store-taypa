from . import stripe

def create_customer(user):
    customer = stripe.Customer.create(
        description=user.description,
        email=user.email,
        name='{} {}'.format(user.first_name, user.last_name)
    )

    return customer
