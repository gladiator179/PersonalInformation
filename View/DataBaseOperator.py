# -*- coding: utf-8 -*-
import wx
import time
import MySQLdb

from calendar import isleap
def get_max_date_from_month(year, month):
    month_31_dates = ['01', '03', '05', '07', '08', '10', '12']
    if month in month_31_dates:
        return '31'
    elif month == '02':
        if isleap(int(year)):
            return '29'
        else:
            return '28'
    else:
        return '30'
    

class DataBaseOperator:
    '''
    这个类主要用于在本程序中所有和数据库相关的操作
    当这个类被调用的时候,就默认连接上了数据库
    '''
    def __init__(self, user_id = None):
        self.user_id = user_id
        self.conn    = MySQLdb.connect(host = 'localhost', port = 3306,
                                       user = 'zero', passwd = 'gladiator',
                                       db   = 'personal_information', 
                                       charset = 'utf8')

    
# -------------下面是和个人信息相关的操作 -----------------------------
    def get_user_information_for_passwd(self):
        '''
        本方法可以通过用户的id号获取其密码和邮箱
        '''
        cur = self.conn.cursor()
        sql = """ select user_email, user_passwd,user_name from basic_information
        where user_id = %s
        """ % self.user_id
        cur.execute(sql)
        result = cur.fetchone()
        cur.close()
        return result

    def get_user_information(self):
        '''
        本方法可以通过用户的id号获取所有的个人信息
        '''
        cur = self.conn.cursor()
        sql = """ Select user_name, user_sex, user_email, user_phone from basic_information
        where user_id = %s """ % self.user_id
        cur.execute(sql)
        result = cur.fetchone()
        cur.close()
        return result

    def update_user_information(self, user_name, user_sex, user_email, user_phone):
        '''
        本方法可以通过用户的id号和相关参数更新用户的个人信息
        '''
        cur = self.conn.cursor()
        sql = """
        UPDATE basic_information SET user_name = '%s', user_sex = '%s', 
        user_email = '%s', user_phone = '%s' WHERE user_id = %s
        """ % (user_name, user_sex, user_email, user_phone, self.user_id)
        cur.execute(sql)
        cur.close()
        self.conn.commit()
        pass

    def change_password(self, new_passwd):
        '''
        本方法可以通过用户的id号和密码修改用户密码
        '''
        cur = self.conn.cursor()
        sql = """
        UPDATE basic_information SET user_passwd = '%s' 
        WHERE user_id = %s
        """ % (new_passwd, self.user_id)
        cur.execute(sql)
        cur.close()
        self.conn.commit()


# -------------------------下面是和朋友信息相关的操作 -----------------------
    def id_get_friend_information(self, f_id):
        '''
        本方法可以通过朋友的id号来获得所有信息
        '''
        cur = self.conn.cursor()
        sql = """
        SELECT friends_id, f_name, f_know_date, f_birth, f_friend_email, f_friend_qq FROM friends WHERE
        friends_id = %s 
        """ % f_id
        cur.execute(sql)
        result = cur.fetchone()
        cur.close()
        return result

    def get_friend_information(self, name, know_date):
        '''
        本方法可以通过用户的名字和认识时间得到所有信息
        '''
        cur = self.conn.cursor()
        if know_date:
            sql = """
            SELECT friends_id, f_name, f_know_date, f_birth, f_friend_email, f_friend_qq 
            FROM friends WHERE
            f_name like '%%%s%%' and f_know_date = '%s' and u_id = %s
            """ % (name, know_date, self.user_id)
        else:
            sql = """
            SELECT friends_id, f_name, f_know_date, f_birth, f_friend_email, f_friend_qq 
            FROM friends WHERE
            u_id = %(user_id)s and f_name like '%%%(name)s%%'
            """ % {'user_id': self.user_id, 'name': name}

        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        return result

    
    def add_friend_information(self, name, know_date, birth,  email, qq):
        cur = self.conn.cursor()
        # 先判断生日一栏是否为空，据此来改变sql语句
        if birth == "":
            sql = """
            INSER INTO friends(f_name, f_know_date, f_friend_email, f_friend_qq, u_id)
            values('%s', '%s', '%s', '%s', %s) 
            """ % (name, know_date, email, qq, self.user_id)
        else:
            sql = """
            INSERT INTO friends(f_name, f_know_date, f_birth, f_friend_email, f_friend_qq, u_id)
            values('%s', '%s', '%s', '%s', '%s', %s) 
            """ % (name, know_date, birth, email, qq, self.user_id)
        cur.execute(sql)
        cur.close()
        self.conn.commit()

    def delete_friend_information(self, friend_id):
        cur = self.conn.cursor()
        sql = """
        DELETE FROM friends WHERE friends_id = %s AND u_id = %s
        """ % (friend_id, self.user_id)
        cur.execute(sql)
        cur.close()
        self.conn.commit()

    def update_friend_information(self, friend_id, name, know_date, birth, email, qq):
        cur = self.conn.cursor()
        sql = """
        UPDATE friends SET f_name = '%s', f_know_date = '%s', f_birth = '%s',
        f_friend_email = '%s', f_friend_qq = '%s' where friends_id = %s AND
        u_id = %s
        """ % (name, know_date, birth, email, qq, friend_id, self.user_id)
        cur.execute(sql)
        cur.close()
        self.conn.commit()

