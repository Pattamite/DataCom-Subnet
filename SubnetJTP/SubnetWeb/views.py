from django.shortcuts import render
from .forms import subnetForm
import json

def index(request):
    form = subnetForm(request.POST or None)
    confirm_message = None
    info_table = None

    if form.is_valid():
        network_class = form.cleaned_data['network_class']
        subnet_num = int(form.cleaned_data['subnet_mask'])
        ip4_input = form.cleaned_data['ip4_input']
        subnet = form.SUBNET_MASK[str(subnet_num)]
        wildcard_num = 32 - subnet_num

        wildcard = []
        for i in range(0, 4):
            wildcard.append(255 - subnet[i])

        ip4 = []
        for string in ip4_input.split('.') :
            ip4.append(int(string))

        net_addr = []
        for i in range(0, 4):
            net_addr.append(subnet[i] & ip4[i])

        broadcast_addr = net_addr[:]
        for i in range(0, 4):
            broadcast_addr[i] |=  wildcard[i]


        info_table = []
        info_table.append(['IP Address', makeIpString(ip4)])
        info_table.append(['Network Address', makeIpString(net_addr)])
        info_table.append(['Usable Host IP Range', usableHostRange(net_addr, broadcast_addr, subnet_num)])
        info_table.append(['Broadcast Address', makeIpString(broadcast_addr)])
        info_table.append(['Total Number of Hosts', str(2 ** wildcard_num)])
        info_table.append(['Number of Usable Hosts', str(max([(2 ** wildcard_num) - 2, 0]))])
        info_table.append(['Subnet Mask', makeIpString(subnet)])
        info_table.append(['Wildcard Mask', makeIpString(wildcard)])
        info_table.append(['Binary Subnet Mask', makeBinaryIpString(subnet)])
        info_table.append(['Binary Wildcard Mask', makeBinaryIpString(wildcard)])

    context = {
    'form' : form,
    'confirm_message' : confirm_message,
    'info_table' : info_table,
    }
    template = 'index.html'
    return render(request, template, context)

def makeIpString(value):
    ans = ''
    if(len(value) > 0):
        ans = str(value[0])
        if(len(value) > 1):
            for i in range(1, len(value)):
                ans += ('.' + str(value[i]))
    return ans

def usableHostRange(net_addr, broadcast_addr, subnet_num):
    if subnet_num >= 31 :
        return 'None'
    else :
        min_addr = net_addr[:]
        min_addr[3] += 1

        max_addr = broadcast_addr[:]
        max_addr[3] -= 1

        return makeIpString(min_addr) + " - " + makeIpString(max_addr)

def makeBinaryIpString(value):
    ans = ''
    if(len(value) > 0):
        ans = '{0:08b}'.format(value[0])
        if(len(value) > 1):
            for i in range(1, len(value)):
                ans += ('.' + '{0:08b}'.format(value[i]))
    return ans
