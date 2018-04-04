import re

def get_name(data):
    name = []
    x = data[0]
    #x = 'Atul  K.Singh  '
    for c in x:
        if c.isalnum() or c==' ' or c=='.':
            name.append(c)
    name = ''.join(name)
    name = re.sub('\s{2,}', ' ', name)
    if name.endswith(' '):
        name=name.rstrip()
    return(name)

def get_address(data):
    address = []
    x = data[1:4]
    x = ' '.join(x)
    x = re.sub('\s{2,}', ' ', x)
    x = x.split()
    for c in x:
        if not(c.isdigit() and len(c)==6):
            address.append(c)
        else:
            address.append(c)
            break
    address = ' '.join(address)
    return(address)

def get_aadhaar(data):
    aadhaar=[]
    x=data[4]
    for c in x:
        if c.isdigit():
            aadhaar.append(c)
    aadhaar=''.join(aadhaar)
    return(aadhaar)

