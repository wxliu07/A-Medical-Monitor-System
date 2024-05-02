import numpy as np
import cv2

# 初始化摄像头
webcam = cv2.VideoCapture(0)

# 设置视频参数
realWidth, realHeight = 320, 240
webcam.set(3, realWidth)
webcam.set(4, realHeight)

# 输出视频设置
outputVideoFilename = "output.mov"
outputVideoWriter = cv2.VideoWriter(outputVideoFilename, cv2.VideoWriter_fourcc('j', 'p', 'e', 'g'), 15,
                                    (realWidth, realHeight), True)

A = 100
B = 5

while True:
    ret, frame = webcam.read()
    if not ret:
        break

    # 提取红色和蓝色通道
    red_channel = frame[:, :, 2]
    blue_channel = frame[:, :, 0]

    # 计算红色通道的统计值
    mean_red, std_red = np.mean(red_channel), np.std(red_channel)
    red_final = std_red / mean_red

    # 计算蓝色通道的统计值
    mean_blue, std_blue = np.mean(blue_channel), np.std(blue_channel)
    blue_final = std_blue / mean_blue

    # 计算血氧饱和度
    sp = A - (B * (red_final / blue_final))
    sp = round(sp, 2)
    print(sp)
    # 输出到视频
    cv2.putText(frame, f"SpO2: {sp}%", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    outputVideoWriter.write(frame)

    # 显示实时视频
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
outputVideoWriter.release()
