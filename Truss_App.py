# WORKED WITH VERNON ROBINSON
# CHAT GPT USED FOR DEBUGGING AND HELP.
# BUILT OFF SMAYS STEM FILE

# region imports
from Truss_GUI import Ui_TrussStructuralDesign  # Import the generated GUI layout
from PyQt5 import QtWidgets as qtw  # PyQt5 widgets module for GUI elements
from PyQt5 import QtCore as qtc  # PyQt5 core module for event handling and core functionality
from PyQt5 import QtGui as qtg  # PyQt5 GUI module for advanced graphic features
from Truss_Classes import TrussController  # Custom controller for managing truss data and interaction
import sys  # System module for command line arguments and system exit


# endregion

# region class definitions
class MainWindow(Ui_TrussStructuralDesign, qtw.QWidget):
    """
    Main window for the Truss Structural Design application.
    Inherits from both the auto-generated GUI class and the QWidget base class.
    """

    def __init__(self):
        """
        Initializes the main window, sets up UI, connects signals to slots,
        and initializes the truss controller.
        """
        super().__init__()
        self.setupUi(self)

        # Connect UI elements to their corresponding functions
        self.btn_Open.clicked.connect(self.OpenFile)
        self.spnd_Zoom.valueChanged.connect(self.setZoom)  # Handles zoom level changes

        # Create an instance of the TrussController and assign GUI display widgets to it
        self.controller = TrussController()
        self.controller.setDisplayWidgets((
            self.te_DesignReport, self.le_LinkName, self.le_Node1Name,
            self.le_Node2Name, self.le_LinkLength, self.gv_Main
        ))

        # Setup custom event filtering to handle user interaction with the graphics view
        self.controller.setupEventFilter(self)
        self.gv_Main.setMouseTracking(True)
        self.gv_Main.setAttribute(qtc.Qt.WA_AlwaysShowToolTips, True)  # Always show tooltips when hovering

        self.show()  # Display the window

    def setZoom(self):
        """
        Adjusts the zoom level of the graphics view based on the spinner value.
        Resets the transformation and rescales using the new value.
        """
        self.gv_Main.resetTransform()
        self.gv_Main.scale(self.spnd_Zoom.value(), self.spnd_Zoom.value())

    def eventFilter(self, obj, event):
        """
        Overrides the default eventFilter to intercept and delegate scene events to the controller.

        :param obj: The object on which the event occurred
        :param event: The event to handle
        :return: Boolean indicating whether the event was handled
        """
        if obj == self.controller.view.scene:
            # Delegate event handling to the controller
            self.controller.handleSceneEvent(event, self.gv_Main.transform(), self.lbl_MousePos, self.spnd_Zoom)
        return super(MainWindow, self).eventFilter(obj, event)

    def OpenFile(self):
        """
        Opens a file dialog to select a truss design file, reads its contents,
        and passes the data to the controller for processing and rendering.
        """
        filename = qtw.QFileDialog.getOpenFileName()[0]  # Open file dialog and get selected file path
        if len(filename) == 0:  # If no file was selected, exit early
            return
        self.te_Path.setText(filename)  # Display selected file path
        file = open(filename, 'r')  # Open file in read mode
        data = file.readlines()  # Read all lines into a list
        self.controller.ImportFromFile(data)  # Pass data to controller for import
