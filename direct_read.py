import cv2
import time

# 需要在服务器安装onceorauto
from camera.ffmpeg.ffmpeg_read import FFmpegRead  # ipc读流
# from camera.ffmpeg.save_video import SaveVideo  # 保存视频

def simple_read(rtsp):
    cap = cv2.VideoCapture(rtsp)
    ret, frame = cap.read()
    while ret:
        ret, frame = cap.read()
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()


def ffmpeg_read(rtsp):
    read_camera = FFmpegRead(rtsp, [1920, 1080])
    read_camera.start_read()
    time.sleep(5)

    image = read_camera.read()
    n = 0
    while n < 30:
        image = read_camera.read()
        n += 1
        if image is not None:
            print(image.shape)
        else:
            print('read None')
            continue

    read_camera.close_read()


if __name__ == '__main__':
    # stream = 'rtsp://admin:dh123456@172.16.115.140:554/cam/realmonitor?channel=1&subtype=0'
    stream = 'rtsp://admin:2021aifjeport@172.16.115.130:554/h264/ch1/main/av_stream'
    ffmpeg_read(stream)

