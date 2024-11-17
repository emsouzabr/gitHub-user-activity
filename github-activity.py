import sys
import json
import urllib.request
from collections import Counter

# Function to fetch user activity from GitHub API
def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = response.read()
                events = json.loads(data)
                return events
            else:
                print(f"Failed to fetch data. Status code: {response.status}")
                return None
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to display recent activity
def display_activity(events):
    if not events:
        print("No activity found or an error occurred.")
        return

    activity_counter = Counter()
    total_commits = Counter()
    for event in events:
        event_type = event['type']
        repo_name = event['repo']['name']

        if event_type == 'PushEvent':
            commit_count = len(event['payload']['commits'])
            total_commits[repo_name] += commit_count
        elif event_type == 'IssuesEvent':
            action = event['payload']['action']
            activity_counter[f"{action.capitalize()} an issue in {repo_name}"] += 1
        elif event_type == 'WatchEvent':
            activity_counter[f"Starred {repo_name}"] += 1
        else:
            activity_counter[f"{event_type} in {repo_name}"] += 1

    for repo, commit_count in total_commits.items():
        print(f"Pushed {commit_count} commits to {repo}")

    for activity, count in activity_counter.items():
        if count > 1:
            print(f"{activity} {count} times")
        else:
            print(activity)

# Main script
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: github-activity <username>")
    else:
        username = sys.argv[1]
        events = fetch_github_activity(username)
        display_activity(events)
