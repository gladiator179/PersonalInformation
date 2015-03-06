# -*- coding: utf-8 -*-
import wx
import wx.dataview as dv
from DataBaseOperator import DataBaseOperator
from arrange_model import arrangement
from MemoFrames.OnAddFrame import OnAddFrame
from MemoFrames.OnDeleteFrame import OnDeleteFrame
from MemoFrames.OnUpdateFrame import OnUpdateFrame

class MemoFrame(wx.Frame):
    '''
    这里是关于备忘录的相关界面
    '''
    def __init__(self, user_id, father = None):
        wx.Frame.__init__(self, father, title = u'备忘录')

        self.user_id = user_id
        self.result  = None

        # 面板初始化
        self.p = wx.Panel(self)

        # 下面是开始查找,添加新记录,删除记录和返回,更新记录的按键
        self.query_btn        = wx.Button(self.p, label = u'检索')
        self.sort_btn         = wx.Button(self.p, label = u'排序')
        self.add_btn          = wx.Button(self.p, label = u'添加备忘录')
        self.delete_btn       = wx.Button(self.p, label = u'删除备忘录')
        self.update_btn       = wx.Button(self.p, label = u'更新备忘录')
        self.quit_btn         = wx.Button(self.p, label = u'返回')

        # 下面是浏览表格的组件
        self.dvlc = dv.DataViewListCtrl(self.p)
        
        # 下面是输入的组件,这里让用户输入的是备忘日期
        self.date_entry = wx.TextCtrl(self.p)

        # 调用类里面的布局函数
        self.__arrangement()

        # 调用类里面的函数进行按键响应设置
        self.__set_events()

    def __arrangement(self):

        # 标签,文本输入控件
        date_label      = wx.StaticText(self.p, 
                                        label = u'备忘日期(格式:xxxx-xx-xx or xxxx-xx)')
        label_entry_tuple = []
        label_entry_tuple.append((date_label, self.date_entry))
        label_entry_tuple = tuple(label_entry_tuple)


        # 接下来是添加数据浏览列表控件
        column_width_tuple = (
            (u'备忘录id'  , 100),
            (u'日期'      , 100),
            (u'地点'      , 200),
            (u'事件'      , 200)
        )

        button_tuple = []
        button_tuple.append(self.query_btn)
        button_tuple.append(self.sort_btn)
        button_tuple.append(self.add_btn)
        button_tuple.append(self.delete_btn)
        button_tuple.append(self.update_btn)
        button_tuple.append(self.quit_btn)
        button_tuple = tuple(button_tuple)

        # 调用布局模板中的函数
        arrangement(p = self.p, label_entry_tuple = label_entry_tuple,
                    dvlc = self.dvlc, column_width_tuple = column_width_tuple,
                    button_tuple = button_tuple)        

        self.SetSize((800, 600))
        self.Center()

# ----------------------- 按键响应函数 ------------------------------------

    def __set_events(self):
        self.query_btn.Bind(wx.EVT_BUTTON, self.on_query)
        self.sort_btn.Bind(wx.EVT_BUTTON, self.on_sort)
        self.add_btn.Bind(wx.EVT_BUTTON, self.on_add)
        self.delete_btn.Bind(wx.EVT_BUTTON, self.on_delete)
        self.update_btn.Bind(wx.EVT_BUTTON, self.on_update)
        self.quit_btn.Bind(wx.EVT_BUTTON, self.on_quit)

    def on_query(self, event):
        '''
        当这个按键被按下之后,就会直接进入查询,并将查询
        结果返回输出
        '''
        # 下面是输入的组件,这里让用户输入的是备忘日期
        date = self.date_entry.GetValue()
        db   = DataBaseOperator(self.user_id)
        result = db.get_memo_information(date)

        # 保存这个结果，以供排序使用
        self.result = result
        # 接下来要对结果的列表进行处理,添加到self.dvlc中
        self.dvlc.DeleteAllItems()

        for item in result:
            item = list(item)
            item[0] = str(item[0])
            item[1] = str(item[1])
            item = tuple(item)
            self.dvlc.AppendItem(item)

    def on_sort(self, event):
        '''
        当这个按键被按下之后,检索到的数据项会按备忘日期排序,
        默认是按id号排序
        '''
        if not self.result:
            # 弹出对话框提醒用户输入有误
            dlg = wx.MessageDialog(self.p, u'请先进行检索!',
                                   'ERROR',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()                    
        else:
            # 按照备忘日期排序
            result = list(self.result)
            result.sort(key = lambda x:x[1])
            result = tuple(result)
        
            # 先删除item中的所有项
            self.dvlc.DeleteAllItems()
            for item in result:
                # 要先对item中的第一项变为整形
                item = list(item)
                item[0] = str(item[0])
                item[1] = str(item[1])
                item = tuple(item)
                self.dvlc.AppendItem(item)                    

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
        当这个按键被按下之后,会进入更新界面
        '''
        id_updated = self.dvlc.GetTextValue(self.dvlc.GetSelectedRow(), 0)
        on_update_frame = OnUpdateFrame(self.user_id, id_updated, self)
        on_update_frame.Show()

    def on_quit(self, event):
        '''
        当这个按键被按下之后,就会退出本界面
        '''
        self.Close()
    

if __name__ == '__main__':
    app = wx.App()
    memo_frame = MemoFrame()
    memo_frame.Show()
    app.MainLoop()
