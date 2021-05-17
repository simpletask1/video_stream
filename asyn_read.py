import sys
import threading
import queue
import cv2
import time
import traceback
from datetime import datetime

from onceorauto.general import set_logger


class readCamera(threading.Thread):
    def __init__(self, id, logger, rtsp_address):
        threading.Thread.__init__(self)
        self.id = id
        self.logger = logger
        self.rtsp= rtsp_address

        self.deal_queue = queue.Queue(5)
        self.exitcode = 0
        self.exception = None
        self.exc_traceback = ''

    # @tail_call_optimized
    def read_vid(self):
        vid = cv2.VideoCapture(self.rtsp)
        self.logger.info('c{}_isOpened {}'.format(self.id, vid.isOpened()))
        if vid.isOpened() == False:
            self.logger.info('c{} no stream'.format(self.id))
        while True:
            _, image = vid.read()
            if image is not None:
                self.deal_queue.put(image)
                if self.deal_queue.full():
                    self.deal_queue.get()
            else:
                vid.release()
                self.logger.info('camera c{} no stream'.format(self.id))
                self.logger.info('camera c{} Reread stream'.format(self.id))
                break
        time.sleep(5)
        return self.read_vid()

    def read(self):
        if not self.deal_queue.empty():
            return self.deal_queue.get()
        else:
            self.logger.info('camera c{} caches no images'.format(self.id))
            return None

    # 捕获线程异常
    def run(self):
        try:
            self._run()
        except:
            self.exitcode = 1
            self.exc_traceback = ''.join(traceback.format_exception(*sys.exc_info()))
            self.logger.error("Appear ERROR about {} thread".format(self.id))
            self.logger.error(traceback.format_exc())
            exit()

    def _run(self):
        self.logger.info("start rtsp_{} thread. time:{}".format(self.id, datetime.now().strftime('%Y-%m-%d/%H:%M:%S')))
        self.read_vid()
        self.logger.info("end rtsp_{} thread. time:{}".format(self.id, datetime.now().strftime('%Y-%m-%d/%H:%M:%S')))


if __name__ == '__main__':
    logger = set_logger(log_path='./log.txt', backup_count=1, max_bytes= 5 * 1024 * 1024)
    rtsp = 'rtsp://admin:2021aifjeport@172.16.115.130:554/h264/ch1/main/av_stream'

    read_camera = readCamera(1, logger, rtsp)
    read_camera.daemon = True
    read_camera.start()
    time.sleep(10)

    print('start read...')
    n = 0
    while n < 20:
        img = read_camera.read()
        if img is not None:
            print(img.shape)
            n += 1
        else:
            continue
