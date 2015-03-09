from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.forms.util import flatatt

import cartridge.shop.forms as shop_forms


class NoNameTextInput(forms.TextInput):

    """ A widget for a text input that omits the 'name' attribute, which
    should prevent them from being submitted to the server.
    """

    def render(self, name, value, attrs=None):
        # See django.forms.widgets.py,
        # class Input, method render()
        if value is None:
            value = ''
        if attrs is None:
            attrs = {}
        attrs['autocomplete'] = 'off'
        final_attrs = self.build_attrs(attrs, type=self.input_type)
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
    - Card token and IP address form elements are set by the Javascript.

    See https://pin.net.au/docs/guides/payment-forms
    """
    card_token = forms.CharField(label=_("Card Token"), required=False)
    ip_address = forms.CharField(label=_("IP Address"), required=False)

    def __init__(self, request, step, data=None, initial=None, errors=None):
        super(PinOrderForm, self).__init__(request, step, data, initial, errors)

        self.fields["card_token"].widget = forms.HiddenInput()
        self.fields["ip_address"].widget = forms.HiddenInput()

        if not isinstance(self.fields["card_number"].widget, forms.HiddenInput):
            # Card number is not hidden
            self.fields["card_number"].widget = NoNameTextInput()
        if not isinstance(self.fields["card_ccv"].widget, forms.HiddenInput):
            # Card CCV is not hidden
            self.fields["card_ccv"].widget = NoNamePasswordInput()

    


