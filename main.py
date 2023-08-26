from PySide2.QtWidgets import QApplication, QMessageBox, QMdiSubWindow, QTableWidgetItem, QTreeWidgetItem
from requests.exceptions import ConnectionError, ConnectTimeout
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon


from win.ImportAccountWin import ImportAccountWin
from win.ImportCourseWin import ImportCourseWin
from win.LoadTestWin import LoadTestWin
from win.DataAnalysisWin import DataAnalysisWin

from lib.share import SI
from lib.api import apimgr
from cfg.ConnectionParameters import ConnectionParameters


class WinLogin:

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load(r'.\ui\login.ui')




        # self.ui.Button_quit.clicked.connect(self.MainQuit1)#退出
        self.ui.Button_login.clicked.connect(self.login) #登录按钮
        self.ui.lineEdit_password.returnPressed.connect(self.login)



    # 定义读取数据库按钮函数reade
    def login(self):
        username = self.ui.lineEdit_username.text().strip()
        password = self.ui.lineEdit_password.text().strip()
        try:
            res = apimgr.login(username, password)
            resObj = res.json()
            if resObj['ret'] != 0:
                QMessageBox.warning(
                    self.ui,
                    '登录失败',
                    resObj['msg'])
                return

        except (ConnectionError, ConnectTimeout):
            QMessageBox.warning(
                self.ui,
                '登录失败',
                '连接错误，请检查网络！')
            return



        SI.mainWin= Mainwin()

        SI.mainWin.ui.show()

        self.ui.lineEdit_password.setText('')
        self.ui.hide()




