from clientAPI.dump import APIBase, DumpingMethods
from assertpy import assert_that
import json

class AuthFeature(APIBase):
    def __init__(self, store_name, email, password):
        super().__init__()
        self.recovery = DumpingMethods()
        self.base_url=DumpingMethods().base_url
        self.store_name = store_name
        self.email = email
        self.password = password
        try:
            self.access_token = self.recovery.get_log("user_data")["data"]["accessToken"]
            self.refresh_token = self.recovery.get_log("user_data")["data"]["refreshToken"]
        except Exception as e:
            print(f"{type(e)}\n{e}")

    def sign_up(self):
        payload = {"name": self.store_name,
                   "email": self.email,
                   "password": self.password}
        session = self.post(self.base_url+"/registration", data=payload)
        return session
    
    def sign_in(self):
        payload = {"email": self.email,
                   "password": self.password}
        session = self.post(self.base_url+"/authentications", data=payload)
        main_data = session.json()
        self.recovery.create_log(main_data, "user_data")
        return session
    
    def update_token(self):
        payload = {"refreshToken": self.refresh_token}
        session = self.put(self.base_url+"/authentications", data=payload,
                           headers={"Authorization": f"Bearer {self.access_token}"})
        token = session.json()["data"]["accessToken"]
        self.headers["Authorization"] = f"Bearer {self.access_token}"
        self.recovery.update_log("user_data", "accessToken", token)
        return session
    
    def sign_out(self):
        payload = {"refreshToken": self.refresh_token}
        session = self.delete(self.base_url+"/authentications", data=payload)
        self.recovery.update_log('user_data', 'accessToken', '')
        return session
    
class BaseFeature(APIBase):
    def __init__(self, url_path):
        super().__init__()
        self.recovery = DumpingMethods()
        self.base_url = self.recovery.base_url
        self.url_path = url_path
        try:
            self.access_token = self.recovery.get_log("user_data")["data"]["accessToken"]
            self.refresh_token = self.recovery.get_log("user_data")["data"]["refreshToken"]
        except Exception as e:
            print(f"{type(e)}\n{e}")

    def add_new(self, payload, logger=None):
        session = self.post(self.base_url+"/"+self.url_path, json=payload,
                            headers={"Authorization": f"Bearer {self.access_token}"})
        feature_data = session.json().get("data")
        default_logger = self.url_path[:-1]+"Id"
        if logger == None:
            logger = default_logger
        else:
            print(end="\r")
        self.headers["Authorization"] = f"Bearer {self.access_token}"
        self.recovery.create_log(feature_data[logger], logger)
        return session

    def get_detail(self, json=None, params=None):
        self.headers["Authorization"] = f"Bearer {self.access_token}"
        return self.get(self.base_url+"/"+self.url_path, params=params, json=json,
                        headers={"Authorization": f"Bearer {self.access_token}"})
    
    def update_data(self, query, payload):
        self.headers["Authorization"] = f"Bearer {self.access_token}"
        return self.put(self.base_url+"/"+self.url_path+"/"+query, data= payload,
                        headers={"Authorization": f"Bearer {self.access_token}"})
    
    def remove_data(self, query):
        self.headers["Authorization"] = f"Bearer {self.access_token}"
        return self.delete(self.base_url+"/"+self.url_path+"/"+query,
                           headers={"Authorization": f"Bearer {self.access_token}"})

class SpecialFeature(APIBase):
    def __init__(self, url_path):
        super().__init__()
        self.basef = BaseFeature(url_path)
        self.create_log = DumpingMethods().create_log
        self.get_log = DumpingMethods().get_log
        self.url_path = url_path

    def get_detail(self, iD, logger=None):
        return self.get(self.basef.base_url+"/"+self.url_path+"/"+iD,
                        headers={"Authorization": f"Bearer {self.basef.access_token}"})