from cfg.ConnectionParameters import ConnectionParameters
import pymysql

class SqlData:
    def __init__(self):
        # 创建一个 Connection 对象，代表了一个数据库连接
        self.connection = pymysql.connect(
            host=ConnectionParameters["数据库服务地址"],  # 数据库IP地址
            user=ConnectionParameters["数据库连接账号"],  # mysql用户名
            passwd="sdfsdf",  # mysql用户登录密码
            db="hylearn",  # 数据库名
            # 如果数据库里面的文本是utf8编码的，
            # charset指定是utf8
            charset="utf8")
        # self.connection = pymysql.connect(**mysqlData)
        # 返回一个 Cursor对象
        self.c = self.connection.cursor()



    def close(self):
        self.connection.close()  # 关闭数据库连接

    def insert_video(self,name,url,author_id):
        sql_statement = f"INSERT INTO `hylearn`.`by_video` (`name`, `url`, `author_id`) VALUES ('{name}', '{url}', '{author_id}');"
        print(sql_statement)
        self.c.execute(sql_statement)
        self.connection.commit()

    def insert_lesson(self,pubdate,title,content,coverimage,status='1',thumbupcount='0',favorcount='0',price='0',purchasecount='0',
                      approved='1',videos=None,usage='1',courses='',author_id='1'):
        '''

        :param pubdate: 发布日期
        :param title: 标题
        :param content:内容
        :param coverimage:封面图片
        :param status:表示状态，取值含义为 1-发布 2-草稿 3-封禁 ，此处固定填写 1 即可
        :param thumbupcount:点赞数
        :param favorcount:收藏数
        :param price:价格
        :param purchasecount:购买数量
        :param approved:表示批准状态 ，取值含义为 0-待批准， 1-批准， 2-待修改 ，此处固定填写 1 即可
        :param videos:格式是如下的json格式，记录了该课程包含的视频信息，、
                        [{"id": 8, "name": "xpath1"}, {"id": 9, "name": "xpath2"}, {"id": 10, "name": "xpath3"}]
        :param usage:表示课程是否可以单独出现，还是只能出现在专辑中 1: 可以单独 0：不可以单独 ，此处固定填写 1 即可。
        :param courses:所属课程
        :param author_id:作者id
        :return:
        '''
        sql_statement = f"INSERT INTO `hylearn`.`by_lesson` \
        (`pubdate`, `title`, `content`, `coverimage`, `status`, `thumbupcount`, `favorcount`, `price`, `purchasecount`, \
        `approved`, `videos`, `usage`, `courses`, `author_id`) VALUES ('{pubdate}', '{title}',\
         '{pymysql.converters.escape_string(content)}', '{coverimage}', '{status}', '{thumbupcount}', '{favorcount}', \
         '{price}', '{purchasecount}', '{approved}', '{videos}', '{usage}','{courses}', '{author_id}');"

        print(sql_statement)
        self.c.execute(sql_statement)
        self.connection.commit()

    def select_video(self):
        sql_statement = f"SELECT * FROM `hylearn`.`by_video` ORDER BY `id` DESC, `name` ASC, `url` ASC LIMIT 1000;"
        print(sql_statement)
        self.c.execute(sql_statement)
        self.connection.commit()
        row = self.c.fetchall()

        return row

    def insert_by_category(self,text,pid=0):
        '''
        在分类数据表中插入节点信息
        :param text: 节点名称
        :param pid: 父节点id
        :return:
        '''
        sql_statement = f"INSERT INTO `hylearn`.`by_category` ( `text`, `pid`) VALUES ( '{text}', '{pid}');"
        print(sql_statement)
        self.c.execute(sql_statement)
        self.connection.commit()
        last_id = self.c.lastrowid

        return last_id

    def select_by_category(self):
        '''
        查询by_category表的数据
        :return:
        '''
        sql_statement = f"SELECT * FROM `hylearn`.`by_category` ORDER BY `id` DESC LIMIT 1000;"
        print(sql_statement)
        self.c.execute(sql_statement)
        self.connection.commit()
        row = self.c.fetchall()

        return row

    def clear_by_category(self):
        '''
        清除by_category表所有数据
        :return:
        '''
        sql_statement = f"DELETE FROM `hylearn`.`by_category` WHERE  `id`>=0;"
        print(sql_statement)
        self.c.execute(sql_statement)
        self.connection.commit()

    def select_by_purchase_record(self,start_time, end_time):
        '''
        查询by_category表的数据，根据日期区间筛选
        :param start_time: 要查询的开始日期
        :param end_time: 要查询的结束日期
        :return:
        '''
        sql_statement = f"SELECT * FROM `hylearn`.`by_purchase_record` WHERE DATE_FORMAT(paiddatetime,'%Y%m%d') BETWEEN '{start_time}' AND '{end_time}';"
        print(sql_statement)
        self.c.execute(sql_statement)
        self.connection.commit()
        row = self.c.fetchall()

        return row,sql_statement


