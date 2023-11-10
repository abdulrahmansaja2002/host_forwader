import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .helper import get_all_hosts, is_app_access, scan_lan_hosts
import requests

target_hosts = []
curr_target_host = None
forward_headers = True
forward_root_path = False
full_forward = False

def concat_path(path1, path2):
    return path1.rstrip("/") + "/" + path2.lstrip("/")
def host_connectivity_check(host):
    print("host_connectivity_check url: " + host.url)
    try:
        requests.get(host.url, timeout=10)
        return True
    except requests.exceptions.ConnectionError:
        return False
class HostIP:
    def __init__(self, name, ip) -> None:
        self.name = name
        self.ip = ip
class Host:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.is_reachable = host_connectivity_check(self)

    def __str__(self):
        return self.name

    def save(self):
        with open("hosts.txt", "a") as f:
            f.write(f"{self.name},{self.url}\n")

    @staticmethod
    def inithost(target_hosts=target_hosts):
        global target_host
        try:
            with open("hosts.txt", "r") as f:
                for line in f.readlines():
                    name, url= line.strip().split(",")
                    host = Host(name, url)
                    target_hosts.append(host)
        except FileNotFoundError:
            print("hosts.txt not found")
        
        global curr_target_host
        try:
            with open("curr_target_host.txt", "r") as f:
                curr_target_host_name = f.read()
                curr_target_host = next((host for host in target_hosts if host.name == curr_target_host_name), None)
        except FileNotFoundError:
            print("curr_target_host.txt not found")
        
def init():
    Host.inithost()

init()


def index(request):
    context = {
        "target_hosts": target_hosts,
        "curr_target_host": curr_target_host,
        "forward_headers" : forward_headers,
        "forward_root_path": forward_root_path,
        "full_forward": full_forward,
    }
    return render(request, "index.html", context)

def add_target_host(request):
    if request.method == "POST":
        name = request.POST.get("name").strip()
        url = request.POST.get("url").strip()
        save_host = request.POST.get("save_host")
        if not name or not url:
            context = {
                "error": "Please fill out all fields."
            }
            return render(request, "add_target_host.html", context)
        if not url.startswith("http"):
            url = "http://" + url
        # if not url.endswith("/"):
        #     url += "/"
        # if not con_check_path.startswith("/"):
        #     con_check_path = "/" + con_check_path
        # if not con_check_path.endswith("/"):
        #     con_check_path += "/"
        host = Host(name, url)
        if not host_connectivity_check(host):
            context = {
                "error": "Host is not reachable."
            }
            return render(request, "add_target_host.html", context)
        target_hosts.append(host)
        if save_host:
            host.save()
        context = {
            "target_hosts": target_hosts,
            "curr_target_host": curr_target_host
        }
        return redirect("index")
    else:
        context = {
            "target_hosts": json.dumps(target_hosts, default=vars),
            # "hosts" : [HostIP(hostname, ip) for (ip, hostname) in get_all_hosts().items()]
            # "hosts": [HostIP(device["hostname"], device["ip"]) for device in scan_lan_hosts()], 
        }
        return render(request, "add_target_host.html", context)

@csrf_exempt
def check_conection(request):
    url = request.GET.get("url")
    print("check_conection url: " + url)
    host = next((host for host in target_hosts if host.url == url), None)
    if host:
        host.is_reachable = host_connectivity_check(host)
    
    return redirect("index")


def forward(request, path):
    global curr_target_host
    method = request.method
    headers = dict(request.headers)
    body = request.body
    url = concat_path(curr_target_host.url, path)
    print("[HOST FORWARDER] forward request to", url, "with method", method )
    if forward_headers:
        response = requests.request(method, url, headers=headers, data=body)
    else:
        response = requests.request(method, url, data=body)
    print("[HOST FORWARDER] get  response from", url, "with status", response.status_code)
    return response


@csrf_exempt
def host_forwader(request, path=""):
    if not forward_root_path and (path == "" or path == "/"):
        return redirect("index")
    if is_app_access(request) and not full_forward:
        return redirect("index")
    if curr_target_host is None:
        return render(request, "error.html")
    print("host_forwader request: " + str(request))
    response = forward(request, path)
    print("host_forwader response: " + str(response))
    content_type = response.headers.get("Content-Type", "")
    return HttpResponse(response.content, status=response.status_code, content_type=content_type)

@csrf_exempt
def set_target_host(request):
    global curr_target_host
    global target_hosts
    if request.method == "POST":
        # target_host_name = request.POST.get("target_host_name")
        # curr_target_host = next((host for host in target_hosts if host.name == target_host_name), None)
        target_host_url = request.POST.get("target_host_url")
        curr_target_host = next((host for host in target_hosts if host.url == target_host_url), None)
        # save curr_target_host to file
        with open("curr_target_host.txt", "w") as f:
            f.write(curr_target_host.url)
        return redirect("index")
    
@csrf_exempt
def scan_all_lan_host(request):
    # script bellow just fetch all host that have connected with this machine before
    # host_neighbors = get_all_hosts()
    # print("scan_all_lan_host: " + str(host_neighbors))
    # return JsonResponse(json.dumps(
    #     [HostIP(hostname, ip) for (ip, hostname) in host_neighbors.items()], 
    #         default=vars
    #         ), safe=False
    #     )
    
    # script bellow fetch all host in same lan 
    # but, you need to carefully using this, 
    # scanning all host in same network maybe will beat
    # an ethic in hacking 
    devices = scan_lan_hosts()
    print("scan_all_lan_host: " + str(devices))
    return JsonResponse(json.dumps(
        [HostIP(device["hostname"], device["ip"]) for device in devices], 
            default=vars
            ), safe=False
        )
    
@csrf_exempt
def set_forward_headers(request):
    global forward_headers
    if request.method == "PUT":
        print(request.body.decode("utf-8"))
        forward_headers =json.loads(request.body.decode("utf-8"))['forward_headers']
        return HttpResponse("Success", status=200)
@csrf_exempt
def set_forward_root_path(request):
    global forward_root_path
    if request.method == "PUT":
        forward_root_path = json.loads(request.body.decode("utf-8"))["forward_root_path"]
        return HttpResponse("Success", status=200)
@csrf_exempt
def set_full_forward(request):
    global full_forward
    if request.method == "PUT":
        full_forward = json.loads(request.body.decode("utf-8"))["full_forward"]
        return HttpResponse("Success", status=200)