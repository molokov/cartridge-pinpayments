import locale

def payment_handler(request, order_form, order):
    from pinpayments.models import PinTransaction, PinError
    
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
    try:
        transaction.save()
    except PinError:
        # Error thrown from django-pinpayments, this means something is bad.
        #
        # To debug this, print the contents of the PinError message here!
        # Modify the above to: except PinError as e:
        # and add: print str(e)
        #
        import cartridge.shop.checkout
        raise cartridge.shop.checkout.CheckoutError(
            "Credit Card Processing error. Please check credit card details and try again.")

    result = transaction.process_transaction()
    if transaction.succeeded:
        return transaction.transaction_token
    else:
        import cartridge.shop.checkout
        raise cartridge.shop.checkout.CheckoutError("Credit Card error: " + result)
