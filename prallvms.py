#
##      .SYNOPSIS
##      Example script to query the Veeam ONE 2.1 api and pull all protected virtual machines and Veeam for Azure API and pull protected machines
##	Then the first file is written to csv with headers and then the second file is appended without headers
##	This is to create a file with servername and backupdate event though the 2 apis have different header names for the backup
## 
##      .DESCRIPTION
##      Provided as is for learning purposes
#
#

##
## urllib3 is used to disable warnings due to lack of installed certificate for end point.
##
import urllib3
urllib3.disable_warnings()
import requests 
import pandas as pd
import json

#import pdb
#pdb.set_trace()


baseurl = "https://IPADDRESS:PORT"
apiurl = "{}/api/token".format(baseurl)

#print (apiurl)

##
## user as domain\user or user.name@domain.com
apipayload = {
  "username": "domain\user",
  "password": "PasswordXX",
  "grant_type": "password",
  "refresh_token": ""
}



headers = {
  "Content-Type": "application/x-www-form-urlencoded",
}

#
## verify=False also due to unsigned endpoint
#
response = requests.post(apiurl, data=apipayload, headers=headers, verify=False)

token = response.json()
apitoken = token.get("access_token")
#print(apitoken)


vmurl = "{}/api/v2.1/protectedData/virtualMachines".format(baseurl)
#print (vmurl)

query = {
  "Offset": "0",
  "Limit": "100",
  "Filter": "",
  "Sort": "",
  "Select": ""
}


headers = {
        "Authorization": "Bearer " + apitoken,
        "Accept": "application/json"
        }

response = requests.get(vmurl, headers=headers, params=query, verify=False)

jsondata = response.json()
jsonitems = pd.DataFrame(jsondata['items'])
csvcolumns = ["name", "lastProtectedDate" ]
jsonitems[csvcolumns].to_csv('output/prallvms.csv', index=False)

#exitcode = response.status_code
#print(exitcode)

baseurl = "https://IPADDRESSAZURE"
apiurl = "{}/api/oauth2/token".format(baseurl)
print (apiurl)

payload = {
  "username": "user",
  "password": "PasswordXX",
  "refresh_token": "",
  "grant_type": "Password",
  "mfa_token": "",
  "mfa_code": "",
  "updater_token": "",
  "saml_response": "",
  "sso_token": "",
  "short_lived_refresh_token": "false"
}




headers = {
  "accept": "application/json",
  "Content-Type": "application/x-www-form-urlencoded"
}


response = requests.post(apiurl, data=payload, headers=headers, verify=False)


token = response.json()
apitoken = token.get("access_token")
#print(apitoken)


vmurl = "{}/api/v5/protectedItem/virtualMachines".format(baseurl)
#print (vmurl)

query = {
  "Offset": "0",
  "Limit": "-1",
  "SearchPattern": "",
  "Sync": "",
  "FlrSession": "",
  "DataRetrievalStatuses": ""
}

headers = {
        "Authorization": "Bearer " + apitoken,
        "Accept": "application/json"
        }

#response = requests.get(vmurl, headers=headers, params=query, verify=False)
response = requests.get(vmurl, headers=headers, verify=False)

#
# index=False stops it output an index column and header=False removes the header
jsondata = response.json()
jsonitems = pd.DataFrame(jsondata['results'])
csvcolumns = ["name", "lastBackup" ]
with open('output/prallvms.csv', 'a') as f:
    jsonitems[csvcolumns].to_csv(f, index=False, header=False)


#exitcode = response.status_code
#print(exitcode)

