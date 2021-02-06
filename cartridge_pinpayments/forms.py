from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.forms.utils import flatatt

import cartridge.shop.forms as shop_forms
from cartridge.shop import checkout


class NoNameTextInput(forms.TextInput):

    """ A widget for a text input that omits the 'name' attribute, which
    should prevent them from being submitted to the server.
    """

    def render(self, name, value, attrs=None, renderer=None):
        # See django.forms.widgets.py,
        # class Input, method render()
        if value is None:
            value = ''
        if attrs is None:
            attrs = {}
        attrs['autocomplete'] = 'off'
        final_attrs = self.build_attrs(attrs, {"type": self.input_type})
        # Remove the name from the attributes, as this is what this
        # widget is for!
        if 'name' in final_attrs:
            final_attrs.pop('name')
        # Never add the value to the HTML rendering, this field
        # will be encrypted and should remain blank if the form is
        # re-loaded!
        final_attrs['value'] = ''
        return format_html('<input{0} />', flatatt(final_attrs))


class NoNamePasswordInput(NoNameTextInput):
    input_type = 'password'


class PinOrderForm(shop_forms.OrderForm):
    """
    The following changes are made to the cartridge order form:
    - Credit Card number and CCV fields are rendered using the
    NoNameTextInput and NoNamePasswordInput widgets so that the
    data is not submitted to the server. Javascript in the page header
    processes these fields (and others) to create a token, which is then
    stored in the hidden form element.
    - Card token form elements are set by the Javascript.
    - Errors from Pin.js are set by the Javascript, and will be handled
      as django errors.

    See https://pin.net.au/docs/guides/payment-forms
    """
    card_token = forms.CharField(label=_("Card Token"), required=False)
    pinjs_errors = forms.CharField(label=_("Pin.js Errors"), required=False)

    def __init__(self, request, step, data=None, initial=None, errors=None):
        super(PinOrderForm, self).__init__(
            request, step, data, initial, errors)
        self.fields["card_token"].widget = forms.HiddenInput()
        self.fields["pinjs_errors"].widget = forms.HiddenInput()
        self.fields["pinjs_errors"].value = ""

        # The card number and CCV fields should have the 'name' attribute removed
        # and the fields made non-required, as they will be handled by the javascript
        # and remain blank when hitting the server.
        if not isinstance(self.fields["card_number"].widget, forms.HiddenInput):
            # Card number is not hidden
            self.fields["card_number"].widget = NoNameTextInput()
            self.fields["card_number"].required = False
        if not isinstance(self.fields["card_ccv"].widget, forms.HiddenInput):
            # Card CCV is not hidden
            self.fields["card_ccv"].widget = NoNamePasswordInput()
            self.fields["card_ccv"].required = False

    def clean(self):
        """
        See if pin.js returned any errors
        See if the card_token was created successfully.
        """
        import json
        pinjs_errors = self.cleaned_data["pinjs_errors"]
        if pinjs_errors:
            errors = json.loads(pinjs_errors)
            for e in errors:
                try:
                    param = e['param']
                    msg = e['message']
                except (KeyError, TypeError):
                    continue

                # Formatting here is done so that errors from Pin Payments API
                # are converted to more Django-like errors for "blank" fields,
                # or given directly otherwise.
                # The errors are also associated with the appropriate form
                # field
                if param == "cvc":
                    self._errors["card_ccv"] = self.error_class(
                        [_("This field is required.")])
                elif param == "number":
                    if "can't be blank" in msg:
                        self._errors["card_number"] = self.error_class(
                            [_("This field is required.")])
                    else:
                        self._errors["card_number"] = self.error_class([msg])
                elif param == "name":
                    if "can't be blank" in msg:
                        self._errors["card_name"] = self.error_class(
                            [_("This field is required.")])
                    else:
                        self._errors["card_name"] = self.error_class([msg])
                else:
                    raise forms.ValidationError(msg)
        elif self.cleaned_data["step"] >= checkout.CHECKOUT_STEP_PAYMENT and not self.cleaned_data["card_token"]:
            # Card token is blank, but pinjs_errors is also blank - this may occur
            # if e.g. javascript is disabled or JS from pin.net.au was not loaded
            # Although we have warnings in place (see pin_headers.html and payment.html)
            # We should catch this here rather than later.
            raise forms.ValidationError(
                "Credit Card number/CCV could not be processed. Please try again.")

        # Cartridge expects card_number and card_ccv to be non-blank
        # when we are using a credit card.
        self.cleaned_data["card_number"] = "CARDNUMBER"
        self.cleaned_data["card_ccv"] = "CCV"

        return super(PinOrderForm, self).clean()
