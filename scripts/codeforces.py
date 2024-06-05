import requests
import pandas as pd
import json
# stringbuffer = ""

contensts = {}


def get_user_contest_ratings(user_name):
    url = f"https://codeforces.com/api/user.rating?handle={user_name}"
    response = requests.get(url)
    if response.status_code != 200:
        print(response, response.text, response.status_code)
        raise Exception(f"Failed to fetch contest ratings for user {user_name}")

    json_data = response.json()
    return json_data['result']

def get_user_problem_status(user_name, **filters):
    url = f"https://codeforces.com/api/user.status?handle={user_name}"
    response = requests.get(url)
    if response.status_code != 200:
        print(response, response.text, response.status_code)
        raise Exception(f"Failed to fetch contest ratings for user {user_name}")
    
    json_data = response.json()
    return json_data['result']


def get_user_info(*user_names):
    url = f"https://codeforces.com/api/user.info?handles={';'.join(user_names)}"
    response = requests.get(url)
    if response.status_code != 200:
        print(response, response.text, response.status_code)
        raise Exception(f"Failed to fetch contest ratings for user {user_name}")
    
    json_data = response.json()
    return json_data['result']

def get_contest_status(contest_id, user_name=None):
    url = f"https://codeforces.com/api/contest.status?contestId={contest_id}"
    if user_name:
        url += f"&handle={user_name}"
    
    response = requests.get(url)
    if response.status_code != 200:
        print(response, response.text, response.status_code)
        raise Exception(f"Failed to fetch contest ratings for user {user_name}")
    
    json_data = response.json()
    return json_data['result']


if __name__ == "__main__":
    user_name = "h3110_fr13nd"
    user_names = ["h3110_fr13nd", "tourist", 'harshdobariya79']
    contest_id = 1782
    ratings = get_user_contest_ratings(user_name)
    contest_df = pd.json_normalize(ratings)
    
    problems = get_user_problem_status(user_name)
    problems_df = pd.json_normalize(problems)

    user_info = get_user_info(*user_names)
    user_info_df = pd.json_normalize(user_info)

    contest_status = get_contest_status(contest_id, user_name)
    contest_status_df = pd.json_normalize(contest_status)
    
    
    print("User Info:")
    print(user_info_df)
    print("\n\n")
    print("Contest Ratings:")
    print(contest_df)
    print("Problems Status:")
    print(problems_df)
    print("Contest Status:")
    print(contest_status_df)

    
        

