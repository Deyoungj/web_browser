from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from browser import Ui_MainWindow
from PyQt5.QtCore import QUrl
import sys

url = 'http://www.google.com'
df = 'VC browser'

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super( MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.actionNewTab.triggered.connect(self.open_new_tab2)
        self.ui.actionNewWindow.triggered.connect(lambda: self.ui.tabWidget.currentWidget().back())
        self.ui.actionback.triggered.connect(lambda: self.ui.tabWidget.currentWidget().back())
        self.ui.actionforward.triggered.connect(lambda: self.ui.tabWidget.currentWidget().forward())
        self.ui.actionreload.triggered.connect(lambda: self.ui.tabWidget.currentWidget().reload())
        self.ui.actionhome.triggered.connect(self.navigate_home)
        self.ui.actionsearch.triggered.connect(self.search_for)
        self.ui.actionvoice.triggered.connect(self.voice_assist)
        self.ui.actionNewWindow.triggered.connect(self.open_new_window)
        # self.ui.actionback.triggered.connect(lambda: self.ui.tabWidget.currentWidget().back())
        self.ui.tabWidget.tabBarDoubleClicked.connect(self.open_new_tab)
        self.ui.tabWidget.currentChanged.connect(self.current_tab_changed)
        self.ui.tabWidget.tabCloseRequested.connect(self.close_current_tab)
        self.ui.url_bar.returnPressed.connect(self.navigate_to_url)


        #creating our first tab
        self.add_new_tab(url,df)

    def add_new_tab(self, Qurl= None, title= 'NewTab'):

        # if url is blank
        if Qurl is None:

            #create open url url
            self.url = QUrl(url)

        #creating a webengineview object
        self.browser = QWebEngineView()

        #settting the url
        self.browser.setUrl(QUrl(Qurl))

        # setting the tab index
        self.index = self.ui.tabWidget.addTab(self.browser, title)
        
        self.ui.tabWidget.setCurrentIndex(self.index)

        # do this when the url is changed
        self.browser.urlChanged.connect(lambda url, browser = self.browser:
                                            self.update_url(url, self.browser))

        # adding action to the browser
        # and seting the tab title

        self.browser.loadFinished.connect(lambda _, index = self.browser:
                        self.ui.tabWidget.setTabText(self.index,self.browser.page().title()))

        print(self.index)


    
    def navigate_home(self):
        # when the home button is clicked go home
        self.ui.tabWidget.currentWidget().setUrl(QUrl(url))



    def open_new_tab(self,i):
        
        if i == -1:
            self.add_new_tab(url,df)


    # for the add tab icon
    def open_new_tab2(self):
        
        # get the current tab index
        i = self.ui.tabWidget.currentIndex()

        # add one to it
        i += 1

        #create new tab
        self.add_new_tab(url,df)

        self.index = self.ui.tabWidget.addTab(self.browser, df)
    
        self.ui.tabWidget.setCurrentIndex(self.index)



    def update_url_bar(self,url, browser = None):

        #if the action is not from this current tabb ignore
        if browser != self.ui.tabWidget.currentWidget():
            pass
        
        #else update the urlbar with the current url
        self.ui.url_bar.setText(url.toString())

        #change th cursor position
        self.ui.url_bar.setCursorPosition(0)


    # search function
    def search(self, url):

        self.ui.tabWidget.currentWidget().setUrl(url)



    # when enter is clicked on the krrboard
    def navigate_to_url(self):
        
        #get the text from the url bar
        text = self.ui.url_bar.text()

        # turn the text to a url object

        url = QUrl(text)

        # if the scheme is empty
        if url.scheme() == "":

            # then set the scheme
            url.setScheme('http')

        # else search for the text
        self.search(url)

        
    # whe the search button is triggered
    def search_for(self):
        #get the text from the url bar
        text = self.ui.url_bar.text()

        # turn the text to a url object

        url = QUrl(text)

        # if the scheme is empty
        if url.scheme() == "":

            # then set the scheme
            url.setScheme('http')
            
        # else search for the text
        self.search(url)


    # opening a new window
    def open_new_window(self):
        pass

    def voice_assist(self):
        pass

    def current_tab_changed(self):
        
        # get url in current tab
        url = self.ui.tabWidget.currentWidget().url()

        # update url
        self.update_url_bar(url, self.ui.tabWidget.currentWidget())

        # update url title



    def close_current_tab(self, index):
        
        #if there is only one tab
        if self.ui.tabWidget.count() < 2:
            self.close()

        #else remove the tab
        self.ui.tabWidget.removeTab(index)
            


    def update_title(self,browser):

        if browser != self.ui.tabWidget.currentWidget():
            return

        # get url title of current tab
        title = self.ui.tabWidget.currentWidget().page().title()

        #update window title with url title
        self.setWindowTitle(f'VC browser - {title}')



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

    