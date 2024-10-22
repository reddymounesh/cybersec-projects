import requests
from requests.exceptions import RequestException
import time

def check_username(username,platfrom):

    url=platfrom.format(username=username)

    try:
        response=requests.get(url,timeout=5)
        if response.status_code==200:
            return True
        
    except RequestException as e:
        print(f"Error checking {platfrom}:{e}")

    return False



def search_username(username):

    platfroms={
        "Github":"https://github.com/{username}",
        "Instagram":"https://www.instagram.com/{username}",
        "Twitter":"https://twitter.com/{username}",
        "Reddit":"https://www.reddit.com/{username}",
        "Facebook":"https://www.facebook.com/{username}",
        "LinkedIn":"https://www.linkedin.com/in/{username}",


    }


    results={}
    for platfrom,url in platfroms.items():
        if check_username(username,url):
            results[platfrom]=url.format(username=username)

        time.sleep(1)
    return results



if __name__=='__main__':
    username=input("Enter the username to search :")
    results=search_username(username)

    if results:
        print(f"Found {username} on the following platfroms:")
        for platfrom,url in results.items():
            print(f"{platfrom}:{url}")

    else:
        print(f"No results found for {username}")




