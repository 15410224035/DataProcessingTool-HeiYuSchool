
import requests
from pprint import  pprint
from lib.share import SI
from cfg.ConnectionParameters import ConnectionParameters
import json


class APIMgr:
    # 返回消息打印函数
    def _printResponse(self,response):
        print('\n\n-------- HTTP response * begin -------')
        print(response.status_code)#打印状态码

        # 打印消息头
        for k,v in response.headers.items():
            print(f'{k}: {v}')

        print('')

        body = response.content.decode('utf8')#获取消息体的二进制内容，并解码
        print(body)

        # 判断返回消息体是否是json格式,并打印
        try:
            jsonBody = response.json()
            print(f'\n\n---- 消息体json ----\n'  )
            pprint(jsonBody)
        except:
            print('消息体不是json格式！！')

        print('-------- HTTP response * end -------\n\n')

# ------------调用接口函数--------------------------------------------------------------


    def login(self,username, password):
        '''
        apid登录
        :param username:
        :param password:
        :return: response
        '''
        self.session = requests.Session()
        url = f"http://{ConnectionParameters['web服务地址']}/api/sign"

        res = self.session.post(url, json={
            "action": "signin",
            "username": username,
            "password": password
        })

        self._printResponse(res)
        return res

    def onSignOut(self):
        '''
        apid登出
        :return: response
        '''
        url = f"http://{ConnectionParameters['web服务地址']}/api/sign"

        res = self.session.post(url, json={
            "action": "signout",
        })

        self._printResponse(res)
        return res

    def add_account(self,realname, username, password, desc, usergroup = None, permission = None):
        '''
        :param realname:用户的姓名
        :param username:用户的登录名
        :param password:用户的密码
        :param desc:账号描述信息
        :param usergroup:可选项，以数组的方式指定 该用户所属的用户组对应的id。 目前创作者 组id 固定为1， 创造管理 组id 固定为2
        :param permission:可选项，以数组的方式指定 该用户所拥有权限 对应的id
        :return:response:接口返回消息
        '''
        url = f"http://{ConnectionParameters['web服务地址']}/api/account"
        payload = {
                  "action": "addone",
                  "data": {
                    "realname" : realname,
                    "username" : username,
                    "password" : password,
                    "desc"     : desc,
                    "usergroup": usergroup,
                    "permission":permission
                  }
                    }

        response = self.session.post(
            url,
            # headers={
            #     'Content-Type': 'application/x-www-form-urlencoded'
            # },
            json=payload
        )
        self._printResponse(response)
        return response

    def delete_account(self,id):
        '''

        :param id: 用户唯一id
        :return: response:接口返回消息
        '''
        url = f"http://{ConnectionParameters['web服务地址']}/api/account"
        payload = {
                  "action": "deleteone",
                  "id": id
                }

        response = self.session.delete(
            url,
            json=payload
        )
        self._printResponse(response)
        return response

apimgr=APIMgr()
# apimgr.login('byhy','sdfsdf')
# apimgr.add_account("紫一元","ziyiyuan","111111","白月黑羽的优秀学员",[1,],[21,])
# apimgr.delete_account('205')
# for i in range(211,308):
#     apimgr.delete_account(str(i))