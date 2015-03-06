# coding: utf-8

'''
布局模板:
'''
import wx

def arrangement(p, label_entry_tuple, dvlc, column_width_tuple, button_tuple):
    '''
    适用于通讯录界面,备忘录界面,日志界面,消费界面,朋友界面
    p 为panel
    label_entry_tuple 标签和输入组合,供用户输入检索条件使用
    dvlc              数据浏览表格
    column_tuple      保存着列名和长度的元组
    button_tuple      保存着按键的元组
    '''
    # 本界面要用到的布局管理器
    main_sizer   = wx.BoxSizer(wx.VERTICAL)
    input_sizer  = wx.BoxSizer()
    button_sizer = wx.BoxSizer()

    # 先将标签和文本控件交替添加到input_sizer中
    for label, entry in label_entry_tuple:
        input_sizer.Add(label, border = 5)
        input_sizer.Add(entry,
                        proportion = 1, flag = wx.ALL | wx.EXPAND, border = 5)        

    # 接下来是添加列到数据浏览列表控件
    for column_name, width in column_width_tuple:
        dvlc.AppendTextColumn(column_name, width = width)

    # 最后是将按键添加到button_sizer中
    for button in button_tuple:
        button_sizer.Add(button, border = 5)

    # 最后将这些组建全都添加到主布局管理器中并设置
    main_sizer.Add(input_sizer, flag = wx.ALL | wx.EXPAND, border = 5)
    main_sizer.Add(dvlc, proportion = 1, flag = wx.EXPAND | wx.ALL, border = 5)
    main_sizer.Add(button_sizer, flag = wx.ALL | wx.ALIGN_CENTER, border = 5)

    p.SetSizer(main_sizer)


# ----------------------------子界面布局模板---------------------------------

def sub_arrangement(p, main_sizer, label_entry_tuple, button_tuple):
    '''
    适用于所有子界面
    p 为panel
    main_sizer 为p的main_sizer,传入这个参数是为了让main_sizer能动态适应主框架frame的变化
    label_entry_tuple 标签和输入组合,供用户输入检索条件使用
    button_tuple      保存着按键的元组    
    '''
    # 本界面要用到的布局管理器
    input_sizer  = wx.BoxSizer(wx.VERTICAL)
    button_sizer = wx.BoxSizer()

    # 先将标签和文本控件交替添加到input_sizer中
    for label, entry in label_entry_tuple:
        input_sizer.Add(label, border = 5)
        input_sizer.Add(entry,
                        proportion = 1, flag = wx.ALL | wx.EXPAND, border = 5)        

    # 最后是将按键添加到button_sizer中
    for button in button_tuple:
        button_sizer.Add(button, border = 5)

    # 最后将这些组建全都添加到主布局管理器中并设置
    main_sizer.Add(input_sizer, flag = wx.ALL | wx.EXPAND, border = 5)
    main_sizer.Add(button_sizer, flag = wx.ALL | wx.ALIGN_CENTER, border = 5)
    
    p.SetSizer(main_sizer)
