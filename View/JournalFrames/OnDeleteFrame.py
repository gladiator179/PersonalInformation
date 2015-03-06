# -*- coding: utf-8 -*-
import wx
from DataBaseOperator import DataBaseOperator
from SubDeleteFrame   import SubDeleteFrame

class OnDeleteFrame(SubDeleteFrame):
    '''
    这里是关于日志中删除日志的界面
    '''
    def __init__(self, user_id, father = None):
        super(OnDeleteFrame, self).__init__(user_id, father)

# ------------------------重写按键响应方法--------------------------------------
    def on_delete(self, event):
        db = DataBaseOperator(self.user_id)
        db.delete_journal_information(int(self.id_entry.GetValue()))
        # 跳出一个对话框
        dlg = wx.MessageDialog(self.p, u'删除成功',
                               'Success',
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()                    
