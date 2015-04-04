import eventmanager
import model
import view
import controller
from ai import AI

import logging
from optparse import OptionParser
import pygame

# Log Levels
# logging.DEBUG
# logging.INFO
# logging.WARNING
# logging.ERROR
# logging.CRITICAL
#LOG_LEVEL = logging.DEBUG
LOG_LEVEL = logging.INFO

logging.basicConfig(format='%(name)s: %(levelname)s: %(message)s', level=LOG_LEVEL) 

logger = logging.getLogger(__name__)



def run():
    use_gui = False
    use_ai = False

    usage = "usage: %prog [options]"
    desc = ("Run drop7 with or without AI.  To enable AI, use -a flag. Use -g "
            "flag to set whether to show the GUI while the AI is "
            "active.  -g flag will not do anything without the -a flag set.")
    parser = OptionParser(usage=usage, description=desc)
    parser.add_option('-a', '--ai', dest='use_ai', action='store_true',
                      help='AI mode [default: %default]')
    parser.add_option('-g', '--gui', dest='use_gui', action='store_true',
                      help='show gui [default -a: False, default: True]')
    (options, args) = parser.parse_args()

    if options.use_ai is None:
        use_ai = False
        use_gui = True
    else:
        use_ai = True

        if options.use_gui is None:
            use_gui = False
        else:
            use_gui = True


    evManager = eventmanager.EventManager()
    gamemodel = model.GameEngine(evManager)
    keyboard = controller.Keyboard(evManager, gamemodel)
    graphics = view.GraphicalView(evManager, gamemodel, use_gui)
    if use_ai:
        ai = AI(evManager)

    gamemodel.run()

if __name__ == '__main__':
    run()
