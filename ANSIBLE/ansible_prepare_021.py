#!/usr/bin/python

import os
import yaml
import csv
import re
import ipaddress

# Calculates the GW IP for given subnet. n is the number of the gateway in the subnet. Usually 1.
#So as example we will have gateway 192.168.12.129 for the subnet 192.168.128.0/255.255.255.128
#In case if n<0 it will get gateway from the end of the network. As example n=-1 will give us latest IP in the network before broadcast
# In case of n=0 returns subnet address
def calc_gateway(subnet,mask,n):
   ip=ipaddress.ip_address(subnet)
   m=ipaddress.ip_address(mask)
   network=ipaddress.ip_network(str(ipaddress.ip_address(int(ip) & int(m)))+"/"+str(m))
   n=int(n)
   
   if(n>=0):
      return str(ipaddress.ip_address(int(network.network_address)+n))
   else:
      return str(ipaddress.ip_address(int(network.broadcast_address)+n))

def calc_prefix_len(subnet,mask,n):
   return ipaddress.IPv4Network("0.0.0.0/"+mask).prefixlen
   
  

class ipdir():
   c=0
   dirdict={}
   interfaces={}
   routes={}
   #csvre=re.compile('^(.+)\.csv$')
   csvre=re.compile('^(.+)\\.csv$')
   def __init__(self,d,dt={},starthost="all"):
      if(self.c==0):
         self.c+=1
         self.dirdict["all"]=dt
         self.dirdict["all"]["vars"]={"ansible_user":"user1","ansible_password":"Test1@3456789","ansible_port":22,"ansible_become_pass":"Test1@3456789","ansible_become_method":"sudo",
                                      "domain": "agentpodd-platform.tech.pd36.digitalgov.gtn",
                                      "hostsfile":[
                                               {"host": "ipa-master-02.coresvc-infra.common.pd34.udp.gtn","ipaddr": "10.246.0.141"},
                                               {"host": "ipa-master-01.coresvc-infra.common.pd34.udp.gtn","ipaddr": "10.246.0.140"}
                                      ],
                                      "route_files":{},"ntp_servers":["10.246.0.140","10.246.0.141"],
                                      "dns_servers": ["10.246.0.140","10.246.0.141"],
                                      "timezone":"/usr/share/zoneinfo/Europe/Moscow",
                                      "ansible_ssh_common_args": '-o ProxyJump=d.kulida@10.246.8.22',
                                      "ansible_ssh_private_key_file": "/home/dkulida/.ssh/id_rsa"}
         self.routes={"mgmt":
                         {
                         #   "10.0.0.0/255.0.0.0":{"ipaddr":"10.0.0.0","netmask":"255.0.0.0"}
                         },
                     }

      self.init_recur(d,dt,starthost,{})
      # Generate route-files condig
      for rt in self.interfaces:
         if rt in self.routes.keys():
            for net_with_mask in self.interfaces[rt]:
                for host in self.interfaces[rt][net_with_mask]:
                   c=0
                   for route_net_with_mask in self.routes[rt]:
                      if net_with_mask==route_net_with_mask:
                         continue

                      val=["ADDRESS"+str(c)+"="+self.routes[rt][route_net_with_mask]["ipaddr"]]
                      val.append("NETMASK"+str(c)+"="+self.routes[rt][route_net_with_mask]["netmask"]) 
                      val.append("GATEWAY"+str(c)+"="+self.interfaces[rt][net_with_mask][host]["gateway"]) 
                      val.append("") 
                      if host not in self.dirdict["all"]["vars"]["route_files"].keys():
                         self.dirdict["all"]["vars"]["route_files"].update({host:{"route-"+self.interfaces[rt][net_with_mask][host]["interface"]:val}})
                      elif "route-"+self.interfaces[rt][net_with_mask][host]["interface"] not in self.dirdict["all"]["vars"]["route_files"][host].keys(): 
                         self.dirdict["all"]["vars"]["route_files"][host].update({"route-"+self.interfaces[rt][net_with_mask][host]["interface"]:val})
                      else:
                         self.dirdict["all"]["vars"]["route_files"][host]["route-"+self.interfaces[rt][net_with_mask][host]["interface"]]+=val
                      c+=1

   # Go over IP directories and fill variables
   def init_recur(self,d,dt={},starthost="all",cfg={}):
      if(os.path.exists(d+"ip")):
         with open(d+"ip") as ipf:
            ip=ipf.readline()
            ip=ip.strip()
            if("hosts" not in dt.keys()):
               dt["hosts"]={starthost:{"ansible_host":ip}}
            elif(starthost not in dt["hosts"].keys()):
               dt["hosts"][starthost]={"ansible_host":ip}
            else:
               dt["hosts"][starthost].update({"ansible_host":ip})

      if(os.path.exists(d+"access.txt")):
         with open(d+"access.txt") as accessfile:
            c=0
            access=accessfile.readlines()
            for l in access:
               l=l.strip()
               if(c==0):
                   acc={"ansible_user":l}
               elif(c==1):
                   acc["ansible_password"]=l
               elif(c==2):
                   acc["ansible_become_pass"]=l
               elif(c==3):
                   acc["ansible_port"]=l
               c+=1
#         print("AAA",dt[i])
         if("hosts" in dt.keys()):
             dt["hosts"][starthost].update(acc) 
         else:
             if("vars" not in dt.keys()):
                 dt["vars"]=acc
             else:
                 dt["vars"].update(acc)

