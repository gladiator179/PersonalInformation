# -*- coding: utf-8 -*-
import wx
from DataBaseOperator import DataBaseOperator

class OnViewFrame(wx.Frame):
    '''
    这是真正浏览日志的界面
    '''
    def __init__(self, user_id, id_viewed, father = None):
        self.user_id = user_id
        self.id_viewed = id_viewed

        wx.Frame.__init__(self, father, title = u'编写日志')
        self.p = wx.Panel(self)

        # 按键初始化
        self.quit_btn         = wx.Button(self.p, label = u'返回')
        

        # 标签,还差设置值的工作
        self.subject_label    = wx.StaticText(self.p, label = u'测试状态')
        self.type_label       = wx.StaticText(self.p, label = u'测试状态')
        self.content_label    = wx.StaticText(self.p, label = u'测试状态')

        # 调用私有函数进行标签的值的设置
        self.__set_label_value()

        # 调用类的私有函数进行布局
        self.__arrangement()


        # 进行按键响应设置
        self.__set_event()

    def __set_label_value(self):
        db = DataBaseOperator(self.user_id)
        # 根据要更新的id号进行查询,获得结果
        result = db.id_get_journal_information(self.id_viewed)

        # 根据结果更新文本域
        self.subject_label.SetLabelText(result[0])
        self.type_label.SetLabelText(result[1])
        self.content_label.SetLabelText(result[2])

        
    def __arrangement(self):
        main_sizer   = wx.BoxSizer(wx.VERTICAL)
        input_sizer  = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.BoxSizer()

        # 初始化标签
        subject_label = wx.StaticText(self.p, label = u'主题')
        type_label    = wx.StaticText(self.p, label = u'类型')
        content_label = wx.StaticText(self.p, label = u'内容')

        # 将标签和输入文本添加到input_sizer中
        input_sizer.Add(subject_label, border = 5)
        input_sizer.Add(self.subject_label, proportion = 1, 
                        flag = wx.ALL | wx.EXPAND, border = 5)
        input_sizer.Add(type_label, border = 5)
        input_sizer.Add(self.type_label, proportion = 1,
                        flag = wx.ALL | wx.EXPAND, border = 5)
        input_sizer.Add(content_label, border = 5)
        input_sizer.Add(self.content_label, proportion = 3,
                        flag = wx.ALL | wx.EXPAND, border = 5)
        
        # 将按键都添加到button_sizer中
        button_sizer.Add(self.quit_btn, border = 5)

        main_sizer.Add(input_sizer, flag = wx.ALL | wx.EXPAND, border = 5)
        main_sizer.Add(button_sizer, flag = wx.ALL | wx.ALIGN_CENTER, border = 5)

        self.p.SetSizer(main_sizer)
        main_sizer.Fit(self)


    def __set_event(self):
        self.quit_btn.Bind(wx.EVT_BUTTON, self.on_quit)

# ------------------------按键响应方法--------------------------------------

    def on_quit(self, event):
        '''
        该按键按下之后,就会退出
        '''
        self.Close()



