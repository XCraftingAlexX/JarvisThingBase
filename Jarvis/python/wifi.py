import subprocess
import re
import socket
import json

def get_device_name(ip_address):
    try:
        device_name = socket.gethostbyaddr(ip_address)[0]
        return device_name
    except:
        pass
    return None

def get_connected_devices(network_name, interface, ssid, password):
    print(f"Scanning network {network_name}...")
    devices = []
    cmd_output = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode("utf-8")
    profile_names = re.findall("All User Profile     : (.*)\r", cmd_output)

    for profile_name in profile_names:
        if ssid not in profile_name:
            continue

        cmd_output = subprocess.check_output(["netsh", "wlan", "show", "profile", profile_name, "key=clear"]).decode("utf-8")
        match = re.search("Key Content            : (.*)\r", cmd_output)

        if not match or match[1].strip() != password:
            continue

        cmd_output = subprocess.check_output(["netsh", "wlan", "show", "interface"]).decode("utf-8")
        match = re.search("Name                   : (.*)\r", cmd_output)

        if not match or match[1].strip() != interface:
            continue

        cmd_output = subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=bssid"]).decode("utf-8")
        lines = cmd_output.split("\n")

        for line in lines:
            if ssid not in line:
                continue

            if network_name not in line:  # Check if the network name is in the line
                continue

            bssid = line.split()[1]
            cmd_output = subprocess.check_output(["arp", "-a"]).decode("utf-8")
            lines = cmd_output.split("\n")

            for line in lines:
                if bssid not in line:
                    continue

                match = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)

                if not match:
                    continue

                ip_address = match.group(1)
                device_name = get_device_name(ip_address)
                print(f"Found device {device_name} ({ip_address}) on network {network_name}")
                devices.append((ip_address, device_name))

    return devices

with open("networks.json") as f:
    data = json.load(f)

password = data["password"]
networks = data["networks"]

for network in networks:
    network_name = network["name"]
    interface = network["interface"]
    ssid = network["ssid"]
    print(f"Connected devices for {network_name}:")
    connected_devices = get_connected_devices(network_name, interface, ssid, password)

    for device in connected_devices:
        print(device[0], device[1])

    print()  # Add an empty line to separate the networks