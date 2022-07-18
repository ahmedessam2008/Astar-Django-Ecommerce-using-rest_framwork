# from django import forms
# from django_countries.fields import CountryField

# class CheckoutForm(forms.Form):
#   name = forms.CharField()
#   adress1 = forms.CharField()
#   adress2 = forms.CharField(required=False)
#   zipcode = forms.CharField()
#   country = CountryField(blank_label='(select country)')
#   phone = forms.IntegerField()
#   email = forms.EmailField(required=False)
#   terms_conditions = forms.BooleanField(widget=forms.CheckboxInput())
#   save_information = forms.BooleanField(widget=forms.CheckboxInput())
#   subscribe = forms.BooleanField(widget=forms.CheckboxInput())
#   pyment = forms.BooleanField(widget=forms.RadioSelect())