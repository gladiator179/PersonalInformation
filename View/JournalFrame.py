# -*- coding: utf-8 -*-
#!/usr/bin/env python
''' 
本模块是对日志检索界面的描述
'''
import wx
import wx.dataview as dv
from arrange_model import arrangement
from DataBaseOperator import DataBaseOperator
from JournalFrames.OnAddFrame    import OnAddFrame
from JournalFrames.OnDeleteFrame import OnDeleteFrame
from JournalFrames.OnViewFrame   import OnViewFrame
from JournalFrames.OnEditFrame   import OnEditFrame

class JournalFrame(wx.Frame):
    def __init__(self, user_id, father = None):
        wx.Frame.__init__(self, father, title = u'日志信息')
        self.user_id = user_id
        self.result = None     # 该属性保存检索结果，供排序使用        
        self.p       = wx.Panel(self)

        # 按键初始化
        self.query_btn        = wx.Button(self.p, label = u'检索')
        self.sort_btn          = wx.Button(self.p, label = u'排序')
        self.edit_btn         = wx.Button(self.p, label = u'编辑')
        self.add_btn          = wx.Button(self.p, label = u'写日记')
        self.delete_btn       = wx.Button(self.p, label = u'删除日记')
        self.view_btn         = wx.Button(self.p, label = u'查看日记内容')
        self.quit_btn         = wx.Button(self.p, label = u'返回')

        # 类型输入文本
        self.type_entry = wx.TextCtrl(self.p)

        # 数据浏览控件
        self.dvlc = dv.DataViewListCtrl(self.p)

        # 调用类里面的布局函数进行布局
        self.__arrangement()

        # 调用类里面的函数进行按键响应设置
        self.__set_events()

    def __arrangement(self):
        # 标签,文本输入控件
        type_label      = wx.StaticText(self.p, label = u'分类(若不填写则为默认)')
        label_entry_tuple = []
        label_entry_tuple.append((type_label, self.type_entry))
        label_entry_tuple = tuple(label_entry_tuple)

        # 接下来是添加数据浏览列表控件
        column_width_tuple = (
            (u'id'      , 100),
            (u'主题'    , 100),
            (u'修改时间', 100),
            (u'类型'    , 100),
        )

        button_tuple = []
        button_tuple.append(self.query_btn)
        button_tuple.append(self.sort_btn)
        button_tuple.append(self.edit_btn)
        button_tuple.append(self.add_btn)
        button_tuple.append(self.delete_btn)
        button_tuple.append(self.view_btn)
        button_tuple.append(self.quit_btn)
        button_tuple = tuple(button_tuple)

        # 调用布局模板中的函数
        arrangement(p = self.p, label_entry_tuple = label_entry_tuple,
                    dvlc = self.dvlc, column_width_tuple = column_width_tuple,
                    button_tuple = button_tuple)

        self.SetSize((800, 600))
        self.Center()

    def __set_events(self):
        self.query_btn.Bind(wx.EVT_BUTTON, self.on_query)
        self.edit_btn.Bind(wx.EVT_BUTTON, self.on_edit)
        self.add_btn.Bind(wx.EVT_BUTTON, self.on_add)
        self.delete_btn.Bind(wx.EVT_BUTTON, self.on_delete)
        self.view_btn.Bind(wx.EVT_BUTTON, self.on_view)
        self.quit_btn.Bind(wx.EVT_BUTTON, self.on_quit)
        self.sort_btn.Bind(wx.EVT_BUTTON, self.on_sort)

# -------------------------- 按键响应部分 --------------------------------------

    def on_query(self, event):
        '''
        当这个按键被按下之后,就会直接进入查询,并将查询
        结果返回输出
        '''
        db = DataBaseOperator(self.user_id)
        date = self.type_entry.GetValue()
        result = db.get_journal_information(date)

        # 保存这个结果，以供排序使用
        self.result = result

        # 还差添加进列表的操作
        self.dvlc.DeleteAllItems()

        for item in result:
            item = list(item)
            item[0] = str(item[0])
            item[2] = str(item[2])
            item = tuple(item)
            self.dvlc.AppendItem(item)

    def on_edit(self, event):
        '''
        当这个按键按下之后,将会获得日志id号，然后进入日志编辑界面
        '''
        id_updated = self.dvlc.GetTextValue(self.dvlc.GetSelectedRow(), 0)

        on_edit_frame = OnEditFrame(self.user_id, id_updated, self)
        on_edit_frame.Show()


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
            # 按照主题排序
            result = list(self.result)
            # 将result中的主题转变为gb2312编码排序，然后转回unicode编码
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
                item = list(item)
                item[0] = str(item[0])
                item[2] = str(item[2])
                item = tuple(item)
                self.dvlc.AppendItem(item)            


    def on_add(self, event):
        '''
        当这个按键被按下之后,就会跳出一个窗口,直接编写日志
        '''
        on_add_frame = OnAddFrame(self.user_id, self)
        on_add_frame.Show()

    def on_delete(self, event):
        '''
        当这个按键被按下之后,就会跳出一个窗口,问用户要删除的日志编号
        '''    
        on_delete_frame = OnDeleteFrame(self.user_id, self)
        on_delete_frame.Show()

    def on_view(self, event):
        '''
        当这个按键被按下之后,将会获得日志id号，然后进入日志编辑界面
        '''
        id_viewed = self.dvlc.GetTextValue(self.dvlc.GetSelectedRow(), 0)

        on_view_frame = OnViewFrame(self.user_id, id_viewed, self)
        on_view_frame.Show()

    def on_quit(self, event):
        '''
        当这个按键被按下之后,就会退出本界面
        '''
        self.Close()


if __name__ == '__main__':
    app = wx.App()
    journal_frame = JournalFrame(1)
    journal_frame.Show()
    app.MainLoop()
