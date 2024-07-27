import requests
import json


class JiraAPIWorker:
    def __init__(self, user_name,api_token,jira_instance,jira_api_version_url):
        self.user_name = user_name
        self.api_token = api_token
        self.jira_instance = jira_instance
        self.jira_api_version_url = jira_api_version_url

    def getIssuesByJQL(self,jql):
        jira_url = f"{self.jira_instance}{self.jira_api_version_url}/search"

        query = {'jql': f'{jql}'}
        headers = {
            "Authorization": f"Bearer {self.api_token}"
        }

        response = requests.request("GET",jira_url,headers=headers,params=query)
        print(response.json())


    def getAllIssues(self,project_name):
        jira_url = f"{self.jira_instance}{self.jira_api_version_url}/search"
        query = {'jql': f'project = {project_name}'}
        headers = {
            "Authorization": f"Bearer {self.api_token}"
        }

        response = requests.request("GET",jira_url,headers=headers,params=query)
        print(response.json())

    
    def getIssueURL(self, issue_key:str) -> str:
        return
    
    def getAttachments_URL(self, issue_key:str) -> list[str]:
        return
    