#      if "hosts" in dt.keys() and starthost in dt["hosts"] and "config" not in dt["hosts"][starthost].keys():
#         dt["hosts"][starthost]["config"]=cfg

      l=os.listdir(d)
      for i in l:
          if(res:=self.csvre.match(i)):
             with open(d+i) as csvfile:
                csvr=csv.reader(csvfile,dialect="unix") 
                csvdict={"name": res.group(1)}
                for raw in csvr:
                   k=raw.pop(0)
                   if(len(raw)==1):
                     raw=raw[0]
                   csvdict[k]=raw
                      
             #print(csvdict)
             #Fill routes attributes
             route_attrs=("route_target","route_gateway")
             route_dict={}
             for a in route_attrs:
               if(a in csvdict.keys()):
                  route_dict[a]=csvdict.pop(a)

             if(route_dict):
                 #route_dict["gateway"]=calc_gateway(csvdict["ipaddr"],csvdict["netmask"],route_dict.pop("route_gateway"))
                 route_dict["netmask"]=csvdict["netmask"]
                 route_dict["ipaddr"]=calc_gateway(csvdict["ipaddr"],csvdict["netmask"],0)
                 #route_dict["interface"]=csvdict["name"]

                 interface_dict={starthost:{}}
                 interface_dict[starthost]["gateway"]=calc_gateway(csvdict["ipaddr"],csvdict["netmask"],route_dict.pop("route_gateway"))
                 if("gateway" in interface_dict[starthost]):
                       csvdict["route_gateway"]=interface_dict[starthost]["gateway"]
                 #interface_dict[starthost]["gateway"]=route_dict["gateway"]
                 #interface_dict[starthost]["netmask"]=csvdict["netmask"]
                 #interface_dict[starthost]["ipaddr"]=calc_gateway(csvdict["ipaddr"],csvdict["netmask"],0)
                 interface_dict[starthost]["interface"]=csvdict["name"]
                 interface_dict[starthost]["route_target"]=route_dict["route_target"] 
          
                 
                 # Reordering routes and interfaces variables
                 #dt["hosts"][starthost]["config"].append({"route": route_dict.copy()})
                 net_with_mask=route_dict["ipaddr"]+"/"+route_dict["netmask"]                 
                 if(route_dict["route_target"] not in self.routes.keys()):
                    self.routes[route_dict.pop("route_target")]={net_with_mask:route_dict.copy()}
                 elif(net_with_mask not in self.routes[route_dict["route_target"]].keys()):
                    self.routes[route_dict.pop("route_target")].update({net_with_mask:route_dict.copy()})
                 else:
                    self.routes[route_dict.pop("route_target")][net_with_mask].update(route_dict.copy())
                
                 if(interface_dict[starthost]["route_target"] not in self.interfaces.keys()):
                    self.interfaces[interface_dict[starthost].pop("route_target")]={net_with_mask:interface_dict.copy()}
                 elif(net_with_mask not in self.interfaces[interface_dict[starthost]["route_target"]].keys()):
                    self.interfaces[interface_dict[starthost].pop("route_target")].update({net_with_mask:interface_dict.copy()})
                 else:
                    self.interfaces[interface_dict[starthost].pop("route_target")][net_with_mask].update(interface_dict.copy())
 

             # Calculating gateway if it is set in form of integer:
             try:
                gw=int(csvdict["gateway"])
                csvdict["gateway"]=calc_gateway(csvdict["ipaddr"],csvdict["netmask"],gw)
             except Exception:
                pass
            
             if "ipaddr" in csvdict and "netmask" in csvdict:
                csvdict["prefixlen"]=calc_prefix_len(csvdict["ipaddr"],csvdict["netmask"],0)

             if("hosts" in csvdict.keys() and csvdict["hosts"]=="yes"):
                csvdict.pop("hosts")
                self.dirdict["all"]["vars"]["hostsfile"].append({"host": f"{starthost}.{self.dirdict['all']['vars']['domain']}","ipaddr": csvdict['ipaddr']})

             #print(csvdict)
             typ=csvdict.pop("type")
             if typ in cfg.keys():
                for n in range(len(cfg[typ])):
                   if cfg[typ][n]["name"]==csvdict["name"]:
                     cfg[typ]=[csvdict.copy()]
                     break
                else:
                   cfg[typ].append(csvdict.copy())
             else:
                cfg[typ]=[csvdict.copy()]

      for typ in cfg.keys():
        if "hosts" in dt.keys() and starthost in dt["hosts"]:
           if "config" in dt["hosts"][starthost].keys():
              if typ in dt["hosts"][starthost]["config"].keys():
                 dt["hosts"][starthost]["config"][typ].append(cfg[typ])
              else:
                 dt["hosts"][starthost]["config"][typ]=cfg[typ]
           else:
              dt["hosts"][starthost]["config"]={typ:cfg[typ]}


      l=os.listdir(d)
      for i in l:
          if (os.path.isdir(d+i)):
             nextdir=d+i+"/"
             if(not os.path.exists(nextdir+"ip")):
                if("children" not in dt.keys()):
                   dt["children"]={}
                if(i not in dt["children"].keys()):
                   dt["children"][i]={}
                self.init_recur(nextdir,dt["children"][i],i,cfg.copy())
             else:
                self.init_recur(nextdir,dt,i,cfg.copy())
               
#      print(self.routes,self.interfaces)

   def __repr__(self):
     return yaml.dump(self.dirdict,None) 

ipd=ipdir("./")

print(ipd)


