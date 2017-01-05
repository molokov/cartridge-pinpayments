# cartridge-pinpayments

PIN payments integration for mezzanine/cartridge

See http://pin.net.au for PIN Payments home page.

## Requirements:

* Mezzanine 4.2.0 or later
* Cartridge 0.12.0 or later
* django-pinpayments 1.0.11 or later ( https://github.com/RossP/django-pinpayments/ )
* Django 1.10 or later

## Installation:
Working in your project's virtual environment:

	pip install -e git+https://github.com/molokov/cartridge-pinpayments.git#egg=cartridge_pinpayments

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

	from cartridge.shop.views import checkout_steps
	from cartridge_pinpayments.forms import PinOrderForm

	# ...

	urlpatterns += [

    	# Use our special OrderForm class
    	url("^shop/checkout/$", checkout_steps, name="shop_checkout", kwargs=dict(form_class=PinOrderForm)),

    	# Cartridge URLs.
    	url("^shop/", include("cartridge.shop.urls")),

    	# ...
    ]


## Migrate Existing Database

The django-pinpayments app needs to create two tables in the database, so be sure to run:

	python manage.py migrate pinpayments


## Templates

**IMPORTANT**

*templates/shop/checkout.html* has been overridden from the version in cartridge 0.12.0 to define some extra ids and names on form elements that are used by the javascript in the included pin_header.html template.

These are:

<pre>
	&lt;form method="post" class="checkout-form col-md-8" <b>id="checkout-form"</b> &gt;

	&lt;input type="submit" class="btn btn-lg btn-primary pull-right" <b>name="next"</b> value="{% trans "Next" %}"&gt;
</pre>

Thus if you are planning to override checkout.html yourself, be sure to copy these modifications across to your version of the template.


