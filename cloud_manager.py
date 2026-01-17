import requests
import json
import os
import datetime

class CloudManager:
    def __init__(self, domain, username, password):
        self.domain = domain
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.base_url = f'https://{self.domain}/'
        self.validationkey = self.login()
    
    def login(self):
        login_url = self.base_url + "sapi/login"
        params = {'action': 'login'}
        data = {'login': self.username, 'password': self.password}
        headers = {'referer': self.base_url}       
        response = self.session.post(login_url, params=params, data=data, headers=headers)
        user_info = response.json()
        return user_info['data']['validationkey']
    
    def get_file_info(self,file_id):
        get_file_info_url = self.base_url + 'sapi/media'
        params = {'action':'get','validationkey': self.validationkey}
        json_data = {'data':{'ids':[file_id]}}
        response = self.session.post(get_file_info_url,params=params,json=json_data)
        file_info = response.json()
        return file_info

    def get_root_folder_id(self):
        get_root_folder_id_url = self.base_url + 'sapi/media/folder'
        params = {'action': 'get','limit':1,'validationkey': self.validationkey}
        response = self.session.post(get_root_folder_id_url, params=params)
        root_folders_info = json.loads(response.text)
        root_folder_id = root_folders_info['data']['folders'][0]['id']
        return root_folder_id

    def list_folders(self,parentid,previous_folders=False):
        if parentid == False:
            parentId = 0
        list_subfolders_url = self.base_url + 'sapi/media/folder'
        params = {'action': 'list','parentid':parentid, 'limit':200,'validationkey': self.validationkey}
        if previous_folders == False:
            previous_folders = []
        else:
            params['offset'] = len(previous_folders)
        response = self.session.get(list_subfolders_url, params=params)
        folders_data = json.loads(response.text)
        folders = folders_data['data']['folders']
        folders.extend(previous_folders)
        if len(folders_data['data']['folders']) == 200:
            return self.list_folders(parentid,folders)
        else:
            return folders
        
    def list_files(self, folderid,previous_files=False):
        list_folder_files_url = self.base_url + 'sapi/media'
        params = {'action': 'get','folderid': folderid,'limit': 200,'validationkey': self.validationkey}
        json_data = {"data":{"fields":["name","modificationdate","size"]}}
        if previous_files == False:
            previous_files = []
        else:
            params['offset'] = len(previous_files)
        response = self.session.post(list_folder_files_url, params=params,json=json_data)
        files_data = json.loads(response.text)
        files = files_data['data']['media']
        files.extend(previous_files)
        if files_data['data']['more'] == True:
            return self.list_files(folderid,files)
        else:
            return files
    
    def move_uncategorized_timeline(self,folder_id):
        get_timeline_ids_url = self.base_url + 'sapi/media/timeline'
        params = {'action':'get','validationkey':self.validationkey}
        json_data = {"data":{"source":"media","types":["picture","video"],"sortorder":"uploaded","origin":["omh"]}}
        response = self.session.post(get_timeline_ids_url, params=params,json=json_data)
        file_ids_data = json.loads(response.text)
        #file_ids = file_ids_data['data']['periods'][0]['ids']
        if len(file_ids_data['data']['periods']) > 0:
            for period in file_ids_data['data']['periods']:
                for file_id in period['ids']:
                    self.move_file(file_id,folder_id)
        
    
    def list_all(self,parentid):
        items=[]
        def walk(folderid,current_path):
            subfolders=self.list_folders(folderid)
            subfolders=sorted(subfolders,key=lambda x:x['name'])
            for folder in subfolders:
                if current_path=="":
                    p="\\"+folder['name']
                else:
                    p=current_path+"\\"+folder['name']
                obj={'id':folder['id'],'name':folder['name'],'path':p,'kind':'folder'}
                items.append(obj)
                walk(folder['id'],p)
            folder_files=self.list_files(folderid)
            folder_files=sorted(folder_files,key=lambda x:x['name'])
            for f in folder_files:
                if current_path=="":
                    p="\\"+f['name']
                else:
                    p=current_path+"\\"+f['name']
                obj={'id':f['id'],'name':f['name'],'path':p,'kind':'file'}
                items.append(obj)
        walk(parentid,"")
        return items

    def create_folder(self,name,parentid=False):
        if parentid == False:
            parentid = self.get_root_folder_id()
        create_folder_url = self.base_url + 'sapi/media/folder'
        params = {'action':'save','validationkey':self.validationkey}
        json_data = {"data":{"magic":False,"offline":False,"name":name,"parentid":parentid}}
        response = self.session.post(create_folder_url,json=json_data,params=params)

    def upload_file(self, file_path, folder_id):
        upload_url = self.base_url + 'sapi/upload'
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        mod_time = os.path.getmtime(file_path)
        mod_date = datetime.datetime.fromtimestamp(mod_time)
        formatted_date = mod_date.strftime("%Y%m%dT%H%M%SZ")
        metadata = {"data":{"name":file_name,"size":file_size,"modificationdate":formatted_date,"contenttype":"application/pdf","folderid":folder_id}}
        params = {'action': 'save','acceptasynchronous': 'true','validationkey': self.validationkey,}
        with open(file_path, 'rb') as file:
            files = {
                'data': (None, json.dumps(metadata), 'application/json'),
                'file': (file_name, file, 'application/pdf')
            }
            response = self.session.post(upload_url, params=params, files=files)
        
        return response.json()
    
    def download_file(self, fileid, save_path=None):
        if save_path is None:
            save_path = os.getcwd()
        file_info_url = self.base_url + 'sapi/media'
        params = {'action': 'get', 'origin': 'omh,dropbox', 'validationkey': self.validationkey}
        json_data = {"data": {"ids": [fileid], "fields": ["url", "name"]}}
        response = self.session.post(file_info_url, params=params, json=json_data)
        file_info = response.json()
        download_url = file_info['data']['media'][0]['url']
        name = file_info['data']['media'][0]['name']
        file_path = os.path.join(save_path, name)
        
        response = self.session.get(download_url, stream=True)
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        
        return file_path
    
    def move_file(self,file_id,folder_id):
        move_file_url = self.base_url + 'sapi/media/folder'
        params = {'action':'add-item','validationkey':self.validationkey}
        json_data = {'data':{'items':[file_id],'folderid':folder_id}}
        response = self.session.post(move_file_url, params=params, json=json_data)

    def remove_file(self,file_id,softdelete):
        file_info = self.get_file_info(file_id)
        mediatype = file_info['data']['media'][0]['mediatype']
        plural = mediatype + 's'
        remove_file_url = self.base_url + 'sapi/media/' + mediatype
        params = {'action':'delete','softdelete':softdelete,'validationkey':self.validationkey}
        json_data = {'data':{plural:[file_id]}}
        self.session.post(remove_file_url,json=json_data,params=params)
    
    def remove_folder(self,folder_id,softdelete):
        remove_folder_url = self.base_url + 'sapi/media/folder'
        if softdelete == True:
            action = 'softdelete'
        else:
            action = 'delete'
        params = {'action':action,'validationkey': self.validationkey}
        json_data = {'data':{'folders':[folder_id]}}
        self.session.post(remove_folder_url,json=json_data,params=params)

    def get_free_space_kb(self):
        quota_stats_url = self.base_url + "sapi/media"
        params = {'action':'get-storage-space','softdeleted':True,'validationkey': self.validationkey}
        response = self.session.get(quota_stats_url, params=params)
        quota_stats = response.json()
        free_space_kb = quota_stats['data']['free'] - quota_stats['data']['softdeleted']
        return free_space_kb
        
    def sync_local_path(self,local_path,parentid=False):
        if parentid==False:
            parentid=self.get_root_folder_id()
        local_path=os.path.abspath(local_path)
        def sync_folder(path,folderid):
            entries=os.listdir(path)
            local_dirs=[e for e in entries if os.path.isdir(os.path.join(path,e))]
            local_files=[e for e in entries if os.path.isfile(os.path.join(path,e))]
            remote_folders=self.list_folders(folderid)
            remote_files=self.list_files(folderid)
            remote_folder_map={f['name']:f for f in remote_folders}
            remote_file_map={f['name']:f for f in remote_files}
            for d in local_dirs:
                if d in remote_folder_map:
                    child_id=remote_folder_map[d]['id']
                else:
                    self.create_folder(d,folderid)
                    remote_folders=self.list_folders(folderid)
                    remote_folder_map={f['name']:f for f in remote_folders}
                    child_id=remote_folder_map[d]['id']
                sync_folder(os.path.join(path,d),child_id)
            for fname in local_files:
                full=os.path.join(path,fname)
                self.upload_file(full,folderid)
            for name,f in remote_file_map.items():
                if name not in local_files:
                    self.remove_file(f['id'],True)
            for name,f in remote_folder_map.items():
                if name not in local_dirs:
                    self.remove_folder(f['id'],True)
        sync_folder(local_path,parentid)

    def sync_remote_path(self, local_path, parentid=False):
        if parentid is False:
            parentid = self.get_root_folder_id()
            local_path = os.path.abspath(local_path)
            os.makedirs(local_path, exist_ok=True)
        def sync_folder(folderid, current_local_path):
            remote_folders = self.list_folders(folderid)
            for folder in remote_folders:
                folder_name = folder['name']
                folder_id = folder['id']
                new_local_path = os.path.join(current_local_path, folder_name)
                os.makedirs(new_local_path, exist_ok=True)
                sync_folder(folder_id, new_local_path)
            remote_files = self.list_files(folderid)
            for f in remote_files:
                file_id = f['id']
                file_name = f['name']
                local_file_path = os.path.join(current_local_path, file_name)
                if not os.path.exists(local_file_path):
                    print("Descargando " + local_file_path)
                    self.download_file(file_id, current_local_path)
                else:
                    print(local_file_path + " ya existe")
        sync_folder(parentid, local_path)
