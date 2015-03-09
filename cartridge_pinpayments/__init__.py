import locale
from pinpayments.models import PinTransaction


def payment_handler(request, order_form, order):
    amount = order.total
    order_id = str(order.id)
    data = order_form.cleaned_data

    # Get currency from locale
    lconv = locale.localeconv()
    currency = lconv.get('int_curr_symbol', 'AUD').strip()

    # Create PIN payments transaction
    transaction = PinTransaction()
    transaction.card_token = data['card_token']
    transaction.ip_address = "0.0.0.0" # IP address is not required
    transaction.amount = order.total
    transaction.currency = currency
    transaction.description = "Payment for #{0}".format(order_id)
    transaction.email_address = data['billing_detail_email']
    transaction.save()
    print "About to submit transaction:"
    print "card_token=", transaction.card_token
    print "amount=", transaction.amount
    print "currency=", transaction.currency
    print "description=",transaction.description
    print "email_address=", transaction.email_address


    result = transaction.process_transaction()
    if transaction.succeeded:
        print "PIN transaction success!"
        print "trans token = ", transaction.transaction_token
        print "fees = ", transaction.fees
        print "pin_response = ", transaction.pin_response
        print transaction.card_address1
        print transaction.card_address2
        print transaction.card_city
        print transaction.card_state
        print transaction.card_postcode
        print transaction.card_country
        print transaction.card_number
        print transaction.card_type

        return transaction.transaction_token
    else:
        import cartridge.shop.checkout
        raise cartridge.shop.checkout.CheckoutError("Credit Card error: " + result)
