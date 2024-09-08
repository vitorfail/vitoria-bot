import requests
import pandas as pd
pd.set_option('display.max_rows', None)

# information
business_account_id = "7816768729"
access_token = "IGQWROR05pZAFBNdE9QeEg2a2YtX3NoUElqdmNFUXlmSzZAPczIxeTFvMHJiNEYxeUtlSy1KaFVWdC1MUk00ckRPWjZAnUkFPT1FhZAnJPRE1PeFhTM21NdmR0bGpLZAnlBbmtGa0F5eHFFMkVCTV9Tc3hRenNFWmhZAMVEZD"
fields = "followers_count,media_count,name"
version = "v17.0"
username = "breno_fons"

def user_info(version, igUserId,access_token,username,fields):
    request_url = f"https://graph.facebook.com/{version}/{igUserId}?fields=business_discovery.username({username}){{{fields}}}&access_token={access_token}"
    print(request_url);
    response = requests.get(request_url)
    return response.json()

print(user_info(version,business_account_id,access_token,username,fields))