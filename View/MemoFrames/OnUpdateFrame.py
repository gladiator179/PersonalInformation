# -*- coding: utf-8 -*-
import wx
from arrange_model import sub_arrangement
from DataBaseOperator import DataBaseOperator

class OnUpdateFrame(wx.Frame):
    '''
    这里是关于备忘录中更新备忘录的界面
    '''
    def __init__(self, user_id, id_updated, father = None):
        wx.Frame.__init__(self, father, title = u'更新备忘录')
        self.id_updated = id_updated
        self.user_id = user_id


        # 面板初始化
        self.p = wx.Panel(self)
        
        # 按键初始化
        self.update_btn    = wx.Button(self.p, label = u'更新')
        self.cancel_btn = wx.Button(self.p, label = u'返回')
        
        # 文本控件初始化
        self.memo_date_entry   = wx.TextCtrl(self.p, size = (300, -1))
        self.memo_place_entry  = wx.TextCtrl(self.p, size = (300, -1))
        self.memo_happen_entry = wx.TextCtrl(self.p, size = (300, -1)) 
                                            

        # 调用类里面的布局函数
        self.__arrangement()

        # 调用类里面的设置文本域函数
        self.__set_entry_value()

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

        button_tuple = (self.update_btn, self.cancel_btn)

        sub_arrangement(self.p, main_sizer, label_entry_tuple, button_tuple)
        main_sizer.Fit(self)
        self.Center()

    def __set_entry_value(self):
        db = DataBaseOperator(self.user_id)
        result = db.id_get_memo_information(self.id_updated)

        self.memo_date_entry.SetValue(str(result[0]))
        self.memo_place_entry.SetValue(result[1])
        self.memo_happen_entry.SetValue(result[2])

    def __set_events(self):
        self.update_btn.Bind(wx.EVT_BUTTON, self.on_update)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_update(self, event):
        db = DataBaseOperator(self.user_id)
        memo_id     = self.id_updated
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
            db.update_memo_information(memo_id, memo_date, memo_place, memo_happen)
            # 跳出一个对话框
            dlg = wx.MessageDialog(self.p, u'更新成功',
                                   'Success',
                                   wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()                            

    def on_cancel(self, event):
        self.Close()

