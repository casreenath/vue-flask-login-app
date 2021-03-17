import json
import requests
import logging


class CommonUtils:
    def __init__(self):
        return

    def api_call_retry(self, url, parameters=None, count=3,
                       call_method="post", timeout=100):
        try:
            error_msg = ""
            for counter in range(count):
                try:
                    print(
                        "trying to call API : {}/{}".format(counter+1, count))
                    print("API Called url: {} Prams: {}".format(url,
                                                                parameters))
                    req2 = ''
                    if call_method == "post":
                        req2 = requests.post(
                            url=url, params=parameters, timeout=timeout)
                    elif call_method == "get":
                        req2 = requests.get(
                            url=url, params=parameters, timeout=timeout)
                    else:
                        raise Exception(
                            "Invalid call_method : {}".format(call_method))
                    if type(req2) == str:
                        raise Exception("Did not receive response")
                    print(req2)
                    req2dict = json.loads(req2.text)
                    if (str(req2dict['status']).lower() == "true" or
                            str(req2dict['status']).lower() == "success"):
                        return req2dict
                    else:
                        print("Error while calling API : "
                              "{}\nError: {}".format(url,
                                                     req2dict['errmsg']))
                        error_msg = req2dict['errmsg']
                except Exception as errmsg:
                    print("Error calling the API : {}\nResponse : {}".format(
                        errmsg, req2.status_code))
                    error_msg = errmsg
            raise Exception(
                "Failed to call API {} times: {}".format(count, error_msg))
        except Exception as errmsg:
            raise Exception(
                "Failed api_call_retry with error: {}".format(errmsg))
        return
