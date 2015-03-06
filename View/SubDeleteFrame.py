# -*- coding: utf-8 -*-
'''
这里是在各大子模块(朋友,通讯录,备忘,日志,消费记录)
的删除界面,在各个具体的界面中都只要继承这个类,然后重写其删除方法即可
'''

import wx
from arrange_model    import sub_arrangement

class SubDeleteFrame(wx.Frame):
    '''
    这里是关于朋友中删除朋友的界面
    '''
    def __init__(self, user_id, father = None):
        wx.Frame.__init__(self, father, title = u'删除')
        self.user_id = user_id
        self.p       = wx.Panel(self)
        # 按键的初始化
        self.delete_btn        = wx.Button(self.p, label = u'删除')
        self.cancel_btn        = wx.Button(self.p, label = u'取消')        

        # 文本控件的初始化
        self.id_entry          = wx.TextCtrl(self.p)

        # 调用类里面的布局函数进行布局
        self.__arrangement()

        # 调用类里面的函数进行按键响应设置
        self.__set_events()        

    def __arrangement(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        id_label = wx.StaticText(self.p, label = u'要删除的id号')
        
        label_entry_tuple = (
            (id_label, self.id_entry),
        )
        
        buttons = (
            self.delete_btn,
            self.cancel_btn
        )

        sub_arrangement(self.p, main_sizer, label_entry_tuple, buttons)
        main_sizer.Fit(self)
        self.Center()

    def __set_events(self):
        self.delete_btn.Bind(wx.EVT_BUTTON, self.on_delete)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

# ------------------------按键响应--------------------------------------
    def on_delete(self, event):
        # 这个方法需要重写,其他都不用
        pass
    
    def on_cancel(self, event):
        self.Close()
