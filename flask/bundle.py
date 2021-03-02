'''Prepare Python App for Bundled Electron App'''

import os
import sys

def setup(app):
    '''
    System Arguments:
        1 - UI Key (used to limit admin functionality scope)
        2 - Port to Serve App on
        3 - Path to Overlay .exe
    '''
    if sys.argv[1] != 'test':
        app.template_folder = os.path.join(sys._MEIPASS, 'templates')
        app.static_folder = os.path.join(sys._MEIPASS, 'static')

    return sys.argv[1], sys.argv[2], sys.argv[3]