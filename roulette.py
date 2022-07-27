import random
import requests
import webbrowser
from bs4 import BeautifulSoup

def main():
    page = requests.get("https://github.com/tgstation/tgstation/issues")
    soup = BeautifulSoup(page.content, 'html.parser')
    total_issues = soup.find('div', {"aria-label": "Issues"}).find('div').find('div')
    total_issues = total_issues['id'].split("_")[1]

    random_issue = random.randint(1, int(total_issues))

    while(not is_valid_issue(random_issue)):
        random_issue = random.randint(1, int(total_issues))

    webbrowser.open("https://github.com/tgstation/tgstation/issues/" + str(random_issue))  # Go to the issue!

def is_valid_issue(issue_number: int):
    url = "https://github.com/tgstation/tgstation/issues/" + str(issue_number)
    issue_page = requests.get(url)
    soup = BeautifulSoup(issue_page.content, 'html.parser')

    pr_reference = soup.find('span', {"title": "tgstation/tgstation:master"})

    print("[#" + str(issue_number) + "] " + soup.find('span', {"class": "js-issue-title markdown-title"}).text)

    if(pr_reference is not None):
        return False

    open_label = soup.find('span', attrs = {"title": "Status: Open"})
    return open_label is not None

main()
