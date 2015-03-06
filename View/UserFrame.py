#coding: utf-8
import wx

from FriendFrame      import FriendFrame
from AddressListFrame import AddressListFrame
from MemoFrame        import MemoFrame
from JournalFrame     import JournalFrame
from PersonalFrame    import PersonalFrame

class UserFrame(wx.Frame):
    '''
    用户登录后的主界面
    '''
    def __init__(self, user_id):
        wx.Frame.__init__(self, None, title = u'欢迎')
        self.user_id          = user_id
        self.friend_btn       = None
        self.address_list_btn = None
        self.memory_btn       = None
        self.journey_btn      = None
        self.personal_btn     = None
        # 调用类里面的布局函数进行布局
        self.__arrangement()
        # 调用类里面的函数进行按键响应设置
        self.__set_events()

    def __arrangement(self):
        self.Center()
        self.SetSize((790, 494))
        self.SetMaxSize((790, 494))
        self.SetMinSize((790, 494))
        p = wx.Panel(self)

        # 设置背景图片
        jpg = wx.Image('User.jpg', type = wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        wx.StaticBitmap(p, bitmap = jpg)

        # 本界面要用到的布局管理器
        # 其中每个子布局管理器都是由一个按钮和按钮对应的描述组成(title_sizer 除外)
        main_sizer    = wx.BoxSizer(wx.VERTICAL)
        friend_sizer  = wx.BoxSizer()
        address_sizer = wx.BoxSizer()
        memory_sizer  = wx.BoxSizer()
        journey_sizer = wx.BoxSizer()
        title_sizer   = wx.BoxSizer()
        personal_sizer= wx.BoxSizer()

        self.friend_btn       = wx.Button(p, label = u'朋友')
        self.address_list_btn = wx.Button(p, label = u'通讯录')
        self.memory_btn       = wx.Button(p, label = u'备忘录')
        self.journey_btn      = wx.Button(p, label = u'日志')
        self.personal_btn     = wx.Button(p, label = u'个人信息')

        font = wx.Font(23, wx.SWISS, wx.BOLD, wx.NORMAL)
        title_label   = wx.StaticText(p, label = u'欢迎进入自己的世界')
        title_label.SetFont(font)
        title_label.SetForegroundColour('Yellow')

        # 初始化各个按键的描述文本
        friend_label  = wx.StaticText(p, 
                                      label = u'您可以在这里浏览并管理和朋友有关的信息')
        friend_label.SetForegroundColour('Red')
        address_label = wx.StaticText(p, 
                                      label = u'想要查找或管理自己的通讯录?就点这里吧')
        address_label.SetForegroundColour('Red')
        memory_label  = wx.StaticText(p, 
                                      label = u'为自己添加或者修改备忘录')
        memory_label.SetForegroundColour('Red')
        journey_label = wx.StaticText(p, 
                                      label = u'您可以在这里留下自己的回忆而不怕被窥视')
        journey_label.SetForegroundColour('Red')
        personal_label = wx.StaticText(p, 
                                      label = u'您可以通过它来查看自己的个人信息')
        personal_label.SetForegroundColour('Red')

        # 将各个组件添加到sizer中
        title_sizer.Add(title_label, flag = wx.ALIGN_CENTER)
        friend_sizer.Add(self.friend_btn, flag = wx.ALIGN_LEFT | wx.ALL, border = 10)
        friend_sizer.Add(friend_label, flag = wx.ALIGN_LEFT | wx.ALL, border = 10)
        address_sizer.Add(self.address_list_btn, flag = wx.ALIGN_LEFT | wx.ALL, border = 10)
        address_sizer.Add(address_label, flag = wx.ALIGN_LEFT | wx.ALL, border = 10)
        memory_sizer.Add(self.memory_btn, flag = wx.ALIGN_LEFT | wx.ALL, border = 10)
        memory_sizer.Add(memory_label, flag = wx.ALIGN_LEFT | wx.ALL, border = 10)
        journey_sizer.Add(self.journey_btn, flag = wx.ALIGN_LEFT | wx.ALL, border = 10)
        journey_sizer.Add(journey_label, flag = wx.ALIGN_LEFT | wx.ALL, border = 10)
        personal_sizer.Add(self.personal_btn, flag = wx.ALIGN_LEFT | wx.ALL, border = 10)
        personal_sizer.Add(personal_label, flag = wx.ALIGN_LEFT | wx.ALL, border = 10)
        
        main_sizer.Add(title_sizer, proportion = 3, flag = wx.ALL | wx.ALIGN_CENTER,
                       border = 10)
        main_sizer.Add(friend_sizer, proportion = 1, flag = wx.ALIGN_LEFT | wx.ALL,
                       border = 5)
        main_sizer.Add(address_sizer, proportion = 1, flag = wx.ALIGN_LEFT | wx.ALL,
                       border = 5)
        main_sizer.Add(memory_sizer, proportion = 1, flag = wx.ALIGN_LEFT | wx.ALL,
                       border = 5)
        main_sizer.Add(journey_sizer, proportion = 1, flag = wx.ALIGN_LEFT | wx.ALL,
                       border = 5)
        main_sizer.Add(personal_sizer, proportion = 1, flag = wx.ALIGN_LEFT | wx.ALL,
                       border = 5)

        p.SetSizer(main_sizer)

    def __set_events(self):
        '''
        本函数负责进行按键的绑定
        '''
        self.friend_btn.Bind(wx.EVT_BUTTON, self.on_friend)
        self.address_list_btn.Bind(wx.EVT_BUTTON, self.on_address_list)
        self.memory_btn.Bind(wx.EVT_BUTTON, self.on_memory)
        self.journey_btn.Bind(wx.EVT_BUTTON, self.on_journey)
        self.personal_btn.Bind(wx.EVT_BUTTON, self.on_personal)

    def on_friend(self, event):
        '''
        当这个按键被按下之后,就会进入朋友界面
        '''
        friend_frame = FriendFrame(self.user_id, self)
        friend_frame.Show()
        pass

    def on_address_list(self, event):
        '''
        当这个按键被按下之后,就会进入通讯录界面
        '''
        address_list_frame = AddressListFrame(self.user_id, self)
        address_list_frame.Show()
        pass

    def on_memory(self, event):
        '''
        当这个按键被按下之后,就会进入备忘录界面
        '''
        memory_frame = MemoFrame(self.user_id, self)
        memory_frame.Show()

    def on_journey(self, event):
        '''
        当这个按键被按下之后,就会进入日志界面
        '''
        journey_frame = JournalFrame(self.user_id, self)
        journey_frame.Show()

    def on_personal(self, event):
        '''
        当这个按键被按下之后,就会进入个人信息管理界面
        '''
        personal_frame = PersonalFrame(self.user_id, self)
        personal_frame.Show()
        pass

if __name__ == '__main__':
    app = wx.App()
    uf = UserFrame()
    uf.Show()
    app.MainLoop()
