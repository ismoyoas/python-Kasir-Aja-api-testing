from clientAPI.base import APIBase
import json
import os

class Setup(APIBase):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://kasir-api.belajarqa.com'
        self.logs_directory = '../clientAPI/data'
        print(end='\r') if os.path.exists(self.logs_directory) else os.makedirs(self.logs_directory)


class DumpingMethods(Setup):
    def __init__(self):
        super().__init__()                

    def create_log(self, value, bin_f):
        json_data = json.dumps(value, indent=4).encode('utf-8')         
        with open(f'{self.logs_directory}/{bin_f}.bin', 'wb') as f:
            f.write(json_data)

    def get_log(self, bin_f):
        with open(f'{self.logs_directory}/{bin_f}.bin', 'rb') as f:
            data = f.read().decode('utf-8')
            return json.loads(data)
        
    def update_log(self, bin_f, key, value):
        with open(f'{self.logs_directory}/{bin_f}.bin', 'rb') as f:
            old_data = f.read().decode('utf-8')
        json_data = json.loads(old_data)
        json_data['data'][key] = value

        new_data = json.dumps(json_data, indent=4).encode('utf-8')
        with open(f'{self.logs_directory}/{bin_f}.bin', 'wb') as bin_f:
            bin_f.write(new_data)