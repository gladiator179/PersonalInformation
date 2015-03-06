# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''
本模块是对朋友相关界面的描述
'''
import wx
import wx.dataview as dv
from arrange_model import arrangement
from DataBaseOperator import DataBaseOperator
from FriendFrames.OnAddFrame import OnAddFrame
from FriendFrames.OnDeleteFrame import OnDeleteFrame
from FriendFrames.OnUpdateFrame import OnUpdateFrame

class FriendFrame(wx.Frame):
    def __init__(self, user_id, father = None):
        wx.Frame.__init__(self, father, title = u'朋友')

        self.user_id = user_id
        self.result = None     # 该属性保存检索结果，供排序使用

        # 面板初始化
        self.p = wx.Panel(self)

        # 按键的初始化
        self.query_btn         = wx.Button(self.p, label = u'检索')
        self.sort_btn          = wx.Button(self.p, label = u'排序')
        self.quit_btn          = wx.Button(self.p, label = u'返回')
        self.add_btn           = wx.Button(self.p, label = u'添加')
        self.delete_btn        = wx.Button(self.p, label = u'删除')
        self.update_btn        = wx.Button(self.p, label = u'更新')
        
        # 姓名和认识时间文本框初始化
        self.name_entry      = wx.TextCtrl(self.p)
        self.know_date_entry = wx.TextCtrl(self.p)

        # 数据显示表格初始化
        self.dvlc = dv.DataViewListCtrl(self.p)

        # 调用类里面的布局函数进行布局
        self.__arrangement()

        # 调用类里面的函数进行按键响应设置
        self.__set_events()

    def __arrangement(self):

        # 构造相关参数然后调用arrangement函数进行布局
        name_label           = wx.StaticText(self.p, label = u'姓名')
        know_date_label      = wx.StaticText(self.p, 
                                             label = u'认识时间(只能为小学,初中,高中,大学,工作单位)')
        label_entry_tuple = []
        label_entry_tuple.append((name_label, self.name_entry))
        label_entry_tuple.append((know_date_label, self.know_date_entry))
        label_entry_tuple = tuple(label_entry_tuple)
        
        column_width_tuple = (
            (u'id'      , 100),
            (u'姓名'    , 100),
            (u'认识时间', 100),
            (u'生日'    , 100),
            (u'邮箱'    , 200),
            (u'qq号'    , 150)
        )

        button_tuple = []
        button_tuple.append(self.query_btn)
        button_tuple.append(self.sort_btn)
        button_tuple.append(self.add_btn)
        button_tuple.append(self.delete_btn)
        button_tuple.append(self.update_btn)
        button_tuple.append(self.quit_btn)
        button_tuple = tuple(button_tuple)

        # 调用布局函数进行统一布局
        arrangement(self.p, label_entry_tuple = label_entry_tuple,
                    dvlc = self.dvlc, column_width_tuple = column_width_tuple,
                    button_tuple = button_tuple)

        self.SetSize((800,600))
        self.Center()

    def __set_events(self):
        self.query_btn.Bind(wx.EVT_BUTTON, self.on_query)
        self.quit_btn.Bind(wx.EVT_BUTTON, self.on_quit)
        self.add_btn.Bind(wx.EVT_BUTTON, self.on_add)
        self.delete_btn.Bind(wx.EVT_BUTTON, self.on_delete)
        self.update_btn.Bind(wx.EVT_BUTTON, self.on_update)
        self.sort_btn.Bind(wx.EVT_BUTTON, self.on_sort)

# ----------------------- 按键响应函数 ------------------------------------
    def on_query(self, event):
        '''
        当这个按键被按下之后,就会直接进入查询,并将查询
        结果返回输出
        '''
        name      = self.name_entry.GetValue()
        know_date = self.know_date_entry.GetValue()
        l = [u'小学', u'初中', u'高中', u'大学', u'工作单位', u'']
        if know_date not in l:
            # 弹出对话框提醒用户输入有误
            dlg = wx.MessageDialog(self.p, u'认识时间输入有误!',
                                   'ERROR',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()        
        else:
            db = DataBaseOperator(self.user_id)
            result = db.get_friend_information(name, know_date)

            # 保存这个结果，以供排序使用
            self.result = result

            # 先删除item中的所有项
            self.dvlc.DeleteAllItems()
            for item in result:
                # 要先对item中的第一项变为整形
                item = list(item)
                item[0] = str(item[0])
                item[3] = str(item[3])
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
                item[3] = str(item[3])
                item = tuple(item)
                self.dvlc.AppendItem(item)            

    def on_quit(self, event):
        '''
        当这个按键被按下之后,就会退出本界面
        '''
        self.Close()

    def on_add(self, event):
        '''
        当这个按键被按下之后,就会跳出一个窗口,问用户要添加什么样的人
        '''
        on_add_frame = OnAddFrame(self.user_id, self)
        on_add_frame.Show()

    def on_delete(self, event):
        '''
        当这个按键被按下之后,就会跳出一个窗口,问用户要删除什么样的人
        '''
        on_delete_frame = OnDeleteFrame(self.user_id, self)
        on_delete_frame.Show()
        
    def on_update(self, event):
        '''
        当这个按键被按下之后,就会跳出一个窗口,问用户要更新什么数据
        '''
        id_updated =  self.dvlc.GetTextValue(self.dvlc.GetSelectedRow(), 0).encode('utf-8')
        on_update_frame = OnUpdateFrame(self.user_id, id_updated, self)
        on_update_frame.Show()



if __name__ == '__main__':
    app = wx.App()
    friend_frame = FriendFrame(1)
    friend_frame.Show()
    app.MainLoop()
