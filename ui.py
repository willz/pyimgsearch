import wx
import imgbase

class FileDropTarget(wx.FileDropTarget):
    def __init__(self, obj):
        wx.FileDropTarget.__init__(self)
        # store the object reference for dropped files
        self.obj = obj

    def OnDropFiles(self, x, y, filenames):
        if len(filenames) == 1:
            # only support search one image at a time
            self.obj.SearchImage(filenames[0])
            pass

class MainWindow(wx.Frame):
    """ This window displays the GUI widgets. """
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size = (512, 512),
                          style = wx.DEFAULT_FRAME_STYLE)
        self.SetBackgroundColour(wx.WHITE)
        # Define a scroll window to show images and receive drop file
        self.panel = wx.Panel(self, -1, (512, 512), style = wx.SUNKEN_BORDER | wx.ALIGN_CENTER)
        # create a file drop target object
        dt = FileDropTarget(self)
        self.SetDropTarget(dt)
        # show text
        txt = wx.StaticText(self.panel, -1, label = 'Drag file here', style = wx.ALIGN_CENTER)
        font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        txt.SetFont(font)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer((250, 225))
        vbox.Add(txt, 0, wx.CENTER)
        self.panel.SetSizer(vbox)
        self.panel.Fit()
        self.panel.Show(True)
        # display the window
        self.imgbase = imgbase.ImgBase()
        self.imgbase.build_index()

    def SearchImage(self, file_name):
        rows, cols = 8, 8
        sizer = wx.GridSizer(rows, cols, 0, 0)
        res = self.imgbase.search(file_name)
        for file_path in res:
            im = wx.StaticBitmap(self.panel, -1, wx.Bitmap(file_path, wx.BITMAP_TYPE_ANY), size = (64, 64))
            sizer.Add(im, 1, flag = wx.SHAPED)
        self.panel.SetSizerAndFit(sizer)

class MyApp(wx.App):
    def OnInit(self):
        frame = MainWindow(None, -1, "Image Search")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True
        
app = MyApp(0)
app.MainLoop()