# -------------------------下面是和通讯录信息相关的操作----------------------
    def id_get_address_list_information(self, al_id):
        '''
        返回一个元组,程序外要记得对元组进行操作
        '''
        cur = self.conn.cursor()
        sql = """
        SELECT al_name, al_phone FROM address_list WHERE address_id = %s AND u_id = %s
        """ % (al_id, self.user_id)
        cur.execute(sql)
        result = cur.fetchone()
        cur.close()
        self.conn.commit()
        return result


    def get_address_list_information(self, name):
        '''
        返回一个元组,程序外要记得对元组进行操作
        '''
        cur = self.conn.cursor()
        sql = """
        SELECT * FROM address_list WHERE al_name LIKE '%%%s%%' AND u_id = %s
        """ % (name, self.user_id)
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        self.conn.commit()
        return result

    def add_address_list_information(self, name, phone):
        '''
        根据姓名和电话号码添加一条通讯录记录
        '''
        cur = self.conn.cursor()
        sql = """
        INSERT INTO address_list(al_name, al_phone, u_id) VALUES
        ('%s', '%s', %s)
        """ % (name, phone, self.user_id)
        cur.execute(sql)
        cur.close()
        self.conn.commit()

    def delete_address_list_information(self, address_list_id):
        '''
        根据通讯录id号删除一条通讯录记录
        '''
        cur = self.conn.cursor()
        sql = """
        DELETE FROM address_list WHERE address_id = %s AND u_id = %s
        """ % (address_list_id, self.user_id)
        cur.execute(sql)
        cur.close()
        self.conn.commit()

    def update_address_list_information(self, address_list_id, name, phone):
        '''
        根据id号,姓名和电话号码更新一条通讯记录
        '''
        cur = self.conn.cursor()
        sql = """
        UPDATE address_list SET al_name = '%s', al_phone = '%s'
        WHERE address_id = %s AND u_id = %s
        """ % (name, phone, address_list_id, self.user_id)
        cur.execute(sql)
        cur.close()
        self.conn.commit()

# -------------------------下面是和备忘录相关的操作 -------------------------
    def id_get_memo_information(self, i):
        '''
        根据备忘录id号获取所有和备忘录相关的信息
        '''
        cur = self.conn.cursor()
        sql = """
        SELECT memo_date, memo_place, memo_happen FROM 
        memorandum WHERE memo_id = %s and u_id = %s
        """ % (i, self.user_id)
        cur.execute(sql)
        result = cur.fetchone()
        cur.close()
        return result
        

    def get_memo_information(self, date):
        '''
        根据日期来获得所有相关的信息
        '''
        cur = self.conn.cursor()
        # 判断date是什么格式的字符串(精确到年月 还是 精确到年月日)
        if len(date) == 7:
            # 先判定它是否有31天,或者是否是2月份,然后进行赋值操作
            month_max_date = get_max_date_from_month(date[:4],date[5:7])
            tmp_date = date + '-%s' % month_max_date

            # 将只有月份的日期给具体话,以构造sql语句
            date += '-01'

            sql = """
            SELECT memo_id, memo_date, memo_place, memo_happen FROM memorandum 
            WHERE memo_date >= '%s' AND memo_date <= '%s'
            AND u_id = %s
            """ % (date, tmp_date, self.user_id)

        elif len(date) == 0:
            sql = """
            SELECT memo_id, memo_date, memo_place, memo_happen FROM memorandum 
            WHERE u_id = %s
            """ % (self.user_id)

        else:
            sql = """
            SELECT memo_id, memo_date, memo_place, memo_happen
            FROM memorandum WHERE memo_date = '%s' AND u_id = %s
            """ % (date, self.user_id)

        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        return result


    def add_memo_information(self, memo_date, memo_place, memo_happen):
        '''
        根据日期,地点和事件来添加备忘录
        '''
        cur = self.conn.cursor()
        sql = """
        INSERT INTO memorandum(memo_date, memo_place, memo_happen, u_id) VALUES
        ('%s', '%s', '%s', '%s') 
        """ % (memo_date, memo_place, memo_happen, self.user_id)
        cur.execute(sql)
        cur.close()
        self.conn.commit()

    def delete_memo_information(self, memo_id):
        '''
        根据备忘录的id号来删除备忘录
        '''
        cur = self.conn.cursor()
        sql = """
        DELETE FROM memorandum WHERE memo_id = %s
        """ % memo_id
        cur.execute(sql)
        cur.close()
        self.conn.commit()


    def update_memo_information(self, memo_id, memo_date, memo_place, memo_happen):
        '''
        更新备忘录
        '''
        cur = self.conn.cursor()
        sql = """
        UPDATE memorandum SET memo_date = '%s', memo_place = '%s', memo_happen = '%s'
        WHERE memo_id = %s AND u_id = %s
        """ % (memo_date, memo_place, memo_happen, memo_id, self.user_id)
        cur.execute(sql)
        cur.close()
        self.conn.commit()

