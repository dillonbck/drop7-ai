import eventmanager
import model
import view
import controller

import logging


# Log Levels
# logging.DEBUG
# logging.INFO
# logging.WARNING
# logging.ERROR
# logging.CRITICAL
LOG_LEVEL = logging.DEBUG
#LOG_LEVEL = logging.INFO

logging.basicConfig(format='%(name)s: %(levelname)s: %(message)s', level=LOG_LEVEL) 

logger = logging.getLogger(__name__)


def run():
    evManager = eventmanager.EventManager()
    gamemodel = model.GameEngine(evManager)
    keyboard = controller.Keyboard(evManager, gamemodel)
    graphics = view.GraphicalView(evManager, gamemodel)
    gamemodel.run()

if __name__ == '__main__':
    run()