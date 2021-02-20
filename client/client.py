
import requests
import json


data = {

    "jwtToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Ikh1Z28iLCJwYXNzd29yZCI6IiRwYmtkZjItc2hhNTEyJDI1MDAwJDQzeHZyYlhXT2lkRWFPMmRFMEtJa1EkaEdtejRrMTFqeW5SZTB2Q243ZEZrek9KL05WeFYzeEk0ZDJ3d3FCcTcwOEVFeU1DSWFyeHFaUGcyWGMyVmFTQWtSeFhJTlRhSWpCa0tMSTIybW5lUkEiLCJlbWFpbCI6Imh1Z29tb250YWV6QGdtYWlsLmNvbSIsImlzc3VhbF90aW1lIjoxNjEzNzU3NjQ0LCJleHBpcmVfdGltZSI6MTYxMzc2MTE0NH0.MovdDZ-dUd5bcUFYmgbnIPrsrML9l4hG242LIpCUAew",
    "refreshToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Ikh1Z28iLCJwYXNzd29yZCI6IiRwYmtkZjItc2hhNTEyJDI1MDAwJDQzeHZyYlhXT2lkRWFPMmRFMEtJa1EkaEdtejRrMTFqeW5SZTB2Q243ZEZrek9KL05WeFYzeEk0ZDJ3d3FCcTcwOEVFeU1DSWFyeHFaUGcyWGMyVmFTQWtSeFhJTlRhSWpCa0tMSTIybW5lUkEiLCJlbWFpbCI6Imh1Z29tb250YWV6QGdtYWlsLmNvbSJ9.3MKwUq3rzYNQ2R77V92xosnYvgsGO0gRlKoDTZjGJQg"
}

    
response = requests.post('http://localhost:8000/api', headers= data)

if response.status_code == 200:
    print(response.json)
