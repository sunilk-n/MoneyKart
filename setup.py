import sys
import os
import platform

from cx_Freeze import setup, Executable

projectPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(projectPath)

import moneyKart

__version__ = moneyKart.version

class PlatformExecutable(Executable):
    """
    Extend cx_Freeze.Executable to handle platform variations.
    """

    Windows = "Windows"
    Linux = "Linux"
    Darwin = "Darwin"

    exeExtensions = {
        Windows: ".exe",
        Linux: "",
        Darwin: ".app"
    }

    def __init__(self, script, initScript=None, base=None, targetName=None, icons=None, shortcutName=None,
                 shortcutDir=None, copyright=None, trademarks=None):

        # despite supposed to be optional, targetName is actually required on some configurations
        if not targetName:
            targetName = os.path.splitext(os.path.basename(script))[0]
        # add platform extension to targetName
        targetName += PlatformExecutable.exeExtensions[platform.system()]
        # get icon for platform if defined
        icon = icons.get(platform.system(), None) if icons else None
        if platform.system() in (self.Linux, self.Darwin):
            currentDir = os.path.dirname(os.path.abspath(__file__))
            initScript = os.path.join(currentDir, "setupInitScriptUnix.py")
        super(PlatformExecutable, self).__init__(script, initScript, base, targetName, icon, shortcutName,
                                                 shortcutDir, copyright, trademarks)

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

moneyKartApp = PlatformExecutable(
    "moneyKart/kartDisplay/__main__.py",
    targetName="MoneyKart", base=base
)

packages = [
    "os", "json", "atexit"
]

options = {
    'build_exe': {
        'includes': packages
    }
}

executables = [
    moneyKartApp
]

setup(
    name="Money Kart",
    description="App to mantain your daily transactions",
    version=__version__,
    options=options,
    executables=executables
)
