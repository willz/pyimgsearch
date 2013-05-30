import wx

class FileDropTarget(wx.FileDropTarget):
    def __init__(self, obj):
        wx.FileDropTarget.__init__(self)
        # store the object reference for dropped files
        self.obj = obj

    def OnDropFiles(self, x, y, filenames):
        if len(filenames) == 1:
            # only support search one image at a time
            pass

class MainWindow(wx.Frame):
    """ This window displays the GUI widgets. """
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self.parent, wx.ID_ANY, title, size = (800, 600),
                          style = wx.DEFAULT_FRAME_STYLE)
        self.SetBackgroundColour(wx.WHITE)
        # Define a scroll window to show images and receive drop file
        self.panel = ScrolledWindow(self, -1, pos = (0, 0))
        # create a file drop target object
        dt = FileDropTarget(self.panel)
        self.panel.SetDropTarget(dt)
        # display the window
        self.show(True)

class MyApp(wx.App):
    def OnInit(self):
        frame = MainWindow(None, -1, "Image Search")
        self.SetTopWindow(frame)
        return True
        
app = MyApp(0)
app.MainLoop()
