# cartridge-pinpayments
PIN payments integration for mezzanine/cartridge

See http://pin.net.au for PIN Payments home page

Requirements:
  Mezzanine 3.1.10 
  Cartridge 0.9.5
  django-pinpayments (https://github.com/RossP/django-pinpayments/)


To install:

PIN_ENVIRONMENTS and PIN_DEFAULT_ENVIRONMENT set up as per django-pinpayments in settings.py

INSTALLED_APPS = (

  "cartridge_pinpayments",
  "cartridge.shop",
  # ...

  "pinpayments",
)

SHOP_HANDLER_PAYMENT = "cartridge_pinpayments.payment_handler"
SHOP_CHECKOUT_FORM_CLASS = "cartridge_pinpayments.forms.PinOrderForm" # FIXME


Run 
python manage.py migrate pinpayments


TO BE COMPLETED


NOTE:
templates/shop/checkout.html has been overridden to define some extra ids and names on form elements that are used by the pin_header.html template. Thus if you are planning to override checkout.html yourself, be sure to copy these modifications across to your version of the template.

