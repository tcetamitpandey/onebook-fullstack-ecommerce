from django.forms import ModelForm

from ecom_app.models import User_Model

class Registration_form(ModelForm):
    class Meta:
        model=User_Model
        fields="__all__"
        # fields=["username",'password']