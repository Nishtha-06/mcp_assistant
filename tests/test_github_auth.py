#To verify that the GitHub token stored in .env is valid and can authenticate with the GitHub API.

import os 

import httpx #httpx is a Python library used to send HTTP requests.We need it because we want Python to communicate with the GitHub API.
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

if not token:
    print("GITHUB Token not found")
    exit(1) #1 generally indicates that the program ended because of an error.

#This creates the HTTP headers that will be sent to GitHub.
#headers give GitHub additional information needed to process that request
headers = {
    "Authorization" : f"Bearer {token}", # Github needs to know Who is making this request, and are they authorized? So we say Here is my authentication token. Use it to authenticate me.
    "Accept" : "acpplication/vnd.github+json", # I want the response in GitHub's JSON format.
}

response = httpx.get(
    "https://api.github.com/user",
    headers = headers,
)

print("Status: ",response.status_code)

if response.status_code == 200:
    user = response.json()
    print("Github authentication successful")
    print()





