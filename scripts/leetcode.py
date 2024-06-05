import requests
import json
from datetime import datetime

# GraphQL query
query = """
query getUserProfile($username: String!) {
  allQuestionsCount {
    difficulty
    count
  }
  matchedUser(username: $username) {
    contributions {
      points
    }
    profile {
      reputation
      ranking
    }
    submissionCalendar
    submitStats {
      acSubmissionNum {
        difficulty
        count
        submissions
      }
      totalSubmissionNum {
        difficulty
        count
        submissions
      }
    }
  }
  recentSubmissionList(username: $username) {
    title
    titleSlug
    timestamp
    statusDisplay
    lang
    __typename
  }
  matchedUserStats: matchedUser(username: $username) {
    submitStats: submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
        submissions
        __typename
      }
      totalSubmissionNum {
        difficulty
        count
        submissions
        __typename
      }
      __typename
    }
  }
}
"""

def format_data(data):
    # Convert submissionCalendar keys from timestamps to yyyy-MM-dd
    submission_calendar_converted = {}
    for timestamp, value in json.loads(data.get("matchedUser", {}).get("submissionCalendar", {})).items():
        date_string = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
        submission_calendar_converted[date_string] = value
    
    send_data = {
        "totalSolved": data["matchedUser"]["submitStats"]["acSubmissionNum"][0]["count"],
        "totalSubmissions": data["matchedUser"]["submitStats"]["totalSubmissionNum"],
        "totalQuestions": data["allQuestionsCount"][0]["count"],
        "easySolved": data["matchedUser"]["submitStats"]["acSubmissionNum"][1]["count"],
        "totalEasy": data["allQuestionsCount"][1]["count"],
        "mediumSolved": data["matchedUser"]["submitStats"]["acSubmissionNum"][2]["count"],
        "totalMedium": data["allQuestionsCount"][2]["count"],
        "hardSolved": data["matchedUser"]["submitStats"]["acSubmissionNum"][3]["count"],
        "totalHard": data["allQuestionsCount"][3]["count"],
        "ranking": data["matchedUser"]["profile"]["ranking"],
        "contributionPoint": data["matchedUser"]["contributions"]["points"],
        "reputation": data["matchedUser"]["profile"]["reputation"],
        "submissionCalendar": submission_calendar_converted,
        "recentSubmissions": data["recentSubmissionList"],
        "matchedUserStats": data["matchedUser"]["submitStats"]
    }
    return send_data

# Fetching the data
def leetcode(user_id):
    url = 'https://leetcode.com/graphql'
    headers = {'Content-Type': 'application/json', 'Referer': 'https://leetcode.com'}
    variables = {"username": user_id}
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if 'errors' in data:
            return data
        else:
            formatted_data = format_data(data['data'])
            return formatted_data
    else:
        return f"Failed to fetch data. Status Code: {response.status_code}"

if __name__ == "__main__":
    user_id = "USERNAME"
    result = leetcode(user_id)
    print(json.dumps(result, indent=4))
