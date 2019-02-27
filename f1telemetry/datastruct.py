from PyQt5.QtCore import pyqtSignal, QObject


class SelectionData:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.radius = 0
        self.zero_frame = 0
        self.start_frame = 0
        self.end_frame = 0

    def set_x(self, x):
        self.x = int(x)

    def set_y(self, y):
        self.y = int(y)

    def set_radius(self, r):
        self.radius = int(r)

    def set_radius_delta(self, rd):
        self.radius += int(rd)

    def set_start_frame(self, f):
        self.start_frame = int(f)

    def set_end_frame(self, f):
        self.end_frame = int(f)

    def set_zero_frame(self, f):
        self.zero_frame = int(f)


class InteractiveDataSet(QObject):
    activeTreeChanged = pyqtSignal()
    initFinished = pyqtSignal()

    def __init__(self, ui, xdata, ydatasets, names, filename, basewidget):
        super().__init__()
        # make sure xdata is a list/tuple containing only numbers, while ydatasets needs to be a list/tuple
        # containing one or multiple lists/tuples which may only contain numbers
        # also names needs to be of equal length as ydatasets so there is one name per dataset
        assert isinstance(xdata, (list, tuple)), 'xdata needs to be a list or tuple!'
        assert isinstance(any(xdata), (float, int)), 'xdata may only contain int or float!'
        assert isinstance(ydatasets, (list, tuple)), 'ydatasets needs to be a list or tuple!'
        assert not isinstance(any(ydatasets), (list, tuple)), 'ydatasets may only contain lists or tuples!'
        assert isinstance(names, (list, tuple)), 'names needs to be a list or tuple!'
        assert len(ydatasets) == len(names), 'ydatasets and names need to be of equal length!'

        self.ui = ui
        self.trees = dict()

        for i in range(len(ydatasets)):
            assert len(ydatasets[i]) == len(xdata), 'every set of values in ydatasets needs have equal length as xdata!'

            # Create a base tree element and append it to a new tree. The tree is then added to the dataset's trees
            element = TreeElement('Base', self, xdata=xdata, ydata=ydatasets[i], options={'filename': filename})
            element.connectWidget(basewidget)
            tree = Tree(names[i], self)
            tree.appendTreeElement(element)
            self.trees[tree.name] = tree

        self.active = None
        self.setActiveTree(self.getTrees()[0])

        self.initFinished.emit()

    def getTrees(self):
        return list(self.trees.keys())

    def getActiveTreeName(self):
        if self.active:
            return self.active.name
        else:
            return None

    def setActiveTree(self, name):
        assert name in self.trees.keys(), 'Invalid tree name given!'
        if self.active and name == self.active.name:
            return

        self.active = self.trees[name]

        self.activeTreeChanged.emit()
        self.active.treeChangeFinished.emit()


class Tree(QObject):
    treeChangeFinished = pyqtSignal()

    def __init__(self, name, dataset):
        super().__init__()
        self.name = name
        self.elements = list()
        self.current = None

        self.dataset = dataset

    def appendTreeElement(self, element):
        element.parent = self
        self.elements.append(element)

        if len(self.elements) == 1:
            self.current = element

    def regenerateAll(self):
        pass

    def regenerateFrom(self, element):
        assert element not in self.elements, 'Element of type {} is not part of this tree!'.format(type(element))
        pass

    def getNewest(self):
        return self.elements[-1]

    def getPrevious(self, element):
        return self.elements[self.elements.index(element)-1]

    def setCurrent(self, element):
        assert element in self.elements, 'Element of type {} is not part of this tree!'.format(type(element))
        self.current = element

    def newElementFromNewest(self, name):
        xdata, ydata = self.getNewest().getData()
        element = TreeElement(name, self.dataset, xdata, ydata)
        self.appendTreeElement(element)
        self.setCurrent(element)

        return element


class TreeElement(QObject):
    dataChanged = pyqtSignal()

    def __init__(self, name, dataset, xdata=None, ydata=None, options=None):
        super().__init__()
        self.dataset = dataset
        self.parent = None
        self.name = name
        self.options = options
        self.xdata = xdata
        self.ydata = ydata

        self.segements = list()

        self.widget = None

    def connectWidget(self, widget):
        self.widget = widget(self)

    def getData(self):
        return self.xdata, self.ydata

    def getPreviousData(self):
        return self.parent.getPrevious(self).getData()

    def index(self):
        return self.parent.elements.index(self)