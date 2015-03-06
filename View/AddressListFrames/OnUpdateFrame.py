# -*- coding: utf-8 -*-
import wx
from arrange_model import sub_arrangement
from DataBaseOperator import DataBaseOperator

class OnUpdateFrame(wx.Frame):
    '''
    这里是关于通讯录中更新通讯录信息的界面
    '''
    def __init__(self, user_id, id_updated, father = None):
        wx.Frame.__init__(self, father, title = u'更新通讯录')
        self.user_id = user_id
        self.id_updated = id_updated

        # 面板初始化
        self.p = wx.Panel(self)
        
        # 按键初始化
        self.update_btn = wx.Button(self.p, label = u'更新')
        self.cancel_btn = wx.Button(self.p, label = u'返回')
        
        # 文本控件初始化
        self.address_name_entry  = wx.TextCtrl(self.p, size = (300, -1))
        self.address_phone_entry = wx.TextCtrl(self.p, size = (300, -1))
        
        # 调用类里面的布局函数进行布局
        self.__arrangement()

        # 调用文本控件内容设置函数
        self.__set_entry_value()

        # 调用类里面的函数进行按键响应设置
        self.__set_events()
        
    def __arrangement(self):
        # 主布局管理器
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 初始化标签
        address_name_label      = wx.StaticText(self.p, label = u'姓名:')
        address_phone_label     = wx.StaticText(self.p, label = u'电话号码')

        # 构造标签和输入控件
        label_entry_tuple = (
            (address_name_label     , self.address_name_entry),
            (address_phone_label    , self.address_phone_entry)
        )

        buttons = (self.update_btn, self.cancel_btn)
        
        sub_arrangement(self.p, main_sizer, label_entry_tuple, buttons)
        main_sizer.Fit(self)
        self.Center()

    def __set_entry_value(self):
        db = DataBaseOperator(self.user_id)
        result = db.id_get_address_list_information(self.id_updated)
        self.address_name_entry.SetValue(result[0])
        self.address_phone_entry.SetValue(result[1])

    def __set_events(self):
        self.update_btn.Bind(wx.EVT_BUTTON, self.on_update)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

# -------------------------- 按键响应组件 ------------------------------------
    def on_update(self, event):
        '''
        当这个按键被按下之后,就可以更新一条通讯录记录
        '''
        address_list_id        = self.id_updated
        address_list_name      = self.address_name_entry.GetValue()
        address_list_phone     = self.address_phone_entry.GetValue()

        # 先判断数据是否不合理
        if address_list_name == '' or address_list_phone == '':
            # 跳出一个对话框
            dlg = wx.MessageDialog(self.p, u'输入不能为空,请重试'
                                   'Error',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()            
        else:
            db = DataBaseOperator(self.user_id)
            db.update_address_list_information(address_list_id, 
                                               address_list_name, address_list_phone)
            # 跳出一个对话框
            dlg = wx.MessageDialog(self.p, u'更新成功',
                                   'Success',
                                   wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()            
            self.Close()

    def on_cancel(self, event):
        '''
        当这个按键被按下之后,就会退出
        '''
        self.Close()
