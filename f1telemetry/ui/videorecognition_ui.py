from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.Qt import QSizePolicy, QFont, QMenu, QIcon

from ui.customwidgets import F1ToolBarButton
from ui.uibaseelements import create_toolbar_category, create_toolbar_divider, create_toolbar_spacer
from ui.videoplayerwidget import VideoPlayerWidget

from datastruct import SelectionData

FONT = QFont('Bahnschrift')


class VideoRecognitionUI(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        mainlayout = QVBoxLayout()
        self.setLayout(mainlayout)

        #######################
        # ##### TOOLBAR ###########################################################################################
        #######################
        toolbar = QWidget()
        toolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        mainlayout.addWidget(toolbar)
        mainlayout.setSpacing(0)
        mainlayout.setContentsMargins(0, 0, 0, 0)

        toolbarlayout = QHBoxLayout(toolbar)
        toolbarlayout.setContentsMargins(0, 0, 0, 0)
        toolbarlayout.setSpacing(0)

        ########################
        # ########### create first category (file) and add it to the toolbar
        # category widget is created in seperate function (title, buttonvars, icons, texts)
        category_file, btns = create_toolbar_category('FILE',
                                                      ('open.png', 'runrecognition.png'),
                                                      ('Open', 'Run'))
        self.openBtn, self.runBtn = btns
        toolbarlayout.addWidget(category_file)  # add category to toolbar

        # add a vertical line between categories; divider is create in seperate function
        toolbarlayout.addWidget(create_toolbar_divider())

        # ##############################
        # ############## add expanding spacer with background
        toolbarspacer = create_toolbar_spacer()
        toolbarlayout.addWidget(toolbarspacer)

        #############################
        # ############ last toolbar button; switch environment
        self.category_env, btns = create_toolbar_category('ENVIRONMENT', ('envvideorecognition.png',),
                                                          ('Videorecognition',), buttonsize=('double+menu',))
        self.changeEnvBtn, = btns
        self.changeEnvBtn.setPopupMode(F1ToolBarButton.InstantPopup)
        changeenvmenu = QMenu()
        changeenvmenu.setFont(FONT)
        changeenvmenu.setStyleSheet('''QMenu {background-color: #e8e8e9;
                                                color: #373a3e;
                                                padding: 0px;
                                                margin: 0px;
                                                }        
                                            QMenu::item {
                                                padding: 0px 5px 0px 60px;
                                                background-color: #e8e8e9;
                                                height: 40px;
                                                margin: 0px;
                                                border: None;
                                                }
                                            QMenu::icon''')
        menubtnpost = changeenvmenu.addAction(QIcon('./ui/images/envpostprocessing.png'), 'Postprocessing')
        menubtnpost.triggered.connect(lambda: self.window().switch_environment(0))  # switch to index 0/postprocessing

        self.changeEnvBtn.setMenu(changeenvmenu)
        toolbarlayout.addWidget(create_toolbar_divider())
        toolbarlayout.addWidget(self.category_env)

        ##############################################
        # ########### Content ########################
        ##############################################

        selection = SelectionData()  # TODO Fix: SelectionData should not be defined in UI file
        self.videoplayer = VideoPlayerWidget(self, selection)
        mainlayout.addWidget(self.videoplayer)
