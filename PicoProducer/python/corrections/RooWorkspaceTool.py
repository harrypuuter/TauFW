# Author: Sebastian Brommer (October 2020)
import os, re
from TauFW.common.tools.file import ensureTFile
from TauFW.common.tools.log import Logger
LOG = Logger('RooWorkspaceTool')


class RooScaleFactor:
    """
    Main class for reading out functions from RooWorkspace
    """
    def __init__(self, workspace, function, arguments):
        self.workspace_file = ensureTFile(workspace)
        self.arguments = arguments
        self.workspace = self.workspace_file.Get("w")
        self.function = self.workspace.function(function)
        self.argset = self.workspace.argSet(",".join(self.arguments))

    def getSF(self, parameters):
        """
            Calculate the SF and return the value
        """
        for paramter in self.arguments:
            self.argset.setRealValue(paramter, parameters[paramter])
        return self.function.getVal(self.argset)