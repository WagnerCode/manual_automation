#!/bin/python

import requests
import os
import time
import getopt
import sys
import json

cloud_endpoints={
    "iam": "https://iam.api.cloud.ru/api/v1/",
    "compute": "https://compute.api.cloud.ru/api/v1/",
    "baremetal": "https://baremetal.api.cloud.ru/v2/",
    "mk8s": "https://mk8s.api.cloud.ru/v2/",
    "vpc": "https://vpc.api.cloud.ru/v1/",
    "dns": "https://dns.api.cloud.ru/v1/",
    "kafka": "https://kafka.api.cloud.ru/v1/",
    "redis": "https://redis.api.cloud.ru/v1/",
    "magic-router": "https://magic-router.api.cloud.ru/v1/",
    "organization": "https://organization.api.cloud.ru/v3/",
    "nlb": "https://nlb.api.cloud.ru/v2/",
    "s3": "https://s3.cloud.ru/",
    "ar": "https://ar.api.cloud.ru/v1",
    "containers": "https://containers.api.cloud.ru/v2",
    "postgresql": "https://postgresql.api.cloud.ru/v1"
}

cloud_key_id=os.getenv("TF_VAR_CLOUDRU_KEY_ID")
cloud_secret=os.getenv("TF_VAR_CLOUDRU_SECRET")
project_id=os.getenv("CLOUDRU_PROJECT_ID")

token=dict()

def help():
   print("""Usage:
   check_entity.py [-h] -a|--api <api> -q|--query <query> [-m|--match <match parameter> -v|--value <match value>]
      -h|--help: Print this message and exit
      -a|--api:  Select API to use. May be iam, compute, baremetal, mk8s, vpc, kafka, redis, magic-router, organization, nlb, s3, ar, containers
      -q|--query: Query, as example "vms" to get list of VMs - based on the Cloud.Ru documentation
      -m|--match: Match parameter. As example name or id
      -v|--value: Value for match parameter
""")

def checkOpts() -> dict:
   ret=dict()
   arg_list=sys.argv[1:]
   short_opts = "ha:q:m:v:"
   long_opts = ["help", "api=","query=","match=","value="]
   
   try:
      opts, arg = getopt.getopt(arg_list,short_opts, long_opts)

   except getopt.GetoptError as err:
      print(str(err))
      exit(1)

   for o,v in opts:
     if o in ("-h","--help"):
       help()
       exit(0)
     if o in ("-a","--api"):
        ret["url"]=v
        continue
     if o in ("-q","--query"):
        ret["query"]=v
        continue
     if o in ("-m","--match"):
        if "match" in ret.keys():
           ret["match"]+=[v]
        else:
           ret["match"]=[v]
        continue
     if o in ("-v","--value"):
        if "value" in ret:
           ret["value"]+=[v]
        else:
           ret["value"]=[v]

#   print(ret)
   return ret 


def main():
   params=checkOpts()

   data=query(params["url"],params["query"],0,100)
   
   #print("LEN:",len(data))
   if "match" in params:
     m=match_res(data,params["match"],params["value"])
     print(json.dumps(m))
   else:
     print(json.dumps(data))   

   exit(0)

def get_token():
   global token
   
   if token and "access_token" in token and check_token():
      return

   uri="auth/token"
   payload=f"""{{
       "keyId": "{cloud_key_id}",
       "secret": "{cloud_secret}"
}}
"""
   headers={'Content-Type': 'application/json'}

   r = requests.post(cloud_endpoints["iam"]+uri, data=payload, headers=headers) 
   if r.status_code != 200:
      print("Error getting token\n")
      exit(1)

   else:
      data=r.json()

   data["time"]=time.time()
   token=data


def check_token() -> bool:
  
  leftTime=token["time"]+token["expires_in"]-time.time()

#  print("Token leftTime =", leftTime)
  if(leftTime<30):
    return False
  else:
    return True


def query(url,qr,offset,limit) -> list:
   get_token()
   res=list()
   headers={'Content-Type': 'application/json', "Authorization": f"Bearer {token["access_token"]}"}
#   print(url)

#   print(cloud_endpoints[url]+qr+f"?project_id={project_id}")
#   if url=="vpc":
#      r = requests.get(cloud_endpoints[url]+qr+f"?project_id={project_id}",headers=headers)
#   else:
   r = requests.get(cloud_endpoints[url]+qr+f"?project_id={project_id}&offset={offset}&limit={limit}",headers=headers)

   if r.status_code != 200:
      print("Error in query\n")
      print(r.text)
      exit(1)

   data=r.json()
   
   if "items" in data:
      items_name="items"
   elif "vpcs" in data:
      items_name="vpcs"

   res.extend(data[items_name])
   #print(res)
   if "offset" in data and "limit" in data and "total" in data and (int(data["offset"])+int(data["limit"]))<int(data["total"]):
      res.extend(query(url,qr,int(data["offset"])+int(data["limit"]),int(data["limit"])))
   return res
  
def match_res(data, match, value):
#   print("Match:",value)
   for j in data:
      #print(j)
      for m in range(len(match)):
         if not match[m] in j.keys() or str(j[match[m]])!=value[m]:
            break
      else:   
         return j


   print("False")
   exit(1)

if __name__ == "__main__":
   main()

