from django import forms


from .models import Inventory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class InventoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(InventoryForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = '/invapp/inventory/add/'

        self.helper.add_input(Submit('submit', 'Submit'))


    class Meta:
        model = Inventory
        exclude = []
