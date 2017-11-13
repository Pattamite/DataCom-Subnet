from django import forms

class subnetForm(forms.Form):
    NETWORK_CLASS_CHOICES = (
    ('Any', 'Any'),
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    )

    SUBNET_MASK_CHOICES = (
    (32 , '255.255.255.255 /32'),
    (31 , '255.255.255.254 /31'),
    )

    network_class = forms.ChoiceField(choices = NETWORK_CLASS_CHOICES
    , required = True, label = 'Network Class')
    subnet_mask = forms.ChoiceField(choices = SUBNET_MASK_CHOICES
    , required = True, label = 'Subnet Mask')
    ip4_input = forms.GenericIPAddressField(protocol = 'IPv4'
    , required = True, label = 'IPv4 Address')
