import wx
import wx.html2
import os

class BrowserTab(wx.Panel):
    def __init__(self, parent, url="https://www.google.com"):
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.url_bar = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.url_bar.Bind(wx.EVT_TEXT_ENTER, self.on_url_enter)

        self.browser = wx.html2.WebView.New(self)
        self.browser.Bind(wx.html2.EVT_WEBVIEW_TITLE_CHANGED, self.on_title_changed)
        self.browser.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, self.on_navigating)
        self.browser.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.on_loaded)

        self.sizer.Add(self.url_bar, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.browser, 1, wx.EXPAND, 5)

        self.SetSizer(self.sizer)
        self.browser.LoadURL(url)

    def on_url_enter(self, event):
        url = self.url_bar.GetValue()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.LoadURL(url)

    def on_title_changed(self, event):
        title = event.GetString()
        notebook = self.GetParent()
        index = notebook.GetPageIndex(self)
        notebook.SetPageText(index, title[:15])

    def on_navigating(self, event):
        self.url_bar.SetValue(event.GetURL())

    def on_loaded(self, event):
        self.url_bar.SetValue(self.browser.GetCurrentURL())

class ZedBrowser(wx.Frame):
    def __init__(self):
        super().__init__(None, title="ZedBrowser - wxPython", size=(1024, 768))
        self.notebook = wx.Notebook(self)
        self.create_menu()
        self.add_tab("https://www.google.com")

    def create_menu(self):
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        new_tab = file_menu.Append(wx.ID_ANY, "New Tab\tCtrl+T")
        close_tab = file_menu.Append(wx.ID_ANY, "Close Tab\tCtrl+W")
        self.Bind(wx.EVT_MENU, self.on_new_tab, new_tab)
        self.Bind(wx.EVT_MENU, self.on_close_tab, close_tab)
        menubar.Append(file_menu, "&File")
        self.SetMenuBar(menubar)

    def add_tab(self, url):
        tab = BrowserTab(self.notebook, url)
        self.notebook.AddPage(tab, "New Tab", select=True)

    def on_new_tab(self, event):
        self.add_tab("https://www.google.com")

    def on_close_tab(self, event):
        if self.notebook.GetPageCount() > 1:
            self.notebook.DeletePage(self.notebook.GetSelection())

class ZedApp(wx.App):
    def OnInit(self):
        frame = ZedBrowser()
        frame.Show()
        return True

if __name__ == "__main__":
    app = ZedApp()
    app.MainLoop()
