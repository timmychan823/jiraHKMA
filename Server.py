#In command line:
#export FLASK_APP=Server
#set FLASK_RUN_PORT=5000
#flask run

#also needa use a thread to put into redis queue

from flask import Flask, request
from redis import Redis
from rq import Queue
import WorkerJob
import ResourcesPackager



app = Flask(__name__)


@app.route('/sendIssueDetails', methods = ['POST'])
def sendIssueDetails():
    data = request.get_json() #get Custom Data which is in the json format {"key": {{issue.key}}}

    #then get data by search the issue with the issue key (change the code below later)

    redis_conn = Redis(host="localhost", port=5001)
    task_queue = Queue("task_queue", connection=redis_conn)
    
    task_queue.enqueue(WorkerJob.workerJob, data["key"])
    return "JSON received"