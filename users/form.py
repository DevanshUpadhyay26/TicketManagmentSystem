from django.contrib.auth.forms import UserCreationForm

from .models import User

class RegisterCustomerForm(UserCreationForm):
    class Meta:  #attributes
        model=User
        fields = ['email','username']