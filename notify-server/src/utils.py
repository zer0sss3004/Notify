from datetime import datetime
import splunklib.client as client
import splunklib.results as results
import json


def connect_to_splunk(
    username,
    password,
    host,
    app,	
    port="8089",
    owner="admin",
    sharing="user",
):
    try:
        service = client.connect(
            host=host,
            port=port,
            username=username,
            password=password,
            owner=owner,
            app=app,
            sharing=sharing,
        )
        if service:
            print("Splunk service created successfully")
            print("------------------------------------")
        return service
    except Exception as e:
        print(e)


def run_normal_mode_search(splunk_service, search_string, payload={}):
    try:
        job = splunk_service.jobs.create(search_string, **payload)
        # print(job.content)
        while True:
            while not job.is_ready():
                pass
            if job["isDone"] == "1":
                break
        for result in results.ResultsReader(job.results()):
            return result

    except Exception as e:
        return e

def generate_response(status, path, detail, data):
    if status == 1:
        success_respone_format = {
            "Message": "success",
            "path": f"{path}",
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "successfully": 1,
            "details": f"{detail}",
            "data": data,
        }

        return success_respone_format
    else:
        fail_respone_format = {
            "Message": "fail",
            "path": f"{path}",
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "successfully": 0,
            "details": f"{detail}",
            "data": data,
        }
        return fail_respone_format
