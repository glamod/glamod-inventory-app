from django import forms


from .models import Inventory
from .models import Contact
from .models import InventoryHistory
from .models import LinkInvHist

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML


class UploadContactForm( forms.ModelForm ):
    file = forms.FileField()
    def __init__(self, *args, **kwargs):
        super( UploadContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'POST'
        self.helper.form_action = '/invapp/contact/upload/'
        self.helper.add_input(Submit('submit', 'Submit'))
    class Meta:
        model = Contact
        fields = []


class ContactForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'POST'
        self.helper.form_action = '/invapp/contact/add/'
        self.helper.add_input(Submit('submit', 'Submit'))
    
    
    class Meta:
        model = Contact
        exclude = []

class InventoryForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(InventoryForm, self).__init__(*args, **kwargs)
        # default helper
        self.helper = FormHelper()
        self.helper.form_id = 'id_inventory_form'
        self.helper.form_method = 'POST'
        self.helper.form_tag = True
        self.helper.layout = Layout(
            # Metadata identification information
            Div(
                Div( HTML('<h3>Identification</h3>'), css_class='col-md-12'),
                Div('source_id','product_name','product_id','product_code','scope', css_class='col-md-6'),
                Div('product_version','product_level','product_status','record_status', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div( 'contact_metadata', 'contact_role_metadata', css_class = 'col-md-12'),
                css_class='row'
            ),
            Div(
                Div(HTML('<h3>Coverage</h3>'), css_class='col-md-12'),
                Div(
                    Div( 'spatial_domain', css_class='col-md-4'),
                    Div( 'geometry_type', css_class='col-md-4'),
                    Div( 'crs', css_class='col-md-4'),
                    css_class='row'
                ),
                Div(
                    Div('start_date', 'end_date', css_class='col-md-4'),
                    Div('bbox_min_latitude', 'bbox_min_longitude', css_class='col-md-4'),
                    Div('bbox_max_latitude', 'bbox_max_longitude', css_class='col-md-4'),
                    css_class='row'
                ),
                Div(
                    Div('station_count', css_class='col-md-6'),
                    Div('mean_years_present', css_class='col-md-6'),
                    css_class='row'
                )
            ),
            Div(
                Div(HTML('<h3>Dataset description</h3>'), css_class='col-md-12'),
                Div( 'description', css_class = 'col-md-12'  ),
                #Div( 'contact_data','contact_role_data',css_class='col-md-3'),
                css_class='row'
            ),
            Div(
                Div('product_citation','product_references', css_class='col-md-12'),
                css_class='row'
            ),
            Div(
                Div('data_policy', css_class='col-md-6'),
                Div('data_policy_document', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div( HTML('<h3>Data centre information</h3>'), css_class='col-md-12'),
                Div( 'data_centre','data_centre_url', css_class='col-md-6'),
                Div( 'contact_data', 'contact_role_data', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div( 'product_uri', css_class='col-md-12'),
                Div( 'source_format','source_format_version', css_class='col-md-6'),
                Div( 'source_file', 'source_file_checksum', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div( HTML('<h3>Additional information</h3>'), css_class='col-md-12'),
                Div( 'comments',css_class='col-md-12'),
                css_class='row'
            ),
            Div(
                Div( 'update_frequency', css_class='col-md-6'),
                Div( 'timestamp', css_class='col-md-6'),
                css_class='row'
            ),
        )
        self.helper.form_action = '/invapp/inventory/add/'
        self.helper.add_input(Submit('submit', 'Submit'))
        # helper without submit
        # ---------------------
        self.helperNoSubmit = FormHelper()
        self.helperNoSubmit.form_id = 'id_inventory_form'
        self.helperNoSubmit.form_method = 'POST'
        self.helperNoSubmit.form_tag = False
        self.helperNoSubmit.layout = Layout(
            # Metadata identification information
            Div(
                Div( HTML('<h3>Identification</h3>'), css_class='col-md-12'),
                Div('source_id','product_name','product_id','product_code','scope', css_class='col-md-6'),
                Div('product_version','product_level','product_status','record_status', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div( 'contact_metadata', 'contact_role_metadata', css_class = 'col-md-12'),
                css_class='row'
            ),
            Div(
                Div(HTML('<h3>Coverage</h3>'), css_class='col-md-12'),
                Div(
                    Div( 'spatial_domain', css_class='col-md-4'),
                    Div( 'geometry_type', css_class='col-md-4'),
                    Div( 'crs', css_class='col-md-4'),
                    css_class='row'
                ),
                Div(
                    Div('start_date', 'end_date', css_class='col-md-4'),
                    Div('bbox_min_latitude', 'bbox_min_longitude', css_class='col-md-4'),
                    Div('bbox_max_latitude', 'bbox_max_longitude', css_class='col-md-4'),
                    css_class='row'
                ),
                Div(
                    Div('station_count', css_class='col-md-6'),
                    Div('mean_years_present', css_class='col-md-6'),
                    css_class='row'
                )
            ),
            Div(
                Div(HTML('<h3>Dataset description</h3>'), css_class='col-md-12'),
                Div( 'description', css_class = 'col-md-12'  ),
                #Div( 'contact_data','contact_role_data',css_class='col-md-3'),
                css_class='row'
            ),
            Div(
                Div('product_citation','product_references', css_class='col-md-12'),
                css_class='row'
            ),
            Div(
                Div('data_policy', css_class='col-md-6'),
                Div('data_policy_document', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div( HTML('<h3>Data centre information</h3>'), css_class='col-md-12'),
                Div( 'data_centre','data_centre_url', css_class='col-md-6'),
                Div( 'contact_data', 'contact_role_data', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div( 'product_uri', css_class='col-md-12'),
                Div( 'source_format','source_format_version', css_class='col-md-6'),
                Div( 'source_file', 'source_file_checksum', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div( HTML('<h3>Additional information</h3>'), css_class='col-md-12'),
                Div( 'comments',css_class='col-md-12'),
                css_class='row'
            ),
            Div(
                Div( 'update_frequency', css_class='col-md-6'),
                Div( 'timestamp', css_class='col-md-6'),
                css_class='row'
            ),
        )

    
    class Meta:
        model = Inventory
        exclude = []

class UploadInventoryForm( forms.ModelForm ):
    file = forms.FileField()
    def __init__(self, *args, **kwargs):
        super( UploadInventoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'POST'
        self.helper.form_action = '/invapp/inventory/upload/'
        self.helper.add_input(Submit('submit', 'Submit'))
    class Meta:
        model = Inventory
        fields = []

class InventoryHistoryForm( forms.ModelForm ):
    def __init__(self, *args, **kwargs):
        super(InventoryHistoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'POST'
        self.helper.form_tag = False
        #self.helper.form_action = '/invapp/contact/add/'
        #self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = InventoryHistory
        exclude = ['date','action']

class GeminiValidate( forms.Form ):
    input = forms.CharField(widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(GeminiValidate, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'POST'
        self.helper.form_tag = False

    class Meta:
        exclude = ''
