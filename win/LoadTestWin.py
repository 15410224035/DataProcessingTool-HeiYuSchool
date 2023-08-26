import json
import random
import uuid
from queue import Queue

from PySide2.QtWidgets import QMdiSubWindow, QTreeWidgetItem
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from lib.share import SI
from lib.sql import sqldata



class LoadTestWin:

    def __init__(self):

        # 先创建子窗口对象
        subWindow = QMdiSubWindow()
        # subWindow.setWindowTitle("配置连接参数")
        # 从ui定义文件中加载子窗口界面
        self.ui = QUiLoader().load(r'ui\actionloadtest.ui')
        subWindow.setWidget(self.ui)
        subWindow.setAttribute(Qt.WA_DeleteOnClose)

        # 把子窗口加入到 MDI 区域
        SI.mainWin.ui.mdiArea.addSubWindow(subWindow)
        # 显示子窗口
        subWindow.show()
        # 子窗口提到最上层，并且最大化
        subWindow.setWindowState(Qt.WindowActive | Qt.WindowMaximized)
        #分类的数据
        self.treedata = []
        with open(r'.\cfg\tree.josn','r',encoding='utf8') as f:
            self.treedata = json.loads(f.read())

        # 隐藏标头栏
        self.ui.treeWidget.setHeaderHidden(True)
        # 获取树控件的不可见根节点
        root = self.ui.treeWidget.invisibleRootItem()
        # 创建图标对象
        self.folderIcon = QIcon("./images/文件夹.png")
        #创建树
        self.create_tree(self.ui.treeWidget, self.treedata, root, self.folderIcon)
        #清除树
        self.ui.action_del.triggered.connect(self.cleartree)
        #添加子节点
        self.ui.actionaddChildNode.triggered.connect(self.action_addChildNode)
        # 添加兄弟节点
        self.ui.actionaddBrotherNode.triggered.connect(self.action_addBrotherNode)
        #树控件被改变，更新josn文件
        self.ui.treeWidget.itemChanged.connect(self.itemChanged1)
        #推送到数据库
        self.ui.action_save.triggered.connect(self.action_save)






    def cleartree(self):
        self.ui.treeWidget.clear()

    # 递归调用函数，完成整个树的遍历
    def iterateFunc(self,parent, dataTree):
        #子节点个数
        child_count = parent.childCount()
        for i in range(child_count):
            item = parent.child(i)

            # 保存这个节点item的信息到字典对象中
            subDictNode = {}
            dataTree.append(subDictNode)
            subDictNode['tit'] = item.text(0)
            subDictNode['children'] = []

            # 对该子节点递归调用遍历处理函数
            self.iterateFunc(item, subDictNode['children'])





    def create_tree(self,tree, treedata, treeItem, folderIcon):
        '''
        定义生成树的函数
        :param tree: ui中的树对象
        :param treedata: 定义树的josn数据
        :param treeItem: 节点对象
        :param folderIcon: 节点图标
        :return:
        '''
        for node in treedata:
            # 准备一个folder节点
            folderItem = QTreeWidgetItem()
            # 设置节点图标
            folderItem.setIcon(0, folderIcon)
            # 设置该节点  第1个column 文本
            folderItem.setText(0, node['tit'])
            # 添加到树的不可见根节点下，就成为第一层节点
            treeItem.addChild(folderItem)
            # 设置该节点为展开状态
            folderItem.setExpanded(True)
            # 设置该节点在以前的flag基础上，多一个可编辑 ItemIsEditable
            folderItem.setFlags(folderItem.flags() | Qt.ItemIsEditable)

            if node['children']:
                self.create_tree(tree, node['children'], folderItem, folderIcon)

    def action_addChildNode(self):
        #获取当前节点
        # 获取当前用户点选的节点
        currentItem = self.ui.treeWidget.currentItem()
        # 没有当前选中节点，不可见根节点作为当前节点
        if not currentItem:
            currentItem = self.ui.treeWidget.invisibleRootItem()

        # # 获取当前节点的父节点
        # parentItem = currentItem.parent()
        # # 如果返回值为None，其必定为顶层节点，它的父节点是不可见的根节点
        # if not parentItem:
        #     parentItem = self.ui.treeWidget.invisibleRootItem()

        # 准备一个folder节点
        folderItem = QTreeWidgetItem()
        # 设置节点图标
        folderItem.setIcon(0, self.folderIcon)
        # 设置该节点  第1个column 文本
        folderItem.setText(0, '新节点')
        # 添加到树的不可见根节点下，就成为第一层节点
        currentItem.addChild(folderItem)
        # 设置该节点为展开状态
        folderItem.setExpanded(True)
        # 设置该节点在以前的flag基础上，多一个可编辑 ItemIsEditable
        folderItem.setFlags(folderItem.flags() | Qt.ItemIsEditable)

    def action_addBrotherNode(self):
        #获取当前节点
        # 获取当前用户点选的节点
        currentItem = self.ui.treeWidget.currentItem()
        # 没有当前选中节点，不可见根节点作为当前节点
        if not currentItem:
            currentItem = self.ui.treeWidget.invisibleRootItem()

        # 获取当前节点的父节点
        parentItem = currentItem.parent()
        # 如果返回值为None，其必定为顶层节点，它的父节点是不可见的根节点
        if not parentItem:
            parentItem = self.ui.treeWidget.invisibleRootItem()

        # 准备一个folder节点
        folderItem = QTreeWidgetItem()
        # 设置节点图标
        folderItem.setIcon(0, self.folderIcon)
        # 设置该节点  第1个column 文本
        folderItem.setText(0, '新节点')
        # 添加到树的不可见根节点下，就成为第一层节点
        parentItem.addChild(folderItem)
        # 设置该节点为展开状态
        folderItem.setExpanded(True)
        # 设置该节点在以前的flag基础上，多一个可编辑 ItemIsEditable
        folderItem.setFlags(folderItem.flags() | Qt.ItemIsEditable)

    def create_graph(self):
        '''
        将现在的树，转化为图（以字典表示）
        :return: 返回图
        '''

        # 递归调用函数，完成整个树的遍历
        def iterateFunc(parent, parentppid, graph, titdic):
            # 定义一个数组，用来保存parent节点的子节点
            childs = []
            # 子节点个数
            child_count = parent.childCount()
            for i in range(child_count):
                item = parent.child(i)
                itemid = str(uuid.uuid1())
                titdic[itemid] = item.text(0)
                childs.append(itemid)

                # 对该子节点递归调用遍历处理函数
                iterateFunc(item,itemid, graph, titdic)
            graph[parentppid] = childs

        graph = {} #图
        # 为了防止节点标题重复，建一个字典，生产id与名字对应
        titdic = {}


        # 获取不可见根节点
        root = self.ui.treeWidget.invisibleRootItem()
        # 为了节点名字不重复，生产一个随机数
        randomstr = str(random.randint(183884748, 1838847488))
        rootname = f'不可见的根节点{randomstr}'
        rootppid = str(uuid.uuid1())
        titdic[rootppid] = rootname
        iterateFunc(root,rootppid, graph, titdic)

        return graph,rootppid,titdic

    def itemChanged1(self, item, column):
        # 获取不可见根节点
        root = self.ui.treeWidget.invisibleRootItem()
        # 用嵌套列表来对应树的数据结构，方便保存到文件
        dataTree = []
        self.iterateFunc(root, dataTree)

        # 序列化到json文件，保存
        jsonStr = json.dumps(dataTree, ensure_ascii=False, indent=2)
        with open(r'.\cfg\tree.josn', 'w', encoding='utf8') as f:
            f.write(jsonStr)

    def action_save(self):
        def BFS_Algorithm(input_graph, rootppid, titdic):

            Q = Queue()

            visited_vertices = list()
            for q in input_graph[rootppid]:
                Q.put({q:0})
            while not Q.empty():
                vertex = Q.get()
                pid = sqldata.insert_by_category(titdic[list(vertex.keys())[0]], list(vertex.values())[0])
                # if list(vertex.values())[0] == 0:
                #     sqldata.insert_by_category(list(vertex.keys())[0])
                # else:
                #     row = sqldata.select_by_category()
                #     for line in row:
                #         if list(vertex.values())[0] in line:
                #             pid = line[0]
                #             sqldata.insert_by_category(list(vertex.keys())[0], pid)
                #     print(row)
                for u in input_graph[list(vertex.keys())[0]]:
                    if u not in visited_vertices:

                        Q.put({u:pid})
                        visited_vertices.append({u:pid})


        #先清空数据库by_category中的数据
        sqldata.clear_by_category()

        # 获取不可见根节点
        root = self.ui.treeWidget.invisibleRootItem()
        graph,rootppid,titdic = self.create_graph()
        BFS_Algorithm(graph, rootppid, titdic)








