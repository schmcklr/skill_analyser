import requests
import pandas as pd

# requesting access token
url = "https://auth.emsicloud.com/connect/token"
payload = "client_id=lwtnyxiuohd90aqc&client_secret=ZqV4d9LQ&grant_type=client_credentials&scope=emsi_open"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.request("POST", url, data=payload, headers=headers)
url = "https://emsiservices.com/skills/versions/latest/skills"

# storing access token
access_token = response.json()["access_token"]

# requesting skill list
querystring = {"fields": "name", "limit": "100000"}
headers = {'Authorization': 'Bearer ' + access_token}
response = requests.request("GET", url, headers=headers, params=querystring)
data = response.json()

# initialise skill array
skills = []

# add skills to the array
for entry in data["data"]:
    skills.append(entry["name"].lower())

# TODO: Remove just needed for developing purpose
# Convert the array to dataFrame
# df = pd.DataFrame(skills, columns=['Skills'])
# Write the DataFrame to an Excel file
#df.to_excel('array_to_excel.xlsx', index=False)