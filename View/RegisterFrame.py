# -*- coding: utf-8 -*
#!/usr/bin/env python
import wx
import hashlib
import MySQLdb

class RegisterFrame(wx.Frame):
    '''
    注册组件,需要父组件(登录组件)作为参数传过来
    '''
    def __init__(self, father):
        wx.Frame.__init__(self, father, title = u'注册')
        self.p = wx.Panel(self)

        self.register_btn      = wx.Button(self.p, label = u'注册')
        self.cancel_btn        = wx.Button(self.p, label = u'取消')
        # 调用类里面的函数进行布局
        self.__arrangement()

        # 设置大小
        self.SetSize((461,219))
        self.SetMinSize((461,219))
        self.SetMaxSize((461,219))

        # 调用类里面的函数进行按键响应设置
        self.__set_events()


    def __arrangement(self):
        self.Center()
        # 本界面要用到的布局管理器
        main_sizer    = wx.BoxSizer(wx.VERTICAL)
        input_sizer  = wx.GridBagSizer(5, 1)
        button_sizer = wx.BoxSizer()        


        # 尝试使用GridBagSizer
        # 初始化标签和文本输入栏
        name_label     = wx.StaticText(self.p, label = u'姓名')
        sex_label      = wx.StaticText(self.p, label = u'性别(只能为男或女)')
        email_label    = wx.StaticText(self.p, label = u'电子邮箱')
        phone_label    = wx.StaticText(self.p, label = u'电话号码')
        passwd_label   = wx.StaticText(self.p, label = u'密码')
        
        # lack
        # 这些文本框均要有一个初始化值的,这里缺少初始化值的处理
        self.sex_entry      = wx.TextCtrl(self.p, size = (300, -1))
        self.email_entry    = wx.TextCtrl(self.p, size = (300, -1))
        self.phone_entry    = wx.TextCtrl(self.p, size = (300, -1))
        self.name_entry     = wx.TextCtrl(self.p, size = (300, -1))
        self.passwd_entry   = wx.TextCtrl(self.p, size = (300, -1), style = wx.TE_PASSWORD)
        # end lack

        input_sizer.Add(passwd_label, (1, 0))
        input_sizer.Add(self.passwd_entry, (1, 1))
        input_sizer.Add(name_label, (2, 0))
        input_sizer.Add(self.name_entry, (2, 1), flag = wx.EXPAND)
        input_sizer.Add(sex_label, (3, 0))
        input_sizer.Add(self.sex_entry, (3, 1))
        input_sizer.Add(email_label, (4, 0))
        input_sizer.Add(self.email_entry, (4, 1))
        input_sizer.Add(phone_label, (5, 0))
        input_sizer.Add(self.phone_entry, (5, 1))

        # 下面是按键的处理
        button_sizer.Add(self.register_btn, border = 5)
        button_sizer.Add(self.cancel_btn, border = 5)

        # 最后将这些组建全部添加到主布局管理器中
        main_sizer.Add(input_sizer, flag = wx.ALL | wx.EXPAND, border = 5)
        main_sizer.Add(button_sizer, flag = wx.ALL | wx.ALIGN_CENTER, border = 5)

        self.p.SetSizer(main_sizer)

    def __set_events(self):
        '''
        本函数负责进行按键的绑定
        '''
        self.register_btn.Bind(wx.EVT_BUTTON, self.on_register)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)
    
    def on_register(self, event):
        '''
        注册的具体操作,和数据库操作相关
        '''
        # 获取输入的值
        user_sex    = self.sex_entry.GetValue()
        user_email  = self.email_entry.GetValue()
        user_phone  = self.phone_entry.GetValue()
        user_name   = self.name_entry.GetValue()
        user_passwd = self.passwd_entry.GetValue()
        
        if user_sex == '' or user_email == '' or user_phone == '' or user_name == '' \
        or user_passwd == '':
            dlg    = wx.MessageDialog(self.p, u'注册失败, 不能有空信息',
                                      'Failure',
                                      wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()            
        else:
            conn = MySQLdb.connect(host = 'localhost', port = 3306, user = 'zero',
                                   passwd = 'gladiator', db = 'personal_information', 
                                   charset = 'utf8')
            cur  = conn.cursor()
            sql  = """INSERT INTO basic_information(user_name, user_sex, user_email, user_passwd, user_phone)
            values ('%s', '%s', '%s', '%s', '%s') """ % (user_name, user_sex, user_email, user_passwd, user_phone)
            # 用游标执行本条sql语句
            cur.execute(sql)
            # 最后要调用连接的commit方法提交事务
            conn.commit()
            # 然后需要弹出一个对话框,提醒用户他的id号是什么.
            sql = """ select user_id from basic_information where 
            user_name = '%s' and user_email = '%s' and user_passwd = '%s' and user_phone = '%s'
            and user_sex = '%s' """ % (user_name, user_email, user_passwd, user_phone, user_sex)
            cur.execute(sql)
            result = cur.fetchone()
            dlg    = wx.MessageDialog(self.p, u'注册成功, 您的id号为: %s' % result,
                                      'Success',
                                      wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

            # 关闭游标
            cur.close()
            # 关闭连接
            conn.close()
        
    def on_cancel(self, event):
        self.Close()

if __name__ == '__main__':
    app = wx.App()
    register_frame = RegisterFrame()
    register_frame.Show()
    app.MainLoop()
