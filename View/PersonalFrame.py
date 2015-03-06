# -*- coding: utf-8 -*-
import wx
from DataBaseOperator import DataBaseOperator
from PersonalFrames.OnChangePwd import OnChangePwd

class PersonalFrame(wx.Frame):
    '''
    修改个人信息的界面
    '''
    def __init__(self, user_id, father = None):
        wx.Frame.__init__(self, father, title = u'修改个人信息')
        self.user_id = user_id
        self.p = wx.Panel(self)

        # 声明属于该类中的各种控件
        self.change_pwd_btn = wx.Button(self.p, label = u'修改密码')
        self.update_btn     = wx.Button(self.p, label = u'更改')
        self.cancel_btn     = wx.Button(self.p, label = u'返回')

        # 这些文本框均要有一个初始化值的,这里缺少初始化值的处理
        self.sex_entry      = wx.TextCtrl(self.p, size = (300, -1))
        self.email_entry    = wx.TextCtrl(self.p, size = (300, -1))
        self.phone_entry    = wx.TextCtrl(self.p, size = (300, -1))
        self.name_entry     = wx.TextCtrl(self.p, size = (300, -1))

        # 调用类里面的布局函数进行布局
        self.__arrangement()

        # 不同于其他界面,这里还要调用__set_entrys方法来设置文本控件的值
        self.__set_entrys()
        
        # 调用类里面的函数进行按键响应设置
        self.__set_events()

    def __arrangement(self):
        self.Center()

        # 本界面要用到的布局管理器
        main_sizer   = wx.BoxSizer(wx.VERTICAL)
        input_sizer  = wx.GridBagSizer(5, 1)
        button_sizer = wx.BoxSizer()

        # 尝试使用GridBagSizer
        # 初始化标签和文本输入栏
        id_label       = wx.StaticText(self.p, label = u'id')
        id_value_label = wx.StaticText(self.p, label = str(self.user_id))
        name_label     = wx.StaticText(self.p, label = u'姓名')
        sex_label      = wx.StaticText(self.p, label = u'性别')
        email_label    = wx.StaticText(self.p, label = u'电子邮箱')
        phone_label    = wx.StaticText(self.p, label = u'电话号码')
        
        input_sizer.Add(id_label, (1, 0))
        input_sizer.Add(id_value_label, (1, 1))
        input_sizer.Add(name_label, (2, 0))
        input_sizer.Add(self.name_entry, (2, 1), flag = wx.EXPAND)
        input_sizer.Add(sex_label, (3, 0))
        input_sizer.Add(self.sex_entry, (3, 1))
        input_sizer.Add(email_label, (4, 0))
        input_sizer.Add(self.email_entry, (4, 1))
        input_sizer.Add(phone_label, (5, 0))
        input_sizer.Add(self.phone_entry, (5, 1))

        # 下面是按键的处理
        button_sizer.Add(self.change_pwd_btn, border = 5)
        button_sizer.Add(self.update_btn, border = 5)
        button_sizer.Add(self.cancel_btn, border = 5)

        # 最后将这些组建全部添加到主布局管理器中
        main_sizer.Add(input_sizer, flag = wx.ALL | wx.EXPAND, border = 5)
        main_sizer.Add(button_sizer, flag = wx.ALL | wx.ALIGN_CENTER, border = 5)

        self.p.SetSizer(main_sizer)
        self.SetSize((380, 240))
        self.SetMaxSize((380, 240))
        self.SetMinSize((380, 240))


    def __set_events(self):
        self.change_pwd_btn.Bind(wx.EVT_BUTTON, self.on_change_pwd)
        self.update_btn.Bind(wx.EVT_BUTTON, self.on_update)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

# ----------------------- 按键响应函数 ------------------------------------
    def __set_entrys(self):
        '''
        设置文本控件中文本域的函数
        '''
        db   = DataBaseOperator(self.user_id)
        info = db.get_user_information()
        self.name_entry.SetValue(info[0])
        self.sex_entry.SetValue(info[1])
        self.email_entry.SetValue(info[2])
        self.phone_entry.SetValue(info[3])

    def on_change_pwd(self, event):
        '''
        当用户按下这个按键之后,就会跳出一个界面来修改密码
        '''
        change_pwd_frame = OnChangePwd(self.user_id, self)
        change_pwd_frame.Show()


    def on_update(self, event):
        '''
        当用户按下按键之后,就会更新自己的信息,然后提示用户更改成功
        '''
        user_name  = self.name_entry.GetValue()
        user_sex   = self.sex_entry.GetValue()
        user_email = self.email_entry.GetValue()
        user_phone = self.phone_entry.GetValue()

        db = DataBaseOperator(self.user_id)
        db.update_user_information(user_name, user_sex, user_email, user_phone)

        # 弹出对话框提醒用户更新成功
        dlg = wx.MessageDialog(self.p, u'更新成功',
                               'Success',
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()        
        

    def on_cancel(self, event):
        '''
        当用户按下按键之后,就会退出本这个个人信息显示
        '''
        self.Close()

if __name__ == '__main__':
    app = wx.App()
    personal_frame = PersonalFrame(1)
    personal_frame.Show()
    app.MainLoop()
