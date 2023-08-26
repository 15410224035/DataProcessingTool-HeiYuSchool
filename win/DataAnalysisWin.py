
from PySide2.QtWidgets import QMdiSubWindow
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt
import pyqtgraph as pg
from decimal import Decimal
import time
from lib.share import SI
from lib.sql import sqldata



class DataAnalysisWin:

    def __init__(self):

        # 先创建子窗口对象
        subWindow = QMdiSubWindow()
        # subWindow.setWindowTitle("配置连接参数")
        # 从ui定义文件中加载子窗口界面
        loader = QUiLoader()
        # pyside2 一定要 使用registerCustomWidget
        # 来注册 ui文件中的第三方控件，这样加载的时候
        # loader才知道第三方控件对应的类，才能实例化对象
        loader.registerCustomWidget(pg.PlotWidget)
        self.ui = loader.load(r'ui\data_analysis.ui')
        # self.ui = QUiLoader().load(r'ui\data_analysis.ui')
        subWindow.setWidget(self.ui)
        subWindow.setAttribute(Qt.WA_DeleteOnClose)

        # 把子窗口加入到 MDI 区域
        SI.mainWin.ui.mdiArea.addSubWindow(subWindow)
        # 显示子窗口
        subWindow.show()
        # 子窗口提到最上层，并且最大化
        subWindow.setWindowState(Qt.WindowActive | Qt.WindowMaximized)

        #按钮“分析”
        self.ui.pushButton_analysis.clicked.connect(self.data_analysis)
        # 按钮“清除log”
        self.ui.pushButton_clear.clicked.connect(self.clear)







    def clear(self):
        '''
        清除日志
        :return:
        '''
        self.ui.textBrowser.clear()

    def data_analysis(self):
        self.star_time = time.strptime(self.ui.dateEdit_start.text(), "%Y/%m/%d")
        self.star_time = ''.join(time.strftime("%Y/%m/%d", self.star_time).split('/'))

        self.end_time = time.strptime(self.ui.dateEdit_end.text(), "%Y/%m/%d")
        self.end_time = ''.join(time.strftime("%Y/%m/%d", self.end_time).split('/'))

        #通过sql查询数据
        data, sql_statement = sqldata.select_by_purchase_record(self.star_time, self.end_time)
        # 订单数量
        order_quantity = len(data)
        #订单总金额
        order_money = Decimal('0')
        #日期和订单数量——折线图数据
        data_trend = {}
        for i in data:
            order_money += i[4]
            if i[5].date() in data_trend:
                data_trend[i[5].date()] += 1
            else:
                data_trend[i[5].date()] = 1



        #打日志
        self.ui.textBrowser.append(f'\n\n-------- 开始查询{self.star_time}到{self.end_time}的数据 -------')
        self.ui.textBrowser.ensureCursorVisible()
        self.ui.textBrowser.append(f'\nsql语句：{sql_statement}')
        self.ui.textBrowser.ensureCursorVisible()
        self.ui.textBrowser.append(f'\n共查询到{order_quantity}条数据')
        self.ui.textBrowser.ensureCursorVisible()



        #画折线图
        # 设置图表标题
        self.ui.historyPlot_trend.setTitle(f"{self.star_time}到{self.end_time} 订单数：{order_quantity} 金额：{str(order_money)}", size='12pt')

        # 设置上下左右的label
        self.ui.historyPlot_trend.setLabel("left", "订单数量（条）")
        self.ui.historyPlot_trend.setLabel("bottom", "日期")
        # 背景色改为白色
        self.ui.historyPlot_trend.setBackground('w')

        # 创建 PlotDataItem ，缺省是曲线图
        curve = self.ui.historyPlot_trend.plot(pen=pg.mkPen('r'))  # 线条颜色

        hour = list(data_trend.keys())
        temperature = list(data_trend.values())

        curve.setData(hour,  # x坐标
                      temperature  # y坐标
                      )


















