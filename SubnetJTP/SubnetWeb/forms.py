import json
from django import forms

class subnetForm(forms.Form):
    NETWORK_CLASS_CHOICES = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('ANY', 'No Class (Only Subnet bits)'),
    ]

    SUBNET_MASK_CHOICES = [
    (32, '255.255.255.255 /32'),
    (31, '255.255.255.254 /31'),
    (30, '255.255.255.252 /30'),
    (29, '255.255.255.248 /29'),
    (28, '255.255.255.240 /28'),
    (27, '255.255.255.224 /27'),
    (26, '255.255.255.192 /26'),
    (25, '255.255.255.128 /25'),
    (24, '255.255.255.0 /24'),
    (23, '255.255.254.0 /23'),
    (22, '255.255.252.0 /22'),
    (21, '255.255.248.0 /21'),
    (20, '255.255.240.0 /20'),
    (19, '255.255.224.0 /19'),
    (18, '255.255.192.0 /18'),
    (17, '255.255.128.0 /17'),
    (16, '255.255.0.0 /16'),
    (15, '255.254.0.0 /15'),
    (14, '255.252.0.0 /14'),
    (13, '255.248.0.0 /13'),
    (12, '255.240.0.0 /12'),
    (11, '255.224.0.0 /11'),
    (10, '255.192.0.0 /10'),
    (9, '255.128.0.0 /9'),
    (8, '255.0.0.0 /8'),
    (7, '254.0.0.0 /7'),
    (6, '252.0.0.0 /6'),
    (5, '248.0.0.0 /5'),
    (4, '240.0.0.0 /4'),
    (3, '224.0.0.0 /3'),
    (2, '192.0.0.0 /2'),
    (1, '128.0.0.0 /1'),
    ]

    SUBNET_MASK = {
    '32' : [255, 255, 255, 255],
    '31' : [255, 255, 255, 254],
    '30' : [255, 255, 255, 252],
    '29' : [255, 255, 255, 248],
    '28' : [255, 255, 255, 240],
    '27' : [255, 255, 255, 224],
    '26' : [255, 255, 255, 192],
    '25' : [255, 255, 255, 128],
    '24' : [255, 255, 255, 0],
    '23' : [255, 255, 254, 0],
    '22' : [255, 255, 252, 0],
    '21' : [255, 255, 248, 0],
    '20' : [255, 255, 240, 0],
    '19' : [255, 255, 224, 0],
    '18' : [255, 255, 192, 0],
    '17' : [255, 255, 128, 0],
    '16' : [255, 255, 0, 0],
    '15' : [255, 254, 0, 0],
    '14' : [255, 252, 0, 0],
    '13' : [255, 248, 0, 0],
    '12' : [255, 240, 0, 0],
    '11' : [255, 224, 0, 0],
    '10' : [255, 192, 0, 0],
    '9' : [255, 128, 0, 0],
    '8' : [255, 0, 0, 0],
    '7' : [254, 0, 0, 0],
    '6' : [252, 0, 0, 0],
    '5' : [248, 0, 0, 0],
    '4' : [240, 0, 0, 0],
    '3' : [224, 0, 0, 0],
    '2' : [192, 0, 0, 0],
    '1' : [128, 0, 0, 0],
    }

    class_subnet_dict = {
    }

    class_subnet_dict['ANY'] = []
    class_subnet_dict['A'] = []
    class_subnet_dict['B'] = []
    class_subnet_dict['C'] = []

    for num in reversed(range(1, 33)):
        class_subnet_dict['ANY'].append(num)
        if num >= 8 :
            class_subnet_dict['A'].append(num)
        if num >= 16 :
            class_subnet_dict['B'].append(num)
        if num >= 24 :
            class_subnet_dict['C'].append(num)

    network_class = forms.ChoiceField(choices = NETWORK_CLASS_CHOICES
    , required = True, label = 'Network Class')
    subnet_mask = forms.ChoiceField(choices = SUBNET_MASK_CHOICES
    , required = True, label = 'Subnet Mask')
    ip4_input = forms.GenericIPAddressField(protocol = 'IPv4'
    , required = True, label = 'IPv4 Address')

    classes = json.dumps(NETWORK_CLASS_CHOICES)
    subnets = json.dumps(class_subnet_dict)
    subnets_text = json.dumps(SUBNET_MASK_CHOICES)
