from urllib.parse import parse_qs
import curlify
import requests
import json

class APIBase(requests.Session):
    base_url: str = ""

    def __init__(self):
        super(APIBase, self).__init__()
        self.hooks["response"].append(self._logging)

    @staticmethod
    def _logging(response: requests.Response, *args, **kwargs):
        """Function to handle logging in hook['response'] """
        print("[Request]".center(80, "-"))
        print("[{:^7}]\n{}\n{}".format(response.request.method, response.request.url, "-"*80))
        print("[{:^7}]\n{}\n{}".format("HEADERS", ", ".join(f"{item}" for item in response.request.headers), "-"*80))
        print("[{:^7}]\n{}\n{}".format("DEBUG", curlify.to_curl(response.request), "-"*80))
        if response.request.body is not None:
            request_body = {key: value[0] for key, value in parse_qs(response.request.body).items()}
            print("[{:^7}]\n{}\n".format("BODY", json.dumps(request_body)))
        
        #print("\n\n")
        print("[Response]".center(80, "-"))
        print("[{:^7}]\n {}, elapsed: {}s\n{}".format("STATUS", response.status_code, response.elapsed.total_seconds(), "-"*80))
        print("[{:^7}]\n{}\n{}".format("HEADER", json.dumps(dict(response.headers), indent=2), "-"*80))
        if response.text != "":
            print("[{:^7}]\n{}\n".format("BODY", json.dumps(response.json(), indent=1)))