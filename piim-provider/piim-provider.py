import zmq
import sys
import time

import io
import logging
import cv2
import imutils
from imutils.video import VideoStream
from PIL import ImageFont
import numpy as np

try:
    import thread
except ImportError:
    import _thread as thread

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    
IMG_BROKER = 'tcp://localhost:5556'
WIDTH = 640
HEIGHT = 480

def make_font(size, path='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'):
    return ImageFont.truetype(path, size)

class PiimProvider(object):
    def __init__(self):
        pass

    def start(self):
        zmq_context = zmq.Context()
        socket = zmq_context.socket(zmq.PUB)
        socket.connect(IMG_BROKER)
        off_time = 0
        stream = None
        while True:
            time.sleep(0.020)
            try:
                if stream is None:
                    stream = VideoStream(src=0).start()
                    time.sleep(2.0)
                frame = stream.read()
                if frame is not None:
                    frame = imutils.resize(frame, width=WIDTH, height=HEIGHT)
                    buf = io.BytesIO()
                    # Save the arrays into the buffer
                    np.savez_compressed(buf, image=frame)
                    # cv2.imshow('Frame', frame)
                    # cv2.waitKey(1)
                    # buf = frame.tobytes()
                    print('frame {}'.format(frame.shape))
                    buf.seek(0)
                    socket.send(buf.read(), 0)
            except KeyboardInterrupt:
                print('keyboard interrupt, exit')
                break
            except:
                logging.error('camera error', exc_info=True)

        
def my_except_hook(exctype, value, traceback):
    logging.info('Uncaught error {} {} {}'.format(exctype, value, traceback))
    sys.__excepthook__(exctype, value, traceback)

sys.excepthook = my_except_hook
provider = PiimProvider()
provider.start()
