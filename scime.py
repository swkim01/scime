import os, sys
import copy
import shutil
import PySide2

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

from PySide2 import QtCore, QtGui, QtWidgets, QtUiTools
import parsemsgs

game_map = "message.map"  # message map file
game_msg = "resource.msg" # message resource file

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def initTable(model):
    model.setColumnCount(5)
    model.setHeaderData(0, QtCore.Qt.Horizontal, "noun")
    model.setHeaderData(1, QtCore.Qt.Horizontal, "verb")
    model.setHeaderData(2, QtCore.Qt.Horizontal, "cond")
    model.setHeaderData(3, QtCore.Qt.Horizontal, "seq")
    model.setHeaderData(4, QtCore.Qt.Horizontal, "Talker")

    #for i in range(model.rowCount()):
    #    print(model.record(i))

class SciEditorMainWindow(object):
    def __init__(self, uifile):
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(uifile)
        self.ui.setWindowTitle('SCIME')
        self.ui.setWindowIcon(QtGui.QIcon('scime.ico'))
        self.mainWindow = self.ui.findChild(QtWidgets.QWidget, "MainWindow")
        
        self.ui.selectButton.clicked.connect(self.open)
        self.ui.resTypeBox.addItem("Default")
        self.ui.resTypeBox.addItem("SCI11/original")
        self.ui.resTypeBox.activated[str].connect(self.resTypeActivated)
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.updateButton.clicked.connect(self.update)
        self.ui.updateButton.setEnabled(False)

        self.msgtreemodel = QtGui.QStandardItemModel()
        self.ui.treeView.setModel(self.msgtreemodel)
        self.ui.treeView.clicked.connect(self.readData)
        self.msgmodel = QtGui.QStandardItemModel()
        initTable(self.msgmodel)
        self.ui.tableView.setModel(self.msgmodel)
        #self.ui.tableView.setColumnWidth(self.msgitem.columnCount()-1, 50)
        self.ui.tableView.clicked.connect(self.selectMsg)
        for i in range(5):
            self.ui.tableView.setColumnWidth(i, 90)
        self.ui.transText.textChanged.connect(self.saveMsg)
        self.ui.closeEvent = self.closeEvent

        self.rtype = None
        self.step = 6

    def resTypeActivated(self):
        restype = self.ui.resTypeBox.currentIndex()
        if restype == 0:
            self.step = 6
        elif restype == 1:
            self.step = 5

    def open(self):
        #dirName = QtWidgets.QFileDialog.getOpenFileName(self.mainWindow)
        self.gamedir = QtWidgets.QFileDialog.getExistingDirectory(self.mainWindow)
        print(self.gamedir)
        self.setTree()

    def save(self):
        resmap, messages = parsemsgs.update_mapmsg(self.rtype, self.resmap, self.transres)
        sortmap = sorted(resmap.items(), key=(lambda x: int(x[1])))
        filemap = '/'.join((self.gamedir, "message2.map"))
        parsemsgs.save_map(filemap, self.rtype, sortmap)

        filemsg = '/'.join((self.gamedir, "resource2.msg"))
        parsemsgs.save_msg(filemsg, self.rtype, sortmap, messages)

        self.ui.updateButton.setEnabled(True)

    def update(self):
        filemap = '/'.join((self.gamedir, "message2.map"))
        ufilemap = '/'.join((self.gamedir, "message.map"))
        shutil.copy(filemap, ufilemap)

        filemsg = '/'.join((self.gamedir, "resource2.msg"))
        ufilemsg = '/'.join((self.gamedir, "resource.msg"))
        shutil.copy(filemsg, ufilemsg)

    def setTree(self):
        # all widgets clear
        self.msgtreemodel.removeRows(0, self.msgtreemodel.rowCount())
        self.msgmodel.removeRows(0, self.msgmodel.rowCount())
        self.ui.origText.clear()
        self.ui.transText.clear()

        item1 = QtGui.QStandardItem("message")
        self.msgtreemodel.setItem(0, item1)

        # get original messages
        # message type : text(sci0/sci1), message(sci1.1+)
        rtype, self.res = parsemsgs.get_msgs_fromdir(self.gamedir)

        # get message map
        filemap = '/'.join((self.gamedir, game_map))
        mtype, self.resmap = parsemsgs.parse_map(filemap, self.step)
        if rtype != None and mtype != None:
            if rtype != mtype:
                print("Orignal msgtype has not equal to trans msgtype!")
                sys.exit(1)
        elif rtype != None:
            self.rtype = rtype
        else:
            self.rtype = mtype

        if self.resmap is None:
            sortmap=sorted(self.res.keys(), key=(lambda x: int(x)))
            #self.resmap = dict.fromkeys(sortmap, 0)
            self.resmap = dict((int(el), i) for i, el in enumerate(sortmap))

        filemsg = '/'.join((self.gamedir, game_msg))
        self.transres = parsemsgs.get_msgs_withmap(filemsg, self.resmap)
        if self.transres is None:
            print("transres is null!")
            self.transres = copy.deepcopy(self.res)
        elif self.res is None:
            print("res is null!")
            self.res = copy.deepcopy(self.transres)
        #else:
        #    checkmsgs()
        #for msg in self.res:
        #    qitem = QtGui.QStandardItem(msg[0])

        for msg in sorted(self.res.keys(), key=(lambda x: int(x))):
            qitem = QtGui.QStandardItem(msg)
            item1.appendRow(qitem)

    def checkmsgs(self, item):
        '''
        check orig msg and patch msg one by one, if differ then correct
        '''
        msgheader = self.res[item][0]
        msgs = self.res[item][1]
        transmsgheader = self.transres[item][0]
        transmsgs = self.transres[item][1]
        if msgheader[6] != transmsgheader[6]:
            print("Differ original msg(%d) and translated msg(%d)!!!"% (msgheader[6], transmsgheader[6]))
            if msgheader[6] > transmsgheader[6]:
                print("What number(s) would you like to add empty msgs among translated msgs?")
                value = input()
                self.transres[item][1].insert(int(value)-1,"")
                self.transres[item][0][6] += 1
            else:
                print("What number(s) would you like to skip msgs among translated msgs?")
                value = input()
                del self.transres[item][1][int(value)-1]
                self.transres[item][0][6] -= 1
                print(value)

    def readData(self, index):
        '''
        select an item on the msg tree, then display msg table
        '''
        item = str(index.data())
        self.curitem = item
        self.msgmodel.removeRows(0, self.msgmodel.rowCount())
        if index.parent().row() != -1: # not top resource("message")
            msgheader = self.res[item][0]
            self.msgs = self.res[item][1]

            self.transmsgs = self.transres[item][1]
            self.checkmsgs(item)

            for msg in self.msgs:
                noun = QtGui.QStandardItem(str(msg[0]))
                verb = QtGui.QStandardItem(str(msg[1]))
                cond = QtGui.QStandardItem(str(msg[2]))
                seq = QtGui.QStandardItem(str(msg[3]))
                talker = QtGui.QStandardItem(str(msg[4]))
                self.msgmodel.appendRow([noun, verb, cond, seq, talker])
        #self.ui.mainWindow.append(message)

    def selectMsg(self, index):
        '''
        select an msg item on the msg table, then display orig and trans msg
        '''
        row = index.row()
        self.curmsg = row
        self.ui.origText.setText(str(self.msgs[row][7]))
        if self.transmsgs:
            self.ui.transText.setText(str(self.transmsgs[row][7]))

    def saveMsg(self):
        if self.transres:
            self.transres[self.curitem][1][self.curmsg][7] = self.ui.transText.toPlainText()
        pass

    def closeEvent(self, event):
        pass

if __name__ == "__main__":
    #from pathlib import Path
    #root = Path.cwd()
    #libpaths = QtWidgets.QApplication.libraryPaths()
    #if sys.platform == 'darwin':
    #    libpaths.append("/usr/local/Cellar/qt5/5.5.1_2/plugins")
    #    QtWidgets.QApplication.setLibraryPaths(libpaths)
    #elif sys.platform == 'win32':
    #    libpaths.append(str(root / "PySide2/plugins/platforms"))
    #    QtWidgets.QApplication.setLibraryPaths(libpaths)
    app = QtWidgets.QApplication(sys.argv)
    loader = QtUiTools.QUiLoader()
    #mw = SciEditorMainWindow('./scime.ui')
    mw = SciEditorMainWindow(resource_path('scime.ui'))
    mw.ui.show()
    sys.exit(app.exec_())
