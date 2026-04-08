import os
from jira import JIRA

def get_jira_client():
    """Initializes and returns the Jira client using environment variables."""
    jira_url = os.getenv('JIRA_URL')
    jira_email = os.getenv('JIRA_EMAIL')
    jira_token = os.getenv('JIRA_API_TOKEN')
    
    if not all([jira_url, jira_email, jira_token]):
        print("Jira credentials missing in .env file.")
        return None
        
    try:
        return JIRA(server=jira_url, basic_auth=(jira_email, jira_token))
    except Exception as e:
        print(f"Failed to connect to Jira: {e}")
        return None

def add_worklog_to_issue(issue_key: str, time_spent_seconds: float, comment: str) -> bool:
    """Pushes a worklog to a specific Jira issue."""
    client = get_jira_client()
    if not client:
        return False
        
    try:
        # The Jira API accepts timeSpentSeconds as an integer
        client.add_worklog(
            issue=issue_key, 
            timeSpentSeconds=int(time_spent_seconds), 
            comment=comment
        )
        return True
    except Exception as e:
        print(f"Jira Worklog Error for {issue_key}: {e}")
        return False
