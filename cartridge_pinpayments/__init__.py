from pinpayments.models import PinTransaction

def payment_handler(request, order_form, order):
    amount = order.total
    order_id = str(order.id)
    data = order_form.cleaned_data

    # Create PIN payments transaction
    transaction = PinTransaction()
    transaction.card_token = data['card_token']
    transaction.ip_address = data['ip_address']
    transaction.amount = order.total
    transaction.currency = 'AUD' # FIXME
    transaction.description = "Payment for #{0}".format(order_id)
    transaction.email_address = data['billing_detail_email]']
    transaction.save()

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
