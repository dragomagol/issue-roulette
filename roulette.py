import random
import requests
import threading
import webbrowser
from bs4 import BeautifulSoup

class myThread (threading.Thread):
    def __init__(self, max_issues):
        threading.Thread.__init__(self)
        self.max_issues = max_issues

    def run(self):
        find_valid_issue(self.max_issues)

def find_valid_issue(max_issues):
    random_issue = random.randint(1, int(max_issues))
    global issue_found
    while not is_valid_issue(random_issue) and not issue_found:
        random_issue = random.randint(1, int(max_issues))

    if not issue_found:
        issue_found = True
        webbrowser.open("https://github.com/tgstation/tgstation/issues/" + str(random_issue))  # Go to the issue!


def is_valid_issue(issue_number: int):
    url = "https://github.com/tgstation/tgstation/issues/" + str(issue_number)
    issue_page = requests.get(url)
    soup = BeautifulSoup(issue_page.content, 'html.parser')

    pr_reference = soup.find('span', {"title": "tgstation/tgstation:master"})

    print("[#" + str(issue_number) + "] " + soup.find('span', {"class": "js-issue-title markdown-title"}).text)

    if(pr_reference is not None):
        return False

    open_label = soup.find('span', attrs = {"class": "State State--open"})
    return open_label is not None

## --------------------------- THREADING
issue_found = False
num_threads = 4
threads = []

## --------------------------- MAIN
page = requests.get("https://github.com/tgstation/tgstation/issues")
soup = BeautifulSoup(page.content, 'html.parser')
total_issues = soup.find('div', {"aria-label": "Issues"}).find('div').find('div')
total_issues = total_issues['id'].split("_")[1]

for i in range(0, num_threads):
    thread = myThread(total_issues)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