class Mainwin:
    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load(r'.\ui\main.ui')
        # 登出
        self.ui.actionexit.triggered.connect(self.onSignOut)
        # 连接参数配置
        self.ui.actionconnectset.triggered.connect(self.openocc_bottle)
        # 点击导入导出
        self.ui.actionImportAndExport.triggered.connect(self.action_ImportAndExport)
        # 点击压力测试
        self.ui.actionloadtest.triggered.connect(self.action_loadtest)
        # 点击数据分析
        self.ui.action_data_analysis.triggered.connect(self.action_data_analysis)
        # 树被点击
        self.ui.treeWidget.itemClicked.connect(self.itemClicked1)
        # 清除按钮
        # self.ui.mdiArea.pushButton_clear.clicked.connect(self.clear)

    # 点击压力测试，生成树
    def action_loadtest(self):
        self.ui.treeWidget.clear()
        # 获取树控件对象
        tree = self.ui.treeWidget

        # 隐藏标头栏
        tree.setHeaderHidden(True)

        # 获取树控件的不可见根节点
        root = tree.invisibleRootItem()

        # 准备一个folder节点
        folderItem0 = QTreeWidgetItem()
        folderItem1 = QTreeWidgetItem()
        # 创建图标对象
        folderIcon = QIcon("./images/文件夹.png")
        # 设置节点图标
        folderItem0.setIcon(0, folderIcon)
        folderItem1.setIcon(0, folderIcon)
        # 设置该节点  第1个column 文本
        folderItem0.setText(0, '数据环境创建')
        folderItem1.setText(0, '数据环境清理')
        # 添加到树的不可见根节点下，就成为第一层节点
        root.addChild(folderItem0)
        root.addChild(folderItem1)
        # 设置该节点为展开状态
        folderItem0.setExpanded(True)
        folderItem1.setExpanded(True)

        # 准备一个 叶子 节点
        leafItem01 = QTreeWidgetItem()
        leafItem02 = QTreeWidgetItem()
        leafItem03 = QTreeWidgetItem()
        leafItem04 = QTreeWidgetItem()
        leafItem05 = QTreeWidgetItem()

        leafItem11 = QTreeWidgetItem()
        leafItem12 = QTreeWidgetItem()
        leafItem13 = QTreeWidgetItem()
        leafItem14 = QTreeWidgetItem()
        leafItem15 = QTreeWidgetItem()
        leafIcon = QIcon("./images/文件夹.png")
        # 设置节点图标
        leafItem01.setIcon(0, leafIcon)
        leafItem02.setIcon(0, leafIcon)
        leafItem03.setIcon(0, leafIcon)
        leafItem04.setIcon(0, leafIcon)
        leafItem05.setIcon(0, leafIcon)

        leafItem11.setIcon(0, leafIcon)
        leafItem12.setIcon(0, leafIcon)
        leafItem13.setIcon(0, leafIcon)
        leafItem14.setIcon(0, leafIcon)
        leafItem15.setIcon(0, leafIcon)
        # 设置该节点  第1个column 文本
        leafItem01.setText(0, '创建分类')
        leafItem02.setText(0, '创建标签')
        leafItem03.setText(0, '创建用户')
        leafItem04.setText(0, '创建课程、专辑')
        leafItem05.setText(0, '创建订单')

        leafItem11.setText(0, '重建数据库')
        leafItem12.setText(0, '导出课程')


        # # 设置该节点  第2个column 文本
        # leafItem.setText(1, '提交日期20200101')
        # 添加到 叶子节点 到 folerItem 目录节点下
        folderItem0.addChild(leafItem01)
        folderItem0.addChild(leafItem02)
        folderItem0.addChild(leafItem03)
        folderItem0.addChild(leafItem04)
        folderItem0.addChild(leafItem05)

        folderItem1.addChild(leafItem11)
        folderItem1.addChild(leafItem12)

        # 点击压力测试，生成树
    #点击数据分析，生成树
    def action_data_analysis(self):
        self.ui.treeWidget.clear()
        # 获取树控件对象
        tree = self.ui.treeWidget

        # 隐藏标头栏
        tree.setHeaderHidden(True)

        # 获取树控件的不可见根节点
        root = tree.invisibleRootItem()

        # 准备一个folder节点
        folderItem0 = QTreeWidgetItem()
        folderItem1 = QTreeWidgetItem()
        # 创建图标对象
        folderIcon = QIcon("./images/文件夹.png")
        # 设置节点图标
        folderItem0.setIcon(0, folderIcon)
        folderItem1.setIcon(0, folderIcon)
        # 设置该节点  第1个column 文本
        folderItem0.setText(0, '数据分析')
        folderItem1.setText(0, '其他')
        # 添加到树的不可见根节点下，就成为第一层节点
        root.addChild(folderItem0)
        root.addChild(folderItem1)
        # 设置该节点为展开状态
        folderItem0.setExpanded(True)
        folderItem1.setExpanded(True)

        # 准备一个 叶子 节点
        leafItem01 = QTreeWidgetItem()
        leafItem02 = QTreeWidgetItem()
        leafItem03 = QTreeWidgetItem()


        leafItem4 = QTreeWidgetItem()

        leafIcon = QIcon("./images/文件夹.png")
        # 设置节点图标
        leafItem01.setIcon(0, leafIcon)
        leafItem02.setIcon(0, leafIcon)
        leafItem03.setIcon(0, leafIcon)


        leafItem4.setIcon(0, leafIcon)

        # 设置该节点  第1个column 文本
        leafItem01.setText(0, '销量趋势')
        leafItem02.setText(0, '热门课程')
        leafItem03.setText(0, '热门分类')

        leafItem4.setText(0, '保险数据分析')


        # # 设置该节点  第2个column 文本
        # leafItem.setText(1, '提交日期20200101')
        # 添加到 叶子节点 到 folerItem 目录节点下
        folderItem0.addChild(leafItem01)
        folderItem0.addChild(leafItem02)
        folderItem0.addChild(leafItem03)

        folderItem1.addChild(leafItem4)


    # 点击导入导出，生成树
    def action_ImportAndExport(self):
        self.ui.treeWidget.clear()
        # 获取树控件对象
        tree = self.ui.treeWidget

        # 隐藏标头栏
        tree.setHeaderHidden(True)

        # 获取树控件的不可见根节点
        root = tree.invisibleRootItem()

        # 准备一个folder节点
        folderItem0 = QTreeWidgetItem()
        folderItem1 = QTreeWidgetItem()
        # 创建图标对象
        folderIcon = QIcon("./images/文件夹.png")
        # 设置节点图标
        folderItem0.setIcon(0, folderIcon)
        folderItem1.setIcon(0, folderIcon)
        # 设置该节点  第1个column 文本
        folderItem0.setText(0, '数据导入')
        folderItem1.setText(0, '数据导出')
        # 添加到树的不可见根节点下，就成为第一层节点
        root.addChild(folderItem0)
        root.addChild(folderItem1)
        # 设置该节点为展开状态
        folderItem0.setExpanded(True)
        folderItem1.setExpanded(True)

        # 准备一个 叶子 节点
        leafItem01 = QTreeWidgetItem()
        leafItem02 = QTreeWidgetItem()
        leafItem03 = QTreeWidgetItem()
        leafItem04 = QTreeWidgetItem()
        leafItem05 = QTreeWidgetItem()

        leafItem11 = QTreeWidgetItem()
        leafItem12 = QTreeWidgetItem()
        leafItem13 = QTreeWidgetItem()
        leafItem14 = QTreeWidgetItem()
        leafItem15 = QTreeWidgetItem()
        leafIcon = QIcon("./images/文件夹.png")
        # 设置节点图标
        leafItem01.setIcon(0, leafIcon)
        leafItem02.setIcon(0, leafIcon)
        leafItem03.setIcon(0, leafIcon)
        leafItem04.setIcon(0, leafIcon)
        leafItem05.setIcon(0, leafIcon)

        leafItem11.setIcon(0, leafIcon)
        leafItem12.setIcon(0, leafIcon)
        leafItem13.setIcon(0, leafIcon)
        leafItem14.setIcon(0, leafIcon)
        leafItem15.setIcon(0, leafIcon)
        # 设置该节点  第1个column 文本
        leafItem01.setText(0, '导入用户数据')
        leafItem02.setText(0, '导入课程')
        leafItem03.setText(0, '导入专辑')
        leafItem04.setText(0, '导入线下订单')
        leafItem05.setText(0, '导入分类标签')

        leafItem11.setText(0, '导出用户数据')
        leafItem12.setText(0, '导出课程')
        leafItem13.setText(0, '导出专辑')
        leafItem14.setText(0, '导出订单数据')
        leafItem15.setText(0, '导出分类标签')

        # # 设置该节点  第2个column 文本
        # leafItem.setText(1, '提交日期20200101')
        # 添加到 叶子节点 到 folerItem 目录节点下
        folderItem0.addChild(leafItem01)
        folderItem0.addChild(leafItem02)
        folderItem0.addChild(leafItem03)
        folderItem0.addChild(leafItem04)
        folderItem0.addChild(leafItem05)

        folderItem1.addChild(leafItem11)
        folderItem1.addChild(leafItem12)
        folderItem1.addChild(leafItem13)
        folderItem1.addChild(leafItem14)
        folderItem1.addChild(leafItem15)

    def itemClicked1(self, item, column):
        # 获取被点击的节点文本
        clickedText = item.text(column)

        if '导入用户数据' in clickedText:
            self.openocc_import_account()
        elif '导入课程' in clickedText:
            self.openocc_import_course()
        elif '创建分类' in clickedText:
            self.openocc_loadtest()
        elif '销量趋势' in clickedText:
            self.openocc_data_analysis()



    def onSignOut(self):
        SI.loginWin.ui.show()
        self.ui.hide()
        url = "http://192.168.56.103/api/sign"

        res = apimgr.onSignOut()

        resObj = res.json()
        if resObj['ret'] != 0:
            QMessageBox.warning(
                self.ui,
                '登出失败',
                resObj['msg'])
            return


    # 信号处理代码
    def openocc_bottle(self):
        # 先创建子窗口对象
        subWindow = QMdiSubWindow()
        # subWindow.setWindowTitle("配置连接参数")
        # 从ui定义文件中加载子窗口界面
        ConnectionParametersForm = QUiLoader().load('ui\ConnectionParameters.ui')
        SI.ConnectionParametersWin =ConnectionParametersForm
        subWindow.setWidget(ConnectionParametersForm)
        subWindow.setAttribute(Qt.WA_DeleteOnClose)

        # 把子窗口加入到 MDI 区域
        self.ui.mdiArea.addSubWindow(subWindow)
        # 显示子窗口
        subWindow.show()
        # 子窗口提到最上层，并且最大化
        subWindow.setWindowState(Qt.WindowActive | Qt.WindowMaximized)


        for i in range(5):
            row = ['web服务地址','web服务端口','数据库服务地址','数据库服务端口','数据库连接账号']
            ConnectionParametersForm.tableWidget.insertRow(i)
            item = QTableWidgetItem(row[i])
            item.setFlags(Qt.ItemIsEnabled)  # 参数名字段不允许修改
            ConnectionParametersForm.tableWidget.setItem(i, 0, item)

            item = QTableWidgetItem(ConnectionParameters[row[i]])
            item.setFlags(Qt.ItemIsEnabled)  # 参数名字段不允许修改
            ConnectionParametersForm.tableWidget.setItem(i, 1, item)

    # 打开导入用户数据界面
    def openocc_import_account(self):
        SI.ImportAccountWin=ImportAccountWin()

    # 打开导入课程数据界面
    def openocc_import_course(self):
        SI.ImportCourseWin = ImportCourseWin()

    # 打开导入课程数据界面
    def openocc_loadtest(self):
        SI.LoadTestWin = LoadTestWin()

    # 打开数据分析界面
    def openocc_data_analysis(self):
        SI.DataAnalysisWin = DataAnalysisWin()













app = QApplication([])


SI.loginWin = WinLogin()
SI.loginWin.ui.show()
app.exec_()