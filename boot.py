import machine
from network import WLAN
wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    if net.ssid == 'TP-LINK_4379':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'TP-LINK_4379'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        print(wlan.ifconfig())
        break
    if net.ssid == 'Butch_ASUS':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, '4085297774'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        print(wlan.ifconfig())
        break
