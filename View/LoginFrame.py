# -*- coding: utf-8 -*-
#!/usr/bin/env python
import wx
import hashlib
import MySQLdb
import smtplib
import socket

from UserFrame import UserFrame
from AdminFrame import AdminFrame
from RegisterFrame import RegisterFrame
from DataBaseOperator import DataBaseOperator

class LoginFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title = u'登录')

        self.p = wx.Panel(self)

        self.id_entry  = wx.TextCtrl(self.p)
        self.passwd_entry      = wx.TextCtrl(self.p, style = wx.TE_PASSWORD)

        self.login_btn         = None
        self.register_btn      = None
        self.forget_passwd_btn = None
        # rb为单选按钮组
        self.rb                = None
        # 调用类里面的函数进行布局
        self.__arrangement()

        # 设置大小
        self.SetSize((320,310))
        self.SetMinSize((320,310))
        self.SetMaxSize((461,346))

        # 调用类里面的函数进行按键响应设置
        self.__set_events()


    def __arrangement(self):
        self.Center()
        

        # 设置背景图片
        jpg = wx.Image('login1.jpg', type = wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        wx.StaticBitmap(self.p, bitmap = jpg)        

        # 本界面要用到的布局管理器
        main_sizer   = wx.BoxSizer(wx.VERTICAL)
        title_sizer  = wx.BoxSizer()
        user_sizer   = wx.BoxSizer()
        passwd_sizer = wx.BoxSizer()
        btn_sizer    = wx.BoxSizer()
        radio_sizer  = wx.BoxSizer()

        # 初始化本界面要用到的各种控件
        title_label    = wx.StaticText(self.p, label = u'个人信息管理系统')
        font = wx.Font(23, wx.SWISS, wx.BOLD, wx.NORMAL)
        title_label.SetFont(font)
        title_label.SetForegroundColour('Green')

        id_label       = wx.StaticText(self.p, label = u'id帐号')
        font = wx.Font(10, wx.SWISS, wx.ITALIC | wx.BOLD, wx.NORMAL)
        id_label.SetFont(font)
        id_label.SetForegroundColour('Yellow')

        passwd_label           = wx.StaticText(self.p, label = u' 密码  ')
        font = wx.Font(10, wx.SWISS, wx.BOLD | wx.ITALIC , wx.NORMAL)
        passwd_label.SetFont(font)
        passwd_label.SetForegroundColour('Yellow')
        self.forget_passwd_btn = wx.Button(self.p, label = u'忘记密码?')

        self.rb = wx.RadioBox(
            self.p, label = u'用户类型', 
            choices = [u'个人', u'管理员']
            )

        self.login_btn         = wx.Button(self.p, label = u'登录')
        self.register_btn      = wx.Button(self.p, label = u'注册')
        
        # 将控件添加到布局管理器中
        title_sizer.Add(title_label, proportion = 0,
                        flag = wx.ALIGN_CENTRE | wx.ALL, border = 5)
        
        user_sizer.Add(id_label, proportion = 0,
                        flag = wx.ALIGN_CENTRE | wx.ALL, border = 5)
        user_sizer.Add(self.id_entry,proportion = 1,
                        flag = wx.ALIGN_CENTRE | wx.ALL , border = 5)
        
        passwd_sizer.Add(passwd_label, proportion = 0,
                        flag = wx.ALIGN_CENTRE | wx.ALL, border = 5)
        passwd_sizer.Add(self.passwd_entry, proportion = 1,
                        flag = wx.ALIGN_CENTRE | wx.ALL, border = 5)
        passwd_sizer.Add(self.forget_passwd_btn, proportion = 0,
                        flag = wx.ALIGN_CENTRE | wx.ALL, border = 5)

        btn_sizer.Add(self.login_btn, proportion = 0,
                        flag = wx.ALIGN_CENTRE | wx.ALL, border = 5)
        btn_sizer.Add(self.register_btn, proportion = 0,
                        flag = wx.ALIGN_CENTRE | wx.ALL, border = 5)

        radio_sizer.Add(self.rb, proportion = 0,
                        flag = wx.ALIGN_CENTRE | wx.ALL, border = 5)

        # 在主控件中添加这些控件
        main_sizer.Add(title_sizer, proportion = 3, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)
        main_sizer.Add(user_sizer, proportion = 1, flag = wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, border = 5)
        main_sizer.Add(passwd_sizer, proportion = 1, flag = wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, border = 5)
        main_sizer.Add(radio_sizer, flag = wx.ALIGN_CENTER | wx.ALL , border = 5)
        main_sizer.Add(btn_sizer, proportion = 1, flag = wx.ALIGN_CENTER | wx.ALL, border = 5)

        self.p.SetSizer(main_sizer)

    def __set_events(self):
        '''
        这里是事件设置函数
        '''
        self.login_btn.Bind(wx.EVT_BUTTON, self.on_login)
        self.forget_passwd_btn.Bind(wx.EVT_BUTTON, self.on_forget_password)
        self.register_btn.Bind(wx.EVT_BUTTON, self.on_register)

    def on_forget_password(self, event):
        '''
        发送邮箱到客户那里，告知密码
        '''
        # 1. 先检测用户是否输入了id号,若没输入，则提醒用户输入id号
        user_id = self.id_entry.GetValue()
        if not user_id:
                # 跳出一个对话框,提示用户id或密码错误
                dlg = wx.MessageDialog(self.p, u'请输入您的id号，以方便找回密码',
                                       'Error',
                                       wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()                        
        # 2. 若用户输入了id号，则通过数据库进行查询，获取其邮箱和密码
        else:
            db = DataBaseOperator(user_id)
            result = db.get_user_information_for_passwd()

            # 获取邮箱,密码和姓名
            receiver = result[0]
            pwd      = result[1]
            name     = result[2]

            sender = "1826716493@qq.com"

            # sending qq email
            body = """
            您好，您在个人信息管理
            系统里面的密码是
            %s（请妥善保管）\n
            (邮箱是系统自动发送的，如果您不需要这份信息，请删除掉即可)""".decode('utf-8') % pwd

            s = smtplib.SMTP()
            # 确保处在联网环境下
            try:
                s.connect("smtp.qq.com")        # 这里是qq邮箱的smtp服务器
            except socket.gaierror as e:
                dlg = wx.MessageDialog(self.p, u'请确保您处在联网的环境下',
                                       'Password Sending',
                                       wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                s.login("1826716493@qq.com", "lmzzgCHZ179")
                msg = u"From:%s\r\nTo: %s\r\nSubject: 个人信息管理系统密码提示\r\n" % (sender, name)

                msg += body
                s.sendmail(sender, receiver.encode('utf-8'), msg.encode('utf-8'))
                s.close()
                # 跳出一个对话框,提示用户id或密码错误
                dlg = wx.MessageDialog(self.p, u'邮件已发送到您的邮箱，请注意查收',
                                       'Password Sending',
                                       wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
            

    def on_login(self, event):
        '''
        当登录按钮被按下之后,就会进入这个函数
        '''
        # 记住,id为整形
        user_id = int(self.id_entry.GetValue())
        user_passwd = self.passwd_entry.GetValue()

        # 判断是用户还是管理员
        user = bool(self.rb.GetSelection() == 0)
        db = DataBaseOperator()
        if user:
            result_len = db.login_get_user_information(user_id, user_passwd)
            # 若长度为0,则表示出错,若长度为1,则代表成功
            if result_len:
                # 登录成功的时候,跳转到个人界面
                self.Close()
                user_frame = UserFrame(user_id = user_id)
                user_frame.Show()
            else:
                # 跳出一个对话框,提示用户id或密码错误
                dlg = wx.MessageDialog(self.p, u'用户名或密码错误',
                                       'Error',
                                       wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
        else:
            result_len = db.login_get_admin_information(user_id, user_passwd)
            # 若长度为0,则表示出错,若长度为1,则代表成功
            if result_len:
                # 登录成功的时候,跳转到个人界面
                self.Close()
                admin_frame = AdminFrame(admin_id = user_id)
                admin_frame.Show()
            else:
                # 跳出一个对话框,提示用户id或密码错误
                dlg = wx.MessageDialog(self.p, u'用户名或密码错误',
                                       'Error',
                                       wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()            
            
        
    def on_register(self, event):
        '''
        当注册按钮被按下之后,就会进入这个函数
        '''
        register_frame = RegisterFrame(self)
        register_frame.Show()


if __name__ == '__main__':
    app = wx.App()
    login_frame = LoginFrame()
    login_frame.Show()
    app.MainLoop()

