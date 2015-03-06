# -*- coding: utf-8 -*-
#!/usr/bin/env python
''' 
本模块是对管理员界面的描述
'''
import wx
import wx.dataview as dv
from DataBaseOperator import DataBaseOperator

class AdminFrame(wx.Frame):
    def __init__(self, admin_id):
        wx.Frame.__init__(self, None, title = u'检索信息')
        self.result = None
        self.admin_id    = admin_id
        self.query_btn   = None
        self.sort_btn    = None
        self.empty_btn   = None
        self.quit_btn    = None
        self.dvlc        = None
        self.id_text     = None
        self.name_text   = None
        self.sex_text    = None
        self.age_text    = None 
        # 调用类里面的布局函数进行布局
        self.__arrangement()

        # 进行按键响应事件的绑定
        self.__set_event()

    def __arrangement(self):
        self.SetSize((800, 600))
        self.Center()
        p = wx.Panel(self)

        # 本界面要用到的布局管理器
        main_sizer   = wx.BoxSizer(wx.VERTICAL)
        input_sizer  = wx.BoxSizer()
        button_sizer = wx.BoxSizer()
        
        name_label      = wx.StaticText(p, label = u'姓名')
        self.name_text  = wx.TextCtrl(p)
        sex_label       = wx.StaticText(p, label = u'性别')
        self.sex_text   = wx.TextCtrl(p)

        # 先将这些标签和文本控件交替添加到input_sizer中
        input_sizer.Add(name_label, border = 5)
        input_sizer.Add(self.name_text, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 5)
        input_sizer.Add(sex_label, border = 5)
        input_sizer.Add(self.sex_text, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 5)

        # 接下来是添加数据浏览列表控件
        dvlc = dv.DataViewListCtrl(p)
        column_width_list = [
            (u'id'      , 100),
            (u'姓名'    , 100),
            (u'性别'    , 40),
            (u'邮箱'    , 200),
            (u'电话号码', 200),
        ]
        for column_name, width in column_width_list:
            dvlc.AppendTextColumn(column_name, width = width)
        self.dvlc = dvlc

        # 接下来是按键的处理
        self.query_btn = wx.Button(p, label = u'查询')
        self.sort_btn  = wx.Button(p, label = u'排序')        
        self.empty_btn = wx.Button(p, label = u'清空')
        self.quit_btn  = wx.Button(p, label = u'退出')
        button_sizer.Add(self.query_btn,  border = 5)
        button_sizer.Add(self.sort_btn,  border = 5)
        button_sizer.Add(self.empty_btn,  border = 5)
        button_sizer.Add(self.quit_btn,   border = 5)

        # 最后将这些组建全都添加到主布局管理器中并设置
        main_sizer.Add(input_sizer, flag = wx.ALL | wx.EXPAND, border = 5)
        main_sizer.Add(dvlc, proportion = 1, flag = wx.EXPAND | wx.ALL, border = 5)
        main_sizer.Add(button_sizer, flag = wx.ALL | wx.ALIGN_CENTER, border = 5)

        p.SetSizer(main_sizer)

    def __set_event(self):
        self.query_btn.Bind(wx.EVT_BUTTON, self.on_query)
        self.sort_btn.Bind(wx.EVT_BUTTON, self.on_sort)
        self.empty_btn.Bind(wx.EVT_BUTTON, self.on_empty)
        self.quit_btn.Bind(wx.EVT_BUTTON, self.on_quit)

    def on_query(self, event):
        # 获取所有的输入值
        name_value = self.name_text.GetValue()
        sex_value  = self.sex_text.GetValue()

        # 记得要先判断sex_value是否满足条件
        valid_sex_value = ('男','女')
        if sex_value not in valid_sex_value:
            # 跳出一个对话框提醒用户重输入
            # 弹出对话框提醒用户输入有误
            dlg = wx.MessageDialog(self.p, u'性别只能为男或女!',
                                   'ERROR',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()                                
        
        else:
            db = DataBaseOperator()
            result = db.get_user_basic_information(name_value, sex_value)
            # 保存这个结果，以供排序使用
            self.result = result

            # 将信息添加进self.dvlc
            self.dvlc.DeleteAllItems()
            for item in result:
                item = list(item)
                item[0] = str(item[0])
                item = tuple(item)
                self.dvlc.AppendItem(item)

    def on_sort(self, event):
        '''
        当这个按键被按下之后，就会对self.result进行排序，然后反映
        到self.dvlc中
        '''
        if not self.result:
            # 弹出对话框提醒用户输入有误
            dlg = wx.MessageDialog(self.p, u'请先进行检索!',
                                   'ERROR',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()                    
        else:
            # 按照人名排序
            result = list(self.result)
            # 将result中的人名转变为gb2312编码排序，然后转回unicode编码
            for i in range(len(result)):
                result[i] = list(result[i])
                result[i][1] = result[i][1].encode('gbk')

            # 将人名按照gbk编码的方式进行排序
            result.sort(key = lambda x:x[1])

            # 再将排好序的gbk编码转回unicode编码,再将其转回元组类型以保护数据
            for i in range(len(result)):
                result[i][1] = result[i][1].decode('gbk')
                result[i] = tuple(result[i])
            result = tuple(result)

            # 先删除item中的所有项
            self.dvlc.DeleteAllItems()
            for item in result:
                # 要先对item中的第一项变为整形
                item = list(item)
                item[0] = str(item[0])
                item = tuple(item)
                self.dvlc.AppendItem(item)            
        
    def on_empty(self, event):
        self.name_text.SetValue("")
        self.sex_text.SetValue("")

    def on_quit(self, event):
        self.Close()

if __name__ == '__main__':
    app = wx.App()
    admin_frame = AdminFrame()
    admin_frame.Show()
    app.MainLoop()
