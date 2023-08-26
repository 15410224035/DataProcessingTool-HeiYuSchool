import os

from PySide2.QtWidgets import QMessageBox, QMdiSubWindow, QTableWidgetItem, QFileDialog, QTreeWidget, QTreeWidgetItem
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt
from lib.share import SI
from lib.api import apimgr

from openpyxl import load_workbook
from lib.Commonly import create_username



import json


class ImportAccountWin:

    def __init__(self):

        # 先创建子窗口对象
        subWindow = QMdiSubWindow()
        # subWindow.setWindowTitle("配置连接参数")
        # 从ui定义文件中加载子窗口界面
        self.ui = QUiLoader().load('ui\import.ui')
        subWindow.setWidget(self.ui)
        subWindow.setAttribute(Qt.WA_DeleteOnClose)

        # 把子窗口加入到 MDI 区域
        SI.mainWin.ui.mdiArea.addSubWindow(subWindow)
        # 显示子窗口
        subWindow.show()
        # 子窗口提到最上层，并且最大化
        subWindow.setWindowState(Qt.WindowActive | Qt.WindowMaximized)
        #清除日志
        self.ui.pushButton_clear.clicked.connect(self.clear)
        # 导入文件
        try:
            self.ui.pushButton_SelectFile.clicked.connect(self.open_file)
        except Exception as e:
            QMessageBox.warning(
                self.ui,
                '有异常',
                e)
        #产生账号
        self.ui.pushButton_CreateAccount.clicked.connect(self.create_account)
        #向系统添加用户
        self.ui.pushButton_Import.clicked.connect(self.import_user)
        #撤销导入
        self.ui.pushButton_Revocation.clicked.connect(self.revocation)


    def clear(self):
        self.ui.textBrowser.clear()

    def open_file(self):
        file_name, file_type = QFileDialog.getOpenFileNames(self.ui,'选取文件',os.getcwd(),
                                                           "All Files(*);;Text Files(*.txt)")
        file = load_workbook(file_name[0])
        sheets_name = file.get_sheet_names()
        i=0
        for sheet_name in sheets_name:
            sheet = file[sheet_name]
            cells = sheet['A']
            for cell in cells[1:]:
                self.ui.tableWidget.insertRow(i)

                item = QTableWidgetItem(cell.value)
                # item.setFlags(Qt.ItemIsEnabled)  # 参数名字段不允许修改
                self.ui.tableWidget.setItem(i, 1, item)

                item = QTableWidgetItem(sheet_name)
                # item.setFlags(Qt.ItemIsEnabled)  # 参数名字段不允许修改
                self.ui.tableWidget.setItem(i, 0, item)

                i += 1

        # QFileDialog.getOpenFileNames()

    def create_account(self):
        user_names = []
        rowcount = self.ui.tableWidget.rowCount()
        for row in range(rowcount):
            name = self.ui.tableWidget.item(row, 1).text()
            username = create_username(name,user_names)

            item = QTableWidgetItem(username)
            self.ui.tableWidget.setItem(row, 2, item)

    def import_user(self):
        rowcount = self.ui.tableWidget.rowCount()
        for row in range(rowcount):
            classname = self.ui.tableWidget.item(row, 0).text()
            realname = self.ui.tableWidget.item(row, 1).text()
            username = self.ui.tableWidget.item(row, 2).text()

            response = apimgr.add_account(realname,username,'111111',classname,[1,],[21,])
            self.print_log(response)
            jsonBody = response.json()
            if jsonBody['ret'] == 0:
                item = QTableWidgetItem(str(jsonBody['id']))
                self.ui.tableWidget.setItem(row, 3, item)
            # else:
            #     QMessageBox.warning(
            #         self.ui,
            #         f'导入账号(名字：{realname})失败！',
            #         jsonBody['msg'])
            #     return



    def revocation(self):
        rowcount = self.ui.tableWidget.rowCount()
        for row in range(rowcount):
            userid = self.ui.tableWidget.item(row, 3).text()
            response = apimgr.delete_account(userid)
            self.print_log(response)
            jsonBody = response.json()
            if jsonBody['ret'] == 0:
                item = QTableWidgetItem('')
                self.ui.tableWidget.setItem(row, 3, item)
            # else:
            #     QMessageBox.warning(
            #         self.ui,
            #         f'撤销账号（id：{userid}）失败！',
            #         jsonBody['msg'])
            #     return



    def print_log(self,response):
        self.ui.textBrowser.append('\n\n-------- HTTP response * begin -------')
        self.ui.textBrowser.ensureCursorVisible()
        self.ui.textBrowser.append(str(response.status_code))  # 打印状态码
        self.ui.textBrowser.ensureCursorVisible()

        # 打印消息头
        for k, v in response.headers.items():
            self.ui.textBrowser.append(f'{k}: {v}')
            self.ui.textBrowser.ensureCursorVisible()

        self.ui.textBrowser.append('')
        self.ui.textBrowser.ensureCursorVisible()

        body = response.content.decode('utf8')  # 获取消息体的二进制内容，并解码
        self.ui.textBrowser.append(body)
        self.ui.textBrowser.ensureCursorVisible()

        # 判断返回消息体是否是json格式,并打印
        try:
            jsonBody = response.json()
            self.ui.textBrowser.append(f'\n\n---- 消息体json ----\n')
            self.ui.textBrowser.ensureCursorVisible()
            self.ui.textBrowser.append(json.dumps(jsonBody))
            self.ui.textBrowser.ensureCursorVisible()
        except:
            self.ui.textBrowser.append('消息体不是json格式！！')
            self.ui.textBrowser.ensureCursorVisible()

        self.ui.textBrowser.append('-------- HTTP response * end -------\n\n')
        self.ui.textBrowser.ensureCursorVisible()