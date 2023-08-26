import os

from PySide2.QtWidgets import QMessageBox, QMdiSubWindow, QTableWidgetItem, QFileDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt
from lib.share import SI
from datetime import datetime
import lib.sql


import json


class ImportCourseWin:

    def __init__(self):

        # 先创建子窗口对象
        subWindow = QMdiSubWindow()
        # subWindow.setWindowTitle("配置连接参数")
        # 从ui定义文件中加载子窗口界面
        self.ui = QUiLoader().load('ui\import_course.ui')
        subWindow.setWidget(self.ui)
        subWindow.setAttribute(Qt.WA_DeleteOnClose)

        # 把子窗口加入到 MDI 区域
        SI.mainWin.ui.mdiArea.addSubWindow(subWindow)
        # 显示子窗口
        subWindow.show()
        # 子窗口提到最上层，并且最大化
        subWindow.setWindowState(Qt.WindowActive | Qt.WindowMaximized)
        #设置表格随窗口变动
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        #清除日志
        self.ui.pushButton_clear.clicked.connect(self.clear)
        # 导入文件
        try:
            self.ui.pushButton_ChooseDir.clicked.connect(self.open_file)
        except Exception as e:
            QMessageBox.warning(
                self.ui,
                '有异常',
                str(e))

        #向系统添加用户
        self.ui.pushButton_Import.clicked.connect(self.import_course)



    def clear(self):
        self.ui.textBrowser.clear()

    def open_file(self):
        # file_name, file_type = QFileDialog.getOpenFileNames(self.ui,'选取文件',os.getcwd(),
        # getExistingDirectory(                                                   "All Files(*);;Text Files(*.txt)")
        targetDir = QFileDialog.getExistingDirectory()

        self.files = []
        for (dirpath, dirnames, filenames) in os.walk(targetDir):
            for fn in filenames:
                # 把 dirpath 和 每个文件名拼接起来 就是全路径
                fpath = os.path.join(dirpath, fn)
                if fpath[-3:] == 'txt': self.files += [fpath]

        for row, file in enumerate(self.files):
            self.ui.tableWidget.insertRow(row)
            with open(file,'r',encoding='utf8') as f:
                lines = [l for l in f.readlines() if l != '\n'][:5]
                for column, line in enumerate(lines):
                    item = QTableWidgetItem(line.split('=')[-1].strip())
                    self.ui.tableWidget.setItem(row, column, item)



    def import_course(self):
        sqldata = lib.sql.SqlData()
        for row, file in enumerate(self.files):
            with open(file, 'r', encoding='utf8') as f:
                lines = [l for l in f.readlines() if l != '\n']
                parameters = []
                # content = re.split(r'-+',f.read())[-1]
                content = ''.join(lines[6:])
                parameters.append(content)
                lines = lines[:5]
                for column, line in enumerate(lines):
                    item = line.split('=')[-1].strip()
                    parameters.append(item)

                try:
                    videos = parameters[3].split(',')
                    videos_list = []
                    for video in videos:
                        video_name = video.split('\\')[-1].split('.')[0]
                        videos_list.append(video_name)
                        video_url = video
                        sqldata.insert_video(video_name, video_url, '1')
                        self.ui.textBrowser.append(f'\n{parameters[1]}课程的视频：{video_name}导入成功\n')
                        self.ui.textBrowser.ensureCursorVisible()

                    videodatas = sqldata.select_video()
                    parameter_video = []
                    for videodata in videodatas:
                        for video_name in videos_list:
                            video_dic = {}
                            if video_name in videodata:
                                video_dic[videodata[0]] = video_name
                                parameter_video.append(video_dic)

                    sqldata.insert_lesson(str(datetime.now()), parameters[1], parameters[0], parameters[2],
                                            '1', '0', '0', parameters[5], '0', '1',json.dumps(parameter_video) , '1', '', '1')
                    # sqldata.insert_lesson(str(datetime.now()), parameters[1], 'neirong', parameters[2],
                    #                       '1', '0', '0', parameters[5], '0', '1', json.dumps(parameter_video), '1', '',
                    #                       '1')
                    self.ui.textBrowser.append(f'\n【{parameters[1]}课程导入成功】\n')
                    self.ui.textBrowser.ensureCursorVisible()



                except Exception as e:
                    self.ui.textBrowser.append(str(e))
                    self.ui.textBrowser.ensureCursorVisible()








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