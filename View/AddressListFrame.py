#coding: utf-8
'''
本模块是对通讯录界面的描述
'''
import wx
import wx.dataview as dv
from arrange_model import arrangement
from DataBaseOperator import DataBaseOperator
from AddressListFrames.OnAddFrame import OnAddFrame
from AddressListFrames.OnUpdateFrame import OnUpdateFrame
from AddressListFrames.OnDeleteFrame import OnDeleteFrame

class AddressListFrame(wx.Frame):
    def __init__(self, user_id, father = None):
        wx.Frame.__init__(self, father, title = u'通讯录管理')

        self.user_id = user_id
        self.result = None     # 该属性保存检索结果，供排序使用
        self.p = wx.Panel(self)

        # 下面是添加新记录,更新记录,删除记录和返回,开始查找的按键
        self.add_btn    = wx.Button(self.p, label = u'添加记录')
        self.delete_btn = wx.Button(self.p, label = u'删除记录')
        self.update_btn = wx.Button(self.p, label = u'更新记录')
        self.cancel_btn = wx.Button(self.p, label = u'返回')
        self.query_btn  = wx.Button(self.p, label = u'开始查找')
        self.sort_btn   = wx.Button(self.p, label = u'排序')

        # 下面是浏览表格的组件
        self.dvlc = dv.DataViewListCtrl(self.p)
        
        # 姓名输入组件
        self.name_entry = wx.TextCtrl(self.p)

        # 调用类里面的布局函数
        self.__arrangement()

        # 调用类里面的函数进行按键响应设置
        self.__set_events()

    def __arrangement(self):

        name_label      = wx.StaticText(self.p, label = u'姓名')
        # 标签,文本输入控件
        label_entry_tuple = []
        label_entry_tuple.append((name_label, self.name_entry))
        label_entry_tuple = tuple(label_entry_tuple)

        # 接下来是添加数据浏览列表控件
        column_width_tuple = (
            (u'id'        , 100),
            (u'姓名'      , 100),
            (u'电话号码'  , 200)
        )
        
        button_tuple = []
        button_tuple.append(self.query_btn)
        button_tuple.append(self.sort_btn)
        button_tuple.append(self.add_btn)
        button_tuple.append(self.delete_btn)
        button_tuple.append(self.update_btn)
        button_tuple.append(self.cancel_btn)
        button_tuple = tuple(button_tuple)

        # 调用布局模板中的函数
        arrangement(p = self.p, label_entry_tuple = label_entry_tuple,
                    dvlc = self.dvlc, column_width_tuple = column_width_tuple,
                    button_tuple = button_tuple)

        self.SetSize((800, 600))
        self.Center()

    def __set_events(self):
        '''
        本函数负责进行按键的绑定
        '''                    
        self.add_btn.Bind(wx.EVT_BUTTON, self.on_add)
        self.delete_btn.Bind(wx.EVT_BUTTON, self.on_delete)
        self.update_btn.Bind(wx.EVT_BUTTON, self.on_update)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.query_btn.Bind(wx.EVT_BUTTON, self.on_query)
        self.sort_btn.Bind(wx.EVT_BUTTON, self.on_sort)

# ----------------------- 按键响应函数 ------------------------------------

    def on_add(self, event):
        '''
        当这个按键按下之后,就会跳出一个窗口,问用户要添加的记录
        '''
        on_add_frame = OnAddFrame(self.user_id)
        on_add_frame.Show()

    def on_delete(self, event):
        '''
        当这个按键被按下之后,就会跳出一个窗口,问用户要删除的记录
        '''
        on_delete_frame = OnDeleteFrame(self.user_id)
        on_delete_frame.Show()

    def on_update(self, event):
        '''
        当这个按键被按下之后,会进入更新界面
        '''
        id_updated = self.dvlc.GetTextValue(self.dvlc.GetSelectedRow(), 0)
        on_update_frame = OnUpdateFrame(self.user_id, id_updated, self)
        on_update_frame.Show()

    def on_cancel(self, event):
        '''
        当这个按键被按下之后,会退出本界面
        '''
        self.Close()

    def on_query(self, event):
        '''
        当按键被按下之后,会进行检索
        '''
        db     = DataBaseOperator(self.user_id)
        name   = self.name_entry.GetValue()
        result = db.get_address_list_information(name)

        # 保存这个结果，以供排序使用
        self.result = result

        # 先删除item中的所有项
        self.dvlc.DeleteAllItems()

        for item in result:
            # 要记得先对item进行变形
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
                item[3] = str(item[3])
                item = tuple(item)
                self.dvlc.AppendItem(item)            

if __name__ == '__main__':
    app = wx.App()
    address_list_frame = AddressListFrame(1)
    address_list_frame.Show()
    app.MainLoop()
