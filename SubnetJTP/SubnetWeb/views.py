from django.shortcuts import render
from .forms import subnetForm

def index(request):
    form = subnetForm(request.POST or None)
    confirm_message = None

    if form.is_valid():
        network_class = form.cleaned_data['network_class']
        subnet_mask = form.cleaned_data['subnet_mask']
        ip4_input = form.cleaned_data['ip4_input']
        confirm_message = str(network_class) + ' ' + str(subnet_mask) + ' ' + str(ip4_input)

    context = {'form' : form,
    'confirm_message' : confirm_message,
    }
    template = 'index_test.html'
    return render(request, template, context)
