#!/bin/bash
##      .SYNOPSIS
##      Example script to query the Veeam ONE 2.1 api and pull all protected virtual machines, select some of the columnts and write to CSV text file.
## 
##      .DESCRIPTION
##      Provided as is for learning purposes
##	
##      Derived from the awesome work of Jorge De La Cruz
 
# Configurations
##

# Endpoint URL for login action
veeamUsername="DOMAIN\username" #Usually domain\user or user@domain.tld
veeamPassword="password"
veeamONEServer="https://YOUR-IP-ADDRESS" #You can use FQDN if you like as well
veeamONEPort="2741" # Check which Port

veeamBearer=$(curl -X POST --header "Content-Type: application/x-www-form-urlencoded" --header "Accept: application/json"  -d "username=$veeamUsername&password=$veeamPassword&rememberMe=&asCurrentUser=&grant_type=password&refresh_token=" "$veeamONEServer:$veeamONEPort/api/token" -k --silent | jq -r '.access_token')


##
# Building the ID to Query 
#
vONEprotectedVMsURL="$veeamONEServer:$veeamONEPort/api/v2.1/protectedData/virtualMachines?Offset=0&Limit=100"
#
# -k switch because the endpoint is not securely signed.

vONEprotectedVMsjson=$(curl -kX GET $vONEprotectedVMsURL -H "Authorization: Bearer $veeamBearer" -H "accept: application/json"  --silent  ) >/dev/null 2>&1

# File management of .json and .csv - I keep both files in case you want to use the full json as well.
if [ -f output/vONEprotectedVMs.json ]
then
	rm output/vONEprotectedVMs.json
else
	touch output/vONEprotectedVMs.json
fi

echo $vONEprotectedVMsjson >> output/vONEprotectedVMs.json 

if [ -f output/vONEprotectedVMs.csv ]
then
	rm output/vONEprotectedVMs.csv
else
	touch output/vONEprotectedVMs.csv
fi

# 
# Here the json is piped to jq (JSON processor) we take the .items object and then pull out which fields we want.
cat output/vONEprotectedVMs.json | jq -r '.items | ["name", "platform", "parentHostName", "usedSourceSizeBytes", "lastProtectedDate" ],(to_entries| .[] | [.value.name, .value.platform, .value.parentHostName, .value.usedSourceSizeBytes, .value.lastProtectedDate ]) | @csv' >> output/vONEprotectedVMs.csv
