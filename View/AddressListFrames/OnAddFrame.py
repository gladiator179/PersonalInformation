# -*- coding: utf-8 -*-
import wx
from DataBaseOperator import DataBaseOperator
from arrange_model import sub_arrangement

class OnAddFrame(wx.Frame):
    '''
    这里是关于通讯录中添加通讯录信息的界面
    '''
    def __init__(self, user_id, father = None):
        wx.Frame.__init__(self, father, title = u'添加朋友')
        self.user_id = user_id

        # 面板初始化
        self.p = wx.Panel(self)
        
        # 按键初始化
        self.add_btn    = wx.Button(self.p, label = u'添加')
        self.cancel_btn = wx.Button(self.p, label = u'返回')
        
        # 文本控件初始化
        self.f_name_entry      = wx.TextCtrl(self.p, size = (300, -1))
        self.f_phone_entry     = wx.TextCtrl(self.p, size = (300, -1))
        
        # 调用类里面的布局函数进行布局
        self.__arrangement()

        # 调用类里面的函数进行按键响应设置
        self.__set_events()
        
    def __arrangement(self):
        # 主布局管理器
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 初始化标签
        f_name_label      = wx.StaticText(self.p, label = u'姓名:')
        f_phone_label     = wx.StaticText(self.p, label = u'电话号码')

        # 构造标签和输入控件
        label_entry_tuple = (
            (f_name_label     , self.f_name_entry),
            (f_phone_label    , self.f_phone_entry)
        )

        buttons = (self.add_btn, self.cancel_btn)
        
        sub_arrangement(self.p, main_sizer, label_entry_tuple, buttons)
        main_sizer.Fit(self)
        self.Center()

    def __set_events(self):
        self.add_btn.Bind(wx.EVT_BUTTON, self.on_add)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

# ---------------------- 按键响应 --------------------------------

    def on_add(self, event):
        '''
        当这个按键被按下之后,就可以添加一条通讯录记录
        '''
        name      = self.f_name_entry.GetValue()
        phone     = self.f_phone_entry.GetValue()

        if name == '' or phone == '':
            # 跳出一个对话框
            dlg = wx.MessageDialog(self.p, u'姓名和电话均不能为空',
                                   'Error',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()            
        else:
            db = DataBaseOperator(self.user_id)
            db.add_address_list_information(name, phone)
            # 跳出一个对话框
            dlg = wx.MessageDialog(self.p, u'添加成功',
                                   'Success',
                                   wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()                    

    def on_cancel(self, event):
        self.Close()
