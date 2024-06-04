import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_html_content(username, page):
    url = f"https://www.codechef.com/recent/user?page={page}&user_handle={username}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page for user {username}")

    json_data = response.json()
    return [json_data['content'], json_data['max_page']]

def get_daily_solved_problems(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    problems_by_day = {}
    
    # Find table containing the data
    table = soup.find('table', {'class': 'dataTable'})
    if not table:
        raise Exception("Could not find the data table.")
    
    rows = table.find('tbody').find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        time_element = cols[0].find('span', {'class': 'tooltiptext'})
        if time_element:
            time_str = time_element.text.strip()
        else:
            continue

        problem_name = cols[1].text.strip()
        result = cols[2].find('span').get('title', '').strip()

        # Only consider 'accepted' problems
        if 'accepted' in result.lower():
            problem_date = datetime.strptime(time_str, '%I:%M %p %d/%m/%y').strftime('%Y-%m-%d')
            if problem_date not in problems_by_day:
                problems_by_day[problem_date] = []
            problems_by_day[problem_date].append(problem_name)
    
    return problems_by_day

def main():
    username = "USERNAME" # Replace with your username
    [html_content, totalPages] = get_html_content(username, "undefined")
    solved_problems = {}

    for i in range(0,totalPages):
        [content, _] = get_html_content(username, i);
        output = get_daily_solved_problems(content)
        solved_problems = {**solved_problems, **output}
        print(f'page {i} done')
    
    for date, problems in solved_problems.items():
        print(f"Solved problems on {date}:")
        for problem in problems:
            print(f"  - {problem}")

if __name__ == "__main__":
    main()
