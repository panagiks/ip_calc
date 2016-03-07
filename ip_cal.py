import sys
from math import floor, ceil

def main():
    #Stupid-proof ... er ... I mean input checking
    try:
        ip_range = sys.argv[1]
    except:
        print ("Syntax Error - Not enough arguments")
        print ("Correct syntax : ip/mask")
        print ("ex. p_scan.py 192.168.1.0/24")
        sys.exit()
            
    ip_split = ip_range.split('/')
    if (ip_split == ip_range):
        print ("Syntax Error")
        print ("Correct syntax : ip/mask")
        print ("ex. p_scan.py 192.168.1.0/24")
        sys.exit()
    
    network = ip_split[0]
    try:
        mask = int(ip_split[1])
        if (mask > 32):
            raise
    except:
        print("Network mask is not an Integer or is greater than 32")
        sys.exit()

    network_dotted = network.split('.')
    if (network_dotted == network or len(network_dotted) != 4 ):
        print("Wrong IP formating")
        sys.exit()

    i = 0
    try:
        for part in network_dotted:
            network_dotted[i] = int(part)
            if (network_dotted[i] > 255):
                raise
            network_dotted[i] = bin(network_dotted[i])
            network_dotted[i] = list(network_dotted[i][2:])
            i += 1
    except:
        print ("Wrond IP formating")

    network_base = []
    network_top = []
    for ip_part in network_dotted:
        for k in range(len(ip_part),8):
            ip_part[0:0] = ['0']
    for j in range(0,int(floor(mask/8))):
        network_base.append(network_dotted[j])
        network_top.append(network_dotted[j])
    if (mask%8 != 0):
        network_base.append(network_dotted[j+1][:(mask%8)] + ['0'] *(8-(mask%8)))
        network_top.append(network_dotted[j+1][:(mask%8)] + ['1'] *(8-(mask%8)))
    for j in range(int(ceil(mask/8)),4):
        network_base.append((['0']*8))
        network_top.append((['1']*8))
    network_base[3][7] = '1'
    network_top[3][7] = '0'

    ip_base_parts = []
    ip_top_parts = []
    for ip_block in network_base:
        ip_block[0:0] = ['0','b']
        ip_base_parts.append(''.join(ip_block))
    for j in range(0,4):
        ip_base_parts[j] = int(ip_base_parts[j],2)
    for ip_block in network_top:
        ip_top_parts.append(''.join(ip_block))
    for j in range(0,4):
        ip_top_parts[j] = int(ip_top_parts[j],2)

    hosts = (2**(32 - mask)) - 2

    print ("Network: "+str(ip_base_parts[0])+"."+str(ip_base_parts[1])+"."+
           str(ip_base_parts[2])+"."+str(ip_base_parts[3]-1)+"/"+str(mask))
    print ("Broadcast: "+str(ip_top_parts[0])+"."+str(ip_top_parts[1])+"."+
           str(ip_top_parts[2])+"."+str(ip_top_parts[3]+1))
    print ("MinHost: "+str(ip_base_parts[0])+"."+str(ip_base_parts[1])+"."+
           str(ip_base_parts[2])+"."+str(ip_base_parts[3]))
    print ("MaxHost: "+str(ip_top_parts[0])+"."+str(ip_top_parts[1])+"."+
           str(ip_top_parts[2])+"."+str(ip_top_parts[3]))
    print ("Total Hosts: "+str(hosts))

if __name__=="__main__":
    main()
