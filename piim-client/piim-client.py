import zmq
import sys
import numpy as np
import logging
import cv2
from PIL import ImageFont
import io

try:
    import thread
except ImportError:
    import _thread as thread

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    
IMG_BROKER = 'tcp://localhost:5555'
WIDTH = 640
HEIGHT = 480

def make_font(size, path='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'):
    return ImageFont.truetype(path, size)

class PiimClient(object):
    def __init__(self):
        pass

    def start(self):
        zmq_context = zmq.Context()
        socket = zmq_context.socket(zmq.SUB)
        socket.connect(IMG_BROKER)
        socket.subscribe('')
        while True:
            try:
                buf = socket.recv()
                if buf != b'CAFF':
                    print('invalid packet {}'.format(buf))
                    continue
                buf = socket.recv()
                print('recv {} bytes'.format(len(buf)))
                # frame = np.frombuffer(buf, dtype=np.dtype('uint8'))
                # frame = frame.reshape(HEIGHT, WIDTH, 3)
                buf = io.BytesIO(buf)
                frame = np.load(buf)['image']
                print('frame {}'.format(frame.shape))
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
            except KeyboardInterrupt:
                print('keyboard interrupt, exit')
                break
            except:
                logging.error('camera error', exc_info=True)

        
def my_except_hook(exctype, value, traceback):
    logging.info('Uncaught error {} {} {}'.format(exctype, value, traceback))
    sys.__excepthook__(exctype, value, traceback)

sys.excepthook = my_except_hook
provider = PiimClient()
provider.start()
