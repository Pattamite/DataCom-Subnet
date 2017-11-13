from django.shortcuts import render
from .forms import subnetForm
import json

def index(request):
    form = subnetForm(request.POST or None)
    confirm_message = None
    info_table = None

    if form.is_valid():
        network_class = form.cleaned_data['network_class']
        subnet_mask = form.cleaned_data['subnet_mask']
        ip4_input = form.cleaned_data['ip4_input']

        subnet = form.SUBNET_MASK[subnet_mask]
        ip4 = []
        for string in ip4_input.split('.') :
            ip4.append(int(string))

        net_addr = []
        for i in range(0, 4):
            net_addr.append(subnet[i] & ip4[i])

        info_table = []
        info_table.append(['IP Address', ip4_input])
        info_table.append(['Network Address', str(net_addr[0]) + '.' + str(net_addr[1]) + '.' + str(net_addr[2]) + '.' + str(net_addr[3])])

    context = {
    'form' : form,
    'confirm_message' : confirm_message,
    'info_table' : info_table,
    }
    template = 'index.html'
    return render(request, template, context)
