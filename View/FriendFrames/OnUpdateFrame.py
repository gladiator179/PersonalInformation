# -*- coding: utf-8 -*-
import wx
import re
from arrange_model import sub_arrangement
from DataBaseOperator import DataBaseOperator

class OnUpdateFrame(wx.Frame):
    '''
    这里是关于朋友中更新朋友的界面
    '''
    def __init__(self, user_id, id_updated, father = None):
        wx.Frame.__init__(self, father, title = u'更新朋友')
        self.id_updated = id_updated
        self.user_id = user_id

        # 面板初始化
        self.p = wx.Panel(self)
        
        # 按键初始化
        self.update_btn    = wx.Button(self.p, label = u'更新')
        self.cancel_btn = wx.Button(self.p, label = u'返回')
        
        # 文本控件初始化
        self.f_name_entry      = wx.TextCtrl(self.p, size = (300, -1))
        self.f_know_date_entry = wx.TextCtrl(self.p, size = (300, -1))
        self.f_birth_entry     = wx.TextCtrl(self.p, size = (300, -1))
        self.f_email_entry     = wx.TextCtrl(self.p, size = (300, -1))
        self.f_qq_entry        = wx.TextCtrl(self.p, size = (300, -1))
        
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
        f_name_label      = wx.StaticText(self.p, label = u'姓名:')
        f_know_date_label = wx.StaticText(self.p, 
                                          label = u'认识时间段(小学,初中,高中,大学,工作)')
        f_birth_label     = wx.StaticText(self.p, label = u'生日(格式为xxxx-xx-xx)')
        f_email_label     = wx.StaticText(self.p, label = u'邮箱')
        f_qq_label        = wx.StaticText(self.p, label = u'qq号码')

        # 构造标签和输入控件
        label_entry_tuple = (
            (f_name_label     , self.f_name_entry),
            (f_know_date_label, self.f_know_date_entry),
            (f_birth_label    , self.f_birth_entry),
            (f_email_label    , self.f_email_entry),
            (f_qq_label       , self.f_qq_entry)
        )

        buttons = (self.update_btn, self.cancel_btn)
        
        sub_arrangement(self.p, main_sizer, label_entry_tuple, buttons)
        main_sizer.Fit(self)
        self.Center()

    def __set_entry_value(self):
        db = DataBaseOperator(self.user_id)
        # 通过id查询该成员所有信息,返回result
        result = db.id_get_friend_information(self.id_updated)
        print result
        self.f_name_entry.SetValue(result[1])
        self.f_know_date_entry.SetValue(result[2])
        self.f_birth_entry.SetValue(str(result[3]))
        self.f_email_entry.SetValue(result[4])
        self.f_qq_entry.SetValue(result[5])


    def __set_events(self):
        self.update_btn.Bind(wx.EVT_BUTTON, self.on_update)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

# -------------------------- 按键响应组件 ------------------------------------

    def on_update(self, event):
        '''
        当这个按键被按下之后,就可以添加一条朋友记录
        '''
        f_id      = self.id_updated
        name      = self.f_name_entry.GetValue()
        know_date = self.f_know_date_entry.GetValue()
        birth     = self.f_birth_entry.GetValue()
        email     = self.f_email_entry.GetValue()
        qq        = self.f_qq_entry.GetValue()

        p = re.compile(r'\d\d\d\d-\d\d-\d\d')
        # 判断生日输入是否合理，要用到正则表达式。。
        if not name:
            # 跳出一个对话框
            dlg = wx.MessageDialog(self.p, u'姓名不能为空',
                                   'Error',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()                        

        elif not p.match(birth):
            # 跳出一个对话框
            dlg = wx.MessageDialog(self.p, u'生日输入格式有误,请重新输入(不能为空)',
                                   'Error',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()                        
        else:
            # 先判断数据是否合理
            test_l  = [u'小学', u'初中', u'高中', u'大学', u'工作单位', '']
            if know_date not in test_l:
                # 跳出一个对话框
                dlg = wx.MessageDialog(self.p, u'认识日期输入有误,请重新输入',
                                       'Error',
                                       wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()            
            else:
                db = DataBaseOperator(self.user_id)
                db.update_friend_information(f_id, name, know_date, birth, email, qq)
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
