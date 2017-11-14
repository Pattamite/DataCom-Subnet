from django.shortcuts import render
from .forms import subnetForm
import json

def index(request):
    form = subnetForm(request.POST or None)
    info_table = None
    network_table_header = None
    network_table = None
    network_table_limit = 100

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

        #---------------------------------------------------------------------------------------------------#
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
        info_table.append(['IP Class', ipClass(ip4)])
        info_table.append(['IP Class (For this calculation)', ipClassForCal(network_class)])
        info_table.append(['CIDR Notation', '/' + str(subnet_num)])
        info_table.append(['IP Type', ipType(ip4)])
        info_table.append(['Short', makeIpString(ip4) + ' /' + str(subnet_num)])
        info_table.append(['Binary ID', makeBinaryValue(ip4)])
        info_table.append(['Integer ID', str(makeIntValue(ip4))])
        info_table.append(['Hex ID', makeHexValue(ip4)])
        #---------------------------------------------------------------------------------------------------#
        network_table = []
        entry_count = 0
        start_value = 0
        end_value = 0x100000000
        step_value = makeIntValue(wildcard) + 1

        if network_class == 'A':
            start_value = makeIntValue(ip4) & 0xff000000
            end_value = start_value + 0x01000000
        elif network_class == 'B':
            start_value = makeIntValue(ip4) & 0xffff0000
            end_value = start_value + 0x00010000
        elif network_class == 'C':
            start_value = makeIntValue(ip4) & 0xffffff00
            end_value = start_value + 0x00000100

        current_value = start_value
        #print(makeIpString(ip4) + " / " + str(makeIntValue(ip4)) + " / " + intToIp(start_value) + " / " + intToIp(end_value) + " / " + intToIp(step_value))

        while entry_count < network_table_limit and current_value < end_value :
            network_addr = intToIp(current_value)
            usable_range = ""
            broad_addr = ""

            if subnet_num == 32 :
                usable_range = "None"
                broad_addr = network_addr[:]
            elif subnet_num == 31 :
                usable_range = "None"
                broad_addr = intToIp(current_value + 1)
            else :
                usable_range = intToIp(current_value + 1) + " - " + intToIp(current_value + step_value - 2)
                broad_addr = intToIp(current_value + step_value - 1)

            network_table.append([network_addr, usable_range, broad_addr])
            current_value += step_value
            entry_count += 1

            if current_value >= end_value :
                network_table_header = "All Possible '/" + str(subnet_num) + "' Networks"
            else :
                network_table_header = "First " + str(network_table_limit) +" Possible '/" + str(subnet_num) + "' Networks"
        #---------------------------------------------------------------------------------------------------#


    context = {
    'form' : form,
    'info_table' : info_table,
    'network_table_header' : network_table_header,
    'network_table' : network_table,
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

def makeIntValue(value):
    ans = 0
    if(len(value) > 0):
        for i in range(0, len(value)):
            ans *= 256
            ans += value[i]
    return ans

def makeBinaryValue(value):
    intValue = makeIntValue(value)
    return '{0:#034b}'.format(intValue)

def makeHexValue(value):
    intValue = makeIntValue(value)
    return '{0:#010x}'.format(intValue)

def ipClass(value):
    if value[0] <= 127 :
        return 'A'
    elif value[0] <= 191 :
        return 'B'
    elif value[0] <= 223 :
        return 'C'
    elif value[0] <= 239 :
        return 'D'
    else:
        return 'E'

def ipClassForCal(value):
    if value == 'ANY' :
        return 'None'
    else :
        return value

def ipType(value):
    if value[0] == 10 :
        return 'Private'
    elif value[0] == 172 and value[1] >= 16 and value[1] <= 31 :
        return 'Private'
    elif value[0] == 192 and value[1] == 168 :
        return 'Private'
    else :
        return 'Public'

def intToIp(value):
    ans = []
    ans.append((value & 0xff000000) >> 24)
    ans.append((value & 0x00ff0000) >> 16)
    ans.append((value & 0x0000ff00) >> 8)
    ans.append(value & 0x000000ff)
    return makeIpString(ans)
