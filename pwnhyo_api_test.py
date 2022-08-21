import requests
import json

URL = 'http://0.0.0.0:9999'
LOGIN_TOKEN = ''

def register():
    # json format
    response = requests.post(URL+'/register', data=json.dumps({'username':'api_test2', 'name':'api_test2', 'email':'api_test2@test.com', 'password':'api_test2'}))
    print(f"/register api test : {response.text}")

def login():
    # json format
    global LOGIN_TOKEN

    response = requests.post(URL+'/login', data=json.dumps({'username':'api_test2', 'password':'api_test2'}))
    LOGIN_TOKEN = json.loads(response.text)["access_token"]
    print(f"/login api test : {response.text}")

def create_arpost(): 
    # multipart/form-data
    headers = {'Authorization':f"Bearer {LOGIN_TOKEN}"}
    response = requests.post(URL+'/arpost/create', headers=headers, files={"file":("test.png", open("test.png","rb").read())}, data={'arpost_name':'제목123', 'arpost_contents':'내용123', 'x_value':'123', 'y_value':'456', 'z_value':'789'}) #tag1, tag2, tag3 is optional
    print(f"/arpost/create api test : {response.text}")

def read_arpost():
    # json
    headers = {'Authorization':f"Bearer {LOGIN_TOKEN}"}
    response = requests.post(URL+'/arpost/read', headers=headers, data=json.dumps({'arpost_id':'1'}))
    print(f"/arpost/read api test : {response.text}")

def edit_arpost():
    # multipart/form-data
    headers = {'Authorization':f"Bearer {LOGIN_TOKEN}"}
    response = requests.post(URL+'/arpost/edit', headers=headers, files={"file":("test.png", open("test.png","rb").read())}, data={'arpost_id':'1', 'arpost_name':'제목1234', 'arpost_contents':'내용123', 'x_value':'123', 'y_value':'456', 'z_value':'789', 'tag1':'asdfasdf'}) #tag1, tag2, tag3 is optional
    print(f"/arpost/edit api test : {response.text}")

def delete_arpost():
    # json
    headers = {'Authorization':f"Bearer {LOGIN_TOKEN}"}
    response = requests.post(URL+'/arpost/delete', headers=headers, data=json.dumps({'arpost_id':'18'}))
    print(f"/arpost/delete api test : {response.text}")

def get_around_arposts():
    # json
    headers = {'Authorization':f"Bearer {LOGIN_TOKEN}"}
    response = requests.post(URL+'/arpost/get_around_posts', headers=headers, data=json.dumps({'x_value':'18.123', 'y_value':'18.123'}))
    print(f"/arpost/get_around_posts api test : {response.text}")

def add_emotion_arpost(): # [':슬픔:', ':놀람:', ':웃김:', ':따봉:', ':하트:']
    # json
    headers = {'Authorization':f"Bearer {LOGIN_TOKEN}"}
    response = requests.post(URL+'/arpost/emotion/add', headers=headers, data=json.dumps({'arpost_id':2, 'emotion':':슬픔:'}))
    print(f"/arpost/emotion/add api test : {response.text}")

def delete_emotion_arpost():
    # json
    headers = {'Authorization':f"Bearer {LOGIN_TOKEN}"}
    response = requests.post(URL+'/arpost/emotion/delete', headers=headers, data=json.dumps({'arpost_id':2}))
    print(f"/arpost/emotion/delete api test : {response.text}")

def add_comment_arpost():
    # json
    headers = {'Authorization':f"Bearer {LOGIN_TOKEN}"}
    response = requests.post(URL+'/arpost/comment/add', headers=headers, data=json.dumps({'arpost_id':2, 'comment':'댓글을 달아봅시다.3'}))
    print(f"/arpost/comment/add api test : {response.text}")

def edit_comment_arpost():
    # json
    headers = {'Authorization':f"Bearer {LOGIN_TOKEN}"}
    response = requests.post(URL+'/arpost/comment/edit', headers=headers, data=json.dumps({'arpost_id':2, 'comment_id':'5', 'comment':'댓글을 달아봅시다.3333'}))
    print(f"/arpost/comment/edit api test : {response.text}")

def delete_comment_arpost():
    # json
    headers = {'Authorization':f"Bearer {LOGIN_TOKEN}"}
    response = requests.post(URL+'/arpost/comment/delete', headers=headers, data=json.dumps({'arpost_id':1, 'comment_id':2}))
    print(f"/arpost/comment/delete api test : {response.text}")

if __name__ == "__main__":
    #register()
    login()
    #create_arpost()
    #read_arpost()
    #edit_arpost()
    #delete_arpost()
    #get_around_arposts()
    #add_emotion_arpost()
    #delete_emotion_arpost()
    #add_comment_arpost()
    #edit_comment_arpost()
    #delete_comment_arpost()