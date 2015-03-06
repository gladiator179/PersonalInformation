# -*- coding: utf-8 -*-
import wx
from arrange_model import sub_arrangement
from DataBaseOperator import DataBaseOperator

class OnAddFrame(wx.Frame):
    '''
    这里是关于备忘录中添加备忘录的界面
    '''
    def __init__(self, user_id, father = None):
        wx.Frame.__init__(self, father, title = u'添加备忘录')
        self.user_id = user_id

        # 面板初始化
        self.p = wx.Panel(self)
        
        # 按键初始化
        self.add_btn    = wx.Button(self.p, label = u'添加')
        self.cancel_btn = wx.Button(self.p, label = u'返回')
        
        # 文本控件初始化        
        self.memo_date_entry   = wx.TextCtrl(self.p, size = (300, -1))
        self.memo_place_entry  = wx.TextCtrl(self.p, size = (300, -1))
        self.memo_happen_entry = wx.TextCtrl(self.p, size = (300, -1))


        # 调用类里面的布局函数
        self.__arrangement()

        # 调用类里面的函数进行按键响应设置
        self.__set_events()

    def __arrangement(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 标签,文本输入控件
        memo_date_label = wx.StaticText(self.p, label = u'备忘日期(格式为xxxx-xx-xx)')
        memo_place_label = wx.StaticText(self.p, label = u'地点')
        memo_happen_label = wx.StaticText(self.p, label = u'事件')

        label_entry_tuple = (
            (memo_date_label, self.memo_date_entry),
            (memo_place_label, self.memo_place_entry),
            (memo_happen_label, self.memo_happen_entry)
        )

        button_tuple = (self.add_btn, self.cancel_btn)

        sub_arrangement(self.p, main_sizer, label_entry_tuple, button_tuple)
        main_sizer.Fit(self)
        self.Center()

    def __set_events(self):
        self.add_btn.Bind(wx.EVT_BUTTON, self.on_add)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_add(self, event):
        db = DataBaseOperator(self.user_id)
        memo_date   = self.memo_date_entry.GetValue()
        memo_place  = self.memo_place_entry.GetValue()
        memo_happen = self.memo_happen_entry.GetValue()

        # 先判断日期和事件输入是否有误
        if memo_date == '' or memo_happen == '':
            # 跳出一个对话框
            dlg = wx.MessageDialog(self.p, u'日期和事件均不能为空,请重试',
                                   'Error',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()            
        else:
            # 跳出一个对话框
            db.add_memo_information(memo_date, memo_place, memo_happen)
            dlg = wx.MessageDialog(self.p, u'添加成功',
                                   'Success',
                                   wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()                            

    def on_cancel(self, event):
        self.Close()
