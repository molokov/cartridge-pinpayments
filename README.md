# cartridge-pinpayments

PIN payments integration for mezzanine/cartridge

See http://pin.net.au for PIN Payments home page.

## Requirements:

* Mezzanine 3.1.10 or later
* Cartridge 0.9.5 or later
* django-pinpayments ( https://github.com/RossP/django-pinpayments/ )


## Installation:
Working in your project's virtual environment:

	pip install git+https://github.com/molokov/cartridge-pinpayments.git

Add the following settings to your settings file:

	INSTALLED_APPS = (

  		"cartridge_pinpayments",
  		"cartridge.shop",
  		# ...

  		"pinpayments",
	)

	SHOP_HANDLER_PAYMENT = "cartridge_pinpayments.payment_handler"

	# set these variables up as per django-pinpayments instructions 
	PIN_ENVIRONMENTS = { ... }
	PIN_DEFAULT_ENVIRONMENT = 'test'

In your urls.py, ensure the PinOrderForm class is used in place of OrderForm:

	from cartridge_pinpayments.forms import PinOrderForm

	# ...

	urlpatterns += patterns('',

    	# Use our special OrderForm class
    	url("^shop/checkout/$", "cartridge.shop.views.checkout_steps", 
        	name="shop_checkout", kwargs=dict(form_class=PinOrderForm)),

    	# Cartridge URLs.
    	("^shop/", include("cartridge.shop.urls")),

    	# ...
    )


## Migrate Existing Database

Required by django-pinpayments. Ensure south is installed first!

	python manage.py migrate pinpayments


## Templates

**IMPORTANT**

*templates/shop/checkout.html* has been overridden from the version in cartridge 0.9.5 to define some extra ids and names on form elements that are used by the javascript in the included pin_header.html template. 

These are:

<pre>
	&lt;form method="post" class="checkout-form col-md-8" <b>id="checkout-form"</b> &gt;
	
	&lt;input type="submit" class="btn btn-lg btn-primary pull-right" <b>name="next"</b> value="{% trans "Next" %}"&gt;
</pre>

Thus if you are planning to override checkout.html yourself, be sure to copy these modifications across to your version of the template.


