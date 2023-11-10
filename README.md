<!-- Introduction -->
# Introduction
This is a simple project to forwarding request to another server. This project is using [Django](https://www.djangoproject.com/) as the web framework and [Requests](https://requests.readthedocs.io/en/master/) as the HTTP library. Purpose of this project to help web developers to send their request to spesific Web service from another machine in same connection (Eg. LAN, Wifi, etc). Developer just need to add the URL of the Web service and the request will be forwarded to the Web service.

<!-- Table of Contents -->
# Table of Contents
- [Introduction](#introduction)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Notes](#notes)

<!-- Installation -->
# Installation
1. Clone this repository
```bash
git clone 
```
2. Install the requirements
```bash
pip install -r requirements.txt
```
3. Run the server
```bash
python manage.py runserver
```

<!-- Usage -->
# Usage
1. Open the browser and go to [Settings](http://127.0.0.1:8000/settings/)
2. Add the URL of the Web service that you want to forward the request to by clicking the button "Add Target Host"
3. Fill the form with the URL of the Web service that you want to forward the request to
4. Click the button "Add Target Host"
5. Go back to [Settings](http://127.0.0.1:8000/settings/), you will see the list of the URL that you have added
6. Check the URL make sure the URL is reachable by clicking the button "Check Connection"
7. If the URL is reachable, you can set the URL to be target host by clicking the button "Set Target Host"
8. Now you can send the request to the target host by using the URL [http://127.0.0.1:8000/](http://127.0.0.1:8000/). The request will be forwarded to the target host that you have set before. You can send all request method (GET, POST, PUT, DELETE, etc) to the URL to all avalable path but not for request with path prefix "/settings/".

<!-- Contributing -->
# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

<!-- License -->
# License

<!-- Notes -->
# Notes
## How to find the IP address of the machine
1. Open the terminal
2. Type the command below
```bash
ipconfig
```
[![ipconfig](/static/img/ipconfig.PNG)](/static/img/ipconfig.PNG)
3. Find the IPv4 Address of the machine on Wireless LAN adapter Wi-Fi
4. The IPv4 Address is the IP address of the machine
[![wifi-lan](/static/img/wifi-lan.PNG)](/static/img/wifi-lan.PNG)
5. Format for url to add target host is http://[IP address]:[port], you can find the port in the terminal when you run the server
[![django run server](/static/img/django-runserver.PNG)](/static/img/django-runserver.PNG)
[![next run dev](/static/img/next-run-dev.PNG)](/static/img/next-run-dev.PNG)
[![go-lang echo](/static/img/go-echo.PNG)](/static/img/go-echo.PNG)


