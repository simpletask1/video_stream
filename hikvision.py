import threading
import traceback

from camera.sdk_gige_hikvision.GrabImage import MVS_Cam  # 工业相机SDK读流


class hikCamera(threading.Thread):

    def __init__(self, ip_name):
        threading.Thread.__init__(self)
        self.ip_name = ip_name

        # 初始化摄像头
        self.device_camera = MVS_Cam(self.ip_name)

    def run(self):
        i = 0
        while i < 100:
            try:
                # 获取图像
                # 该读流方式不会缓存，读到的一定是最新帧
                frame = self.device_camera.Get_Frame()
            except:
                print(traceback.format_exc())
            else:
                if type(frame) != type(None):
                    print(type(frame), self.ip_name, frame.shape[:2])

            i += 1

        # 关闭摄像头
        self.device_camera.Close_Cam()