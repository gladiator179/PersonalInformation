# -*- coding: utf-8 -*-
import wx
# 注解:不能单独运行它,这个from ... import中的文件路径是相对于第一个执行的程序的路径而言的
# 这样会让事情好办得多..
from DataBaseOperator import DataBaseOperator
# 导入布局模板
from arrange_model import sub_arrangement

class OnChangePwd(wx.Frame):
    '''
    本界面是关于修改密码的界面
    '''
    def __init__(self, user_id, father = None):
        wx.Frame.__init__(self, father, title = u'修改密码')
        self.user_id = user_id
        self.p = wx.Panel(self)

        self.new_passwd_entry     = wx.TextCtrl(self.p, 
                                            style = wx.TE_PASSWORD)
        self.confirm_passwd_entry = wx.TextCtrl(self.p, 
                                            style = wx.TE_PASSWORD)
        self.change_btn           = wx.Button(self.p, label = u'修改')
        self.cancel_btn           = wx.Button(self.p, label = u'返回')
        # 调用类里面的布局函数进行布局
        self.__arrangement()

        # 调用类里面的函数进行按键响应设置
        self.__set_events()

    def __arrangement(self):
        main_sizer   = wx.BoxSizer(wx.VERTICAL)

        new_passwd_label     = wx.StaticText(self.p, label = u'新密码')
        confirm_passwd_label = wx.StaticText(self.p, label = u'确认密码')

        label_entry_tuple = (
            (new_passwd_label, self.new_passwd_entry),
            (confirm_passwd_label, self.confirm_passwd_entry)
        )
        button_tuple = (self.change_btn, self.cancel_btn)
        # 调用子布局模板
        sub_arrangement(self.p, main_sizer, label_entry_tuple, button_tuple)

        main_sizer.Fit(self)
        self.Center()

    def __set_events(self):
        '''
        设置按键相关参数
        '''
        self.change_btn.Bind(wx.EVT_BUTTON, self.on_change_btn)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel_btn)
        

    def on_change_btn(self, event):
        '''
        当本按键按下之后,就会检查两次密码前后是否匹配
        若不匹配,则提醒用户重新输入
        若匹配则修改密码,并提示修改成功
        '''
        new_passwd = self.new_passwd_entry.GetValue()
        confirm_passwd = self.confirm_passwd_entry.GetValue()
        if new_passwd == '' or confirm_passwd == '':
            # 提醒用户重新输入
            # 跳出一个对话框
            dlg = wx.MessageDialog(self.p, u'输入不能为空',
                                   'Error',
                                   wx.OK | wx.ICON_ERROR)

            self.new_passwd_entry.SetValue('')
            self.confirm_passwd_entry.SetValue('')
            dlg.ShowModal()
            dlg.Destroy()
            
        elif new_passwd != confirm_passwd:
            # 提醒用户重新输入
            # 跳出一个对话框,提示用户密码不匹配
            dlg = wx.MessageDialog(self.p, u'两次密码前后不匹配,请重新输入',
                                   'Error',
                                   wx.OK | wx.ICON_ERROR)

            self.new_passwd_entry.SetValue('')
            self.confirm_passwd_entry.SetValue('')
            dlg.ShowModal()
            dlg.Destroy()

        else:
            # 进行数据库操作
            db  = DataBaseOperator(self.user_id)
            db.change_password(new_passwd)
            dlg = wx.MessageDialog(self.p, u'密码修改成功',
                                   'success',
                                   wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            self.Close()
            
  
    def on_cancel_btn(self, event):
        '''
        当本按键按下之后,就会退出窗口
        '''
        self.Close()
