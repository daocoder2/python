# -*- coding: utf-8 -*-

import pymysql
import random

IP_CONFIG = {
    'MYSQL_HOST': '192.168.8.119',
    'MYSQL_PORT': 3306,
    'MYSQL_DBNAME': 'test',
    'MYSQL_USER': 'test',
    'MYSQL_PASSWD': 'test',
}
STORE_CONFIG = {
    'MYSQL_HOST': '192.168.8.234',
    'MYSQL_PORT': 3306,
    'MYSQL_DBNAME': 'docker',
    'MYSQL_USER': 'test',
    'MYSQL_PASSWD': 'test',
}

MYSQL_MIDDLEWARES = {
    'IP_CONFIG': IP_CONFIG,
    'STORE_CONFIG': STORE_CONFIG
}


class DbHelper(object):
    def __init__(self, config='IP_CONFIG'):
        self.settings = MYSQL_MIDDLEWARES[config]
        self.host = self.settings['MYSQL_HOST']
        self.port = self.settings['MYSQL_PORT']
        self.user = self.settings['MYSQL_USER']
        self.passwd = self.settings['MYSQL_PASSWD']
        self.db = self.settings['MYSQL_DBNAME']

    def connect(self):
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                               passwd=self.passwd, db=self.db, charset='utf8')
        cur = conn.cursor()
        return cur, conn

    def create_database(self):
        pass

    def create_table(self, sql):
        (cur, conn) = self.connect()
        res = cur.execute(sql)
        conn.close()
        return res

    def insert(self, sql, *params):
        (cur, conn) = self.connect()
        try:
            res = cur.execute(sql)
            conn.commit()
            return res
        except Exception as e:
            raise e
        finally:
            conn.close()

    def update(self, sql, *params):
        pass

    def delete(self, sql, *params):
        pass

    def get_one(self, sql):
        (cur, conn) = self.connect()
        try:
            cur.execute(sql)
            result = cur.fetchone()
            data_dict = []
            for field in cur.description:
                # print(field)
                data_dict.append(field[0])
            return result, data_dict
        except Exception as e:
            raise e
        finally:
            conn.close()

    def get_rows(self, sql):
        (cur, conn) = self.connect()
        try:
            cur.execute(sql)
            results = cur.fetchall()
            data_dict = []
            for field in cur.description:
                # print(field)
                data_dict.append(field[0])
            return results, data_dict
        except Exception as e:
            raise e
        finally:
            conn.close()

    def get_rows_arr(self, sql):
        (cur, conn) = self.connect()
        try:
            cur.execute(sql)
            results = cur.fetchall()
            data_list = []
            result_list = []
            res_dict = {}
            for field in cur.description:
                data_list.append(field[0])
            for row in results:
                for i in range(len(data_list)):
                    res_dict[data_list[i]] = row[i]
                    result_list.append(res_dict)
            return result_list
        except Exception as e:
            raise e
        finally:
            conn.close()


class TestDBHelper(object):
    def __init__(self, config='IP_CONFIG'):
        self.db_helper = DbHelper(config)

    def get_one(self, sql):
        (value, column) = self.db_helper.get_one(sql)
        ip = "http://%s:%s" % (value[1], value[5])
        print(value)
        print(column)
        print(ip)

    def get_rows(self, sql):
        (values, column) = self.db_helper.get_rows(sql)

    def get_rows_arr(self, sql):
        res = self.db_helper.get_rows_arr(sql)
        print(res)

    def create_table(self, sql):
        res = self.db_helper.create_table(sql)
        print(res)
        pass


if __name__ == "__main__":
    test_db_helper = TestDBHelper()
    # query_sql = "select * from `lft_proxy_ip` order by `time` desc"
    # test_db_helper.get_one(query_sql)
    query_sql = "select * from `lft_proxy_ip` order by `time` desc limit 10"
    test_db_helper.get_rows_arr(query_sql)

    # create_sql = """create table `xiaoqu` (
    #                  `id` int(11) auto_increment ,
    #                  `name` varchar(50) not null,
    #                  `alias` varchar(500) not null,
    #                  `detail_url` varchar(200) not null,
    #                  `quname` varchar(20) not null,
    #                  `tarea` varchar(20) not null,
    #                  `wuye_fee` varchar(10) not null,
    #                  `wuye_company` varchar(50) not null,
    #                  `builder` varchar(50) not null,
    #                  `address` varchar(50) not null,
    #                  `jianzhu_year` varchar(10) not null,
    #                  `jianzhu_type` varchar(20) not null,
    #                  `jz_mianji` varchar(20) not null,
    #                  `lvhualv` varchar(20),
    #                  `rongjilv` varchar(20),
    #                  `desc` text not null,
    #                  primary key (`id`))
    #                  engine=innodb default charset=utf8"""
    # test_db_helper = TestDBHelper('STORE_CONFIG')
    # test_db_helper.create_table(create_sql)
