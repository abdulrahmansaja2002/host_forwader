import ipaddress
import os
import socket
from pprint import pprint
# import scapy.all as scapy


# taken from chatGPT
# def scan(ip, timeout=1):
#     arp_request = scapy.ARP(pdst=ip)
#     ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
#     arp_request_packet = ether/arp_request
#     answered_list, _ = scapy.srp(arp_request_packet, timeout=timeout, verbose=False)

#     devices = []
#     for element in answered_list:
#         device_ip = element[1].psrc
#         device_mac = element[1].hwsrc
#         try:
#             device_hostname = socket.gethostbyaddr(device_ip)[0]
#         except socket.herror:
#             device_hostname = "Unknown"
#         devices.append({"ip": device_ip, "mac": device_mac, "hostname": device_hostname})
#     return devices


def is_app_access(request):
    origin = request.META.get('HTTP_ORIGIN')
    server = request.build_absolute_uri("/")
    if origin is None:
        return True
    return origin == server

def get_gateway_and_subnet_mask(interface_key="Wireless LAN adapter WiFi"):
    script = 'ipconfig'
    lines = []
    for line in os.popen(script): lines.append(line)
    # get default gateway and subnet mask
    subnet_mask = None
    default_gateway = None
    for i in range(len(lines)):
        line = lines[i].strip()
        key = line.split(":")[0]
        if key.strip().startswith(interface_key) or interface_key in key:
            for j in range(i+1, len(lines)):
                line = lines[j].strip()
                key = line.split(":")[0]
                default_gateway_key = "Default Gateway"
                subnet_mask_key = "Subnet Mask"
                if key.strip().startswith(default_gateway_key):
                    default_gateway = line.split(":")[1].strip()
                elif key.strip().startswith(subnet_mask_key):
                    subnet_mask = line.split(":")[1].strip()
                if subnet_mask is not None and default_gateway is not None: break
            break

    return default_gateway, subnet_mask

def cidr_notation(ip, subnet_mask):
    network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)
    return str(network)

def get_local_ipv4_address():
    try:
        # Create a socket object and connect to an external server (e.g., Google DNS)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))

        # Get the local IPv4 address
        local_ip = s.getsockname()[0]

        # Close the socket
        s.close()

        return local_ip
    except socket.error:
        raise "Unable to retrieve the local IPv4 address"

def scan_lan_hosts(): 
#     lan_interface_key = "Wireless LAN adapter WiFi"
#     default_gateway, subnet_mask = get_gateway_and_subnet_mask(interface_key=lan_interface_key)
#     local_ip = get_local_ipv4_address()
#     cidr = cidr_notation(ip=local_ip, subnet_mask=subnet_mask)
#     return scan(ip=cidr)
    pass

def get_all_hosts():
    lines = []
    for line in os.popen('arp -a'): lines.append(line)
    # hostname = socket.gethostname()
    ip_addr = get_local_ipv4_address()
    ip_neighbors = []
    interface_key = "Interface"
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith(interface_key) and \
            line.split()[1] == ip_addr:
            for j in range(i+1, len(lines)):
                line = lines[j].strip()
                if len(line) == 0: break
                if line.startswith("Internet"):
                    continue
                ip = line.split()[0]
                print(ip)
                # if type == "dynamic": ip_neighbors.append(ip)
                ip_neighbors.append(ip)

            break
    key = "Wireless LAN adapter WiFi"
    default_gateway, subnet_mask = get_gateway_and_subnet_mask(interface_key=key)
    
    host_neighbors = {}
    for ip in list(filter(
        lambda host: validate_ip_in_subnet(host, default_gateway, subnet_mask),  
        ip_neighbors
    )):
        try: host_neighbors[ip] = socket.gethostbyaddr(ip)[0]
        except: 
            print(f"Host for Ip Adderess {ip} wasn't found")
            host_neighbors[ip] = "Unknown"
        finally:
            pass
    return host_neighbors
            



def validate_ip_in_subnet(ip_str, gateway_str, subnet_mask_str):
    try:
        ip = ipaddress.IPv4Address(ip_str)
        gateway = ipaddress.IPv4Address(gateway_str)
        subnet = ipaddress.IPv4Network(f"{gateway_str}/{subnet_mask_str}", strict=False)
        print(ip_str)
        return ip in subnet
    except ipaddress.AddressValueError:
        return False

def clean_headers(headers):
    # clean django headers
    # remove headers that are only from django request headers
    # and not from the original request
    # https://stackoverflow.com/questions/4823468/
    pass




    