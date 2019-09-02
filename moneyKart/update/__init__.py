import logging as _log

from moneyKart import version
_log.basicConfig(level=_log.INFO)

__version__ = version

def checkForUpdates():
    # _log.info("New update is available")
    return False
