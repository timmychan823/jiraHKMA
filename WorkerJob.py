import ResourcesPackager
import JiraAPIWorker

USER_NAME = "chanshunhei@gmail.com"
API_TOKEN = ""
JIRA_INSTANCE = "https://chan-shun-hei.atlassian.net/"
JIRA_API_VERSION_URL = "rest/api/2"
MAIL_ADDRESS = "tshchan@hkma.gov.hk"

def workerJob(issuekey):
    resourcesPackager = ResourcesPackager.ResourcesManager(issuekey)

    jiraAPIWorker = JiraAPIWorker()
    for i in range(len(data["fields"]["attachment"])):
        resourcesPackager.downloadFile(data["fields"]["attachment"][i]["content"],{"Authorization": f"Bearer {API_TOKEN}"},data["fields"]["attachment"][i]["filename"]) #need Auth I guess) #need Auth I guess

    resourcesPackager.compress()