# -------------------------下面是和日志相关的操作 ---------------------------
    def id_get_journal_information(self, i):
        '''
        根据日志的id号获取日志详细信息
        '''
        cur = self.conn.cursor()
        sql = """
        SELECT j_subject, j_type, j_content FROM 
        personal_journal WHERE journal_id = %s AND u_id = %s
        """ % (i, self.user_id)
        cur.execute(sql)
        result = cur.fetchone()
        cur.close()
        return result

    def get_journal_information(self, t):
        '''
        根据日志的类型来获取所有的日志列表
        返回的内容为id, 主题, 日志类型
        '''
        # 先判断t是否为空,若为空,则输出所有的日志列表即可
        cur = self.conn.cursor()
        if len(t) == 0:
            sql = """
            SELECT journal_id, j_subject, m_time, j_type FROM 
            personal_journal WHERE  u_id = %s
            """ % (self.user_id)
        else:
            sql = """
            SELECT journal_id, j_subject, m_time, j_type FROM 
            personal_journal WHERE j_type = '%s' and u_id = %s
            """ % (t, self.user_id)
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        return result

    def add_journal_information(self, j_subject, j_content, j_type):
        '''
        添加一条新日志
        '''
        # 添加一条日志之前,要先获取当前时间
        # something about strftime
        # time.strftime(format[, t])
        # if t is not provided, the current time as returned by localtime() is used
        current_date = time.strftime('%Y-%m-%d')

        cur = self.conn.cursor()
        sql = """
        INSERT INTO personal_journal(j_subject, j_content, j_type, m_time, u_id)
        VALUES ('%s', '%s', '%s', '%s', %s)
        """ % (j_subject, j_content, j_type, current_date, self.user_id)
        cur.execute(sql)
        cur.close()
        self.conn.commit()

    def delete_journal_information(self, j_id):
        '''
        删除一条日志
        '''
        cur = self.conn.cursor()
        sql = """
        DELETE FROM personal_journal WHERE journal_id = %s AND u_id = %s
        """ % (j_id, self.user_id)
        cur.execute(sql)
        cur.close()
        self.conn.commit()

    def update_journal_information(self, j_id, j_subject, j_content, j_type):
        '''
        更新一条日志
        '''
        # 更新一条日志之前,要先获取当前时间
        # something about strftime
        # time.strftime(format[, t])
        # if t is not provided, the current time as returned by localtime() is used
        current_date = time.strftime('%Y-%m-%d')

        cur = self.conn.cursor()
        sql = """
        UPDATE personal_journal SET j_subject = '%s', 
        j_content = '%s', j_type = '%s', m_time = '%s' WHERE journal_id = %s and u_id = %s
        """ % (j_subject, j_content, j_type, current_date, j_id, self.user_id)
        cur.execute(sql)
        cur.close()
        self.conn.commit()
        

# -----------------------------------下面是和用户基本信息查询相关的工作----------------
    def get_user_basic_information(self, u_name, u_sex):
        cur = self.conn.cursor()
        if u_sex == '':
            sql = """
            SELECT user_id, user_name, user_sex, user_email, user_phone 
            FROM basic_information WHERE
            user_name LIKE '%%%s%%'
            """ % u_name
        else:
            sql = """
            SELECT user_id, user_name, user_sex, user_email, user_phone 
            FROM basic_information WHERE
            user_name LIKE '%%%s%%' AND user_sex = '%s'
            """ % (u_name, u_sex)
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        return result

# -----------------------------------下面是和登录相关的验证工作----------------

# ---------------------------个人登录----------------------------------------
    def login_get_user_information(self, user_id, user_pwd):
        '''
        返回bool值
        若用户的id和密码匹配，则返回真
        否则返回假
        '''
        cur = self.conn.cursor()
        sql = """
        SELECT user_id, user_passwd FROM basic_information 
        WHERE user_id = %d and user_passwd = '%s'""" % (user_id, user_pwd)
        result_len = cur.execute(sql)
        cur.close()
        return result_len

# --------------------------管理员登录--------------------------------------
    def login_get_admin_information(self, admin_id, admin_pwd):
        '''
        返回bool值
        当管理员的id和密码匹配的时候,返回真
        否则返回假
        '''
        cur = self.conn.cursor()
        sql = """
        SELECT admin_id, admin_passwd FROM admin
        WHERE admin_id = %d and admin_passwd = '%s'""" % (admin_id, admin_pwd)
        result_len = cur.execute(sql)
        cur.close()
        return result_len

    def __del__(self):
        self.conn.close()
