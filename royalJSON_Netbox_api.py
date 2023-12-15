import requests
import json

url = "http://10.90.0.135/api/dcim/devices"
site_url = "http://10.90.0.135/api/dcim/sites/"

payload = {}
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Token 57598e341d295290ca85914663a7897adf7a4051',
  '57598e341d295290ca85914663a7897adf7a4051': 'JWT '
}

device_response = requests.request("GET", url, headers=headers, data=payload)
site_response = requests.request("GET", site_url, headers=headers, data=payload)

device_apidata = (device_response.json())
site_apidata = (site_response.json())

# Print json data using loop
# for key in apidata:{
#     print(key,":", apidata[key])
# }
    
device_results = device_apidata['results']
site_results = site_apidata['results']
sites = []

for device in device_results:
    theid = device.get('id', 'no id')
    device_name = device.get('name', 'No Name')
    primary_ip = device.get('primary_ip', {}).get('address', 'No IP Address')
    site_name = device.get('site', {}).get('name', 'No Site Name')

   # print(f"Device Name: {device_name}")
   # print(f"Primary IP: {primary_ip}")
    #print(f"Site Name: {site_name}")
    #print("-" * 30)

for theSite in site_results:
    site = theSite.get('name', 'no site')
    sites.append(site)

#print(sites)

class Folder:
    def __init__(self, name, connections):
        self.name = name
        self.connections = connections

    #
    # This format assumes everything is a terminal session. You can adjust the code to add additional types
    #
    def to_dict(self):
        objects = [{"Type": "TerminalConnection",
                    "TerminalConnectionType": "SSH",
                    "Name": connection["name"],
                    "ComputerName": connection["computer_name"]}
                   for connection in self.connections]
        return {"Type": "Folder", "Name": self.name, "Objects": objects}
    
class Connections:
    def __init__(self):
        self.folders = []

    def add_folder(self, name, connections):
        folder = Folder(name, connections)
        self.folders.append(folder)

    def to_dict(self):
        objects = [folder.to_dict() for folder in self.folders]
        return {"Objects": objects}

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
    

connections = Connections()

for site in sites:
    connection_objects = []
    #devices = [item["site"]['name'] for item in device_results]
        #devices = nb.dcim.devices.filter(site_id=site.id)
    for device in device_results:
        if device.get('site', {}).get('name', 'No Site Name') == site:
        #if device.device_role.id not in interesting_role_ids:
            #   break
            ipadd = device.get('primary_ip', {}).get('address', 'No IP Address')
            connection_objects.append(
                {
                "name": device.get('name', 'No Name'),
                "computer_name": ipadd[:-3]
                }
                )
    connections.add_folder(str(site), connection_objects)

print(connections.to_json())
