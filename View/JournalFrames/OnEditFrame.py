# -*- coding: utf-8 -*-
import wx
from DataBaseOperator import DataBaseOperator

class OnEditFrame(wx.Frame):
    '''
    这是真正编辑日志的界面
    '''
    def __init__(self, user_id, id_updated, father = None):
        self.id_updated = id_updated
        self.user_id = user_id
        wx.Frame.__init__(self, father, title = u'编写日志')
        self.p = wx.Panel(self)

        # 按键初始化
        self.edit_btn         = wx.Button(self.p, label = u'提交')
        self.quit_btn         = wx.Button(self.p, label = u'返回')
        
        # 输入文本,这里文本还差设置值的操作
        self.subject_entry    = wx.TextCtrl(self.p, size = (300, -1))
        self.type_entry       = wx.TextCtrl(self.p, size = (300, -1))
        self.content_entry    = wx.TextCtrl(self.p, size = (300, 300), 
                                            style = wx.TE_MULTILINE | wx.HSCROLL)
        # 调用类的私有函数进行布局
        self.__arrangement()

        # 调用私有函数进行文本域的值的设置
        self.__set_entry_value()

        # 进行按键响应设置
        self.__set_event()

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
        input_sizer.Add(self.subject_entry, proportion = 0, 
                        flag = wx.ALL | wx.EXPAND, border = 5)
        input_sizer.Add(type_label, border = 5)
        input_sizer.Add(self.type_entry, proportion = 0,
                        flag = wx.ALL | wx.EXPAND, border = 5)
        input_sizer.Add(content_label, border = 5)
        input_sizer.Add(self.content_entry, proportion = 1,
                        flag = wx.ALL | wx.EXPAND, border = 5)
        
        # 将按键都添加到button_sizer中
        button_sizer.Add(self.edit_btn, border = 5)
        button_sizer.Add(self.quit_btn, border = 5)

        main_sizer.Add(input_sizer, flag = wx.ALL | wx.EXPAND, border = 5)
        main_sizer.Add(button_sizer, flag = wx.ALL | wx.ALIGN_CENTER, border = 5)

        self.p.SetSizer(main_sizer)
        self.SetSize((800, 600))
        self.SetMinSize((800, 600))
        self.SetMaxSize((800, 600))

    def __set_entry_value(self):
        db = DataBaseOperator(self.user_id)
        # 根据要更新的id号进行查询,获得结果
        result = db.id_get_journal_information(self.id_updated)

        # 根据结果更新文本域
        self.subject_entry.SetValue(result[0])
        self.type_entry.SetValue(result[1])
        self.content_entry.SetValue(result[2])

    def __set_event(self):
        self.edit_btn.Bind(wx.EVT_BUTTON, self.on_edit)
        self.quit_btn.Bind(wx.EVT_BUTTON, self.on_quit)

# ------------------------按键响应方法--------------------------------------

    def on_edit(self, event):
        '''
        该按键被按下之后,就会更新一条日志到数据库中
        '''
        # 日志的id号隐藏在self.id_updated 中
        id_updated = self.id_updated
        j_subject = self.subject_entry.GetValue()
        j_content = self.content_entry.GetValue()
        j_type = self.type_entry.GetValue()

        # 先判断主题是否为空，若为空则提示出错
        if j_subject == '':
            # 跳出一个对话框
            dlg = wx.MessageDialog(self.p, u'日志主题不能为空,请重试',
                                   'Error',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()                        
        else:
            j_type = u'无' if not j_type else j_type

            db = DataBaseOperator(self.user_id)
            db.update_journal_information(id_updated, j_subject, j_content, j_type)
            # 跳出一个对话框
            dlg = wx.MessageDialog(self.p, u'日志更新成功',
                                   'Success',
                                   wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()                    
        

    def on_quit(self, event):
        '''
        该按键按下之后,就会退出
        '''
        self.Close()
