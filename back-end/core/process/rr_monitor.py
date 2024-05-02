import cv2
import numpy as np
import scipy
from scipy import signal
from scipy.signal import find_peaks, savgol_filter
from Siamfc import TrackerSiamFC

# 呼吸率对应的频率:0.15-0.40Hz，参考论文: https://www.nature.com/articles/s41598-019-53808-9
RR_Min_HZ = 0.15  # 根据数据分布调整呼吸率滤波范围
RR_Max_HZ = 0.40

FPS = 25  # 采样频率


# 将目标检测中包含边界框信息的列表从(x1, y1, w, h)的格式转换为(x1, y1, x2, y2)
def _x1y1wh_to_xyxy(bbox_x1y1wh):
    x1, y1, w, h = bbox_x1y1wh
    x2 = int(x1 + w)
    y2 = int(y1 + h)
    return x1, y1, x2, y2


# 从指定路径中读取红外视频文件，将视频帧存储在numpy数组中以便后续处理
def read_video_infrared(data_path_infrared):
    img_num = 1500  # 读取的最大帧数
    vc = cv2.VideoCapture(data_path_infrared)  # 读取视频文件
    c = 0
    count_imgs_num = 0  # 已经读取的帧数
    videonpy = []  # 存储视频帧的列表
    timeF_infrared = 1  # timeF 视频帧计数间隔频率
    if vc.isOpened():  # 判断是否正常打开
        rval, frame = vc.read()  # rval: 捕获是否成功;  frame: 捕获到的一帧图像
    else:
        rval = False

    while rval:
        rval, frame = vc.read()
        if c % timeF_infrared == 0:  # 每隔timeF帧加到数组内;
            if frame is not None:
                videonpy.append(frame)
                count_imgs_num = count_imgs_num + 1
        c = c + 1
        cv2.waitKey(1)
        if c >= img_num:
            break
    vc.release()
    videonpy = np.array(videonpy)
    return videonpy


# 计算输入图像感兴趣区域（ROI）的平均灰度值，用于后续分析信号变化
def get_avg_gray_pixel(img_ROI):
    gray_img = cv2.cvtColor(img_ROI, cv2.COLOR_BGR2GRAY)
    avg_pixel = np.mean(gray_img)
    return avg_pixel


# 对从视频中提取的信号进行预处理，包括去趋势、标准化、滤波和平滑。
def infrared_preprocessing(signals):
    # 去趋势
    detrend_signals = detrend(signals, 100)
    detrend_signals = detrend_signals.flatten()
    # 标准化
    normalized_signals = normalize(detrend_signals)
    # 滤波并返回平滑后的数据
    filtered_signals = filter_signal_infrared(normalized_signals)
    return smooth_data(filtered_signals)


# 消除信号中可能存在的线性或非线性趋势
def detrend(X, detLambda=10):  # new detrend
    """
    desc: get rid of a randomness trend might deal with sudden increase trend coming from head movements
    args:
        - X::[array<float>]
            signal
    ret:
        - detrendedX::[array<float>]
            detrended signal
    """
    # 参考论文: "An advanced detrending method with application to HRV analysis"
    t = X.shape[0]  # 信号的长度
    l = t / detLambda  # 平滑度参数 lambda
    I = np.identity(t)  # 单位矩阵
    D2 = scipy.sparse.diags([1, -2, 1], [0, 1, 2],  # 差分矩阵, 捕捉信号的变化情况
                            shape=(t - 2, t)).toarray()
    # 进行去趋势处理
    detrendedX = (I - np.linalg.inv(I + l ** 2 * (np.transpose(D2).dot(D2)))).dot(X)
    return detrendedX


# 对输入的信号进行标准化(归一化)处理，并返回标准化后的信号
def normalize(signals):
    print('func:normalize>>{},type:{}'.format(signals, type(signals)))
    if np.all(signals == 0) or len(signals) == 0:
        return signals
    mean = np.mean(signals)
    std_dev = np.std(signals, ddof=1)
    normalized_signals = (signals - mean) / std_dev
    return normalized_signals


# 滤波处理:
def filter_signal_infrared(signals):
    filtered_signals = butterworth_filter(signals, RR_Min_HZ, RR_Max_HZ, FPS, order=5)
    return filtered_signals


# 巴特沃斯滤波器: 对信号进行频率域的滤波操作
def butterworth_filter(data, low, high, sample_rate, order=2):
    """
    :param data:  信号数据
    :param low:   下限频率
    :param high:  上限频率
    :param sample_rate:  采样率(FPS)
    :param order: 滤波器的阶数
    :return:  滤波后的信号
    """
    nyquist_rate = sample_rate * 0.5  # 奈奎斯特频率
    low /= nyquist_rate  # 滤波器的下限频率
    high /= nyquist_rate  # 滤波器的上限频率
    # 创建 Butterworth 滤波器的系数 b 和 a
    b, a = signal.butter(N=order, Wn=[low, high], btype='bandpass')
    return signal.lfilter(b, a, data)  # 将输入数据 data 与滤波器系数进行卷积，得到滤波后的信号


# 对信号进行平滑处理
def smooth_data(signals):
    # https://www.delftstack.com/zh/howto/python/smooth-data-in-python/
    win_len = 91  # 平滑窗口的长度, 影响波峰拟合, 考虑信号中当前点及其前后各45个数据点
    poly_order = 3  # 拟合多项式的阶数, 影响呼吸信号的幅值拟合
    # “萨维茨基-戈雷”滤波器
    signal_smooth = savgol_filter(signals, win_len, poly_order)
    return signal_smooth


# 从处理后的信号中提取呼吸率（RR）
def rr_extraction(PPG_values):
    # 傅里叶变换
    fft = np.abs(np.fft.rfft(PPG_values))
    buffer_size = len(PPG_values)
    # 当 buffer_size==0 的问题需要判断
    if buffer_size == 0:  # 3-19
        rr_value = 0
    else:
        freqs = FPS / buffer_size * np.arange(buffer_size / 2 + 1)
        # 找到在正常呼吸率范围内的频率最高值
        while True:
            max_idx = fft.argmax()  # 寻找数组的最大索引值
            bps = freqs[max_idx]
            if bps < RR_Min_HZ or bps > RR_Max_HZ:
                fft[max_idx] = 0
            else:
                rr_value = bps * 60.0
                break
        # print('rr:',rr_value)
    return rr_value


# 进一步处理信号，包括平滑处理和剔除异常波峰。
def eliminate_abnormal_peaks(index_arr, PPG_nose, rate, total_num, fps):
    peaks_values_arr = []
    for i in range(len(index_arr)):
        if PPG_nose[index_arr[i]] > 0:
            peaks_value = PPG_nose[index_arr[i]]
            peaks_values_arr.append(peaks_value)

    # 波峰的平均幅度
    avg_value_peaks = np.mean(peaks_values_arr)
    # 波峰限制
    max_value_peak = avg_value_peaks + avg_value_peaks * rate
    min_value_peak = avg_value_peaks - avg_value_peaks * rate
    print('max_value_peak:', max_value_peak)
    print('min_value_peak:', min_value_peak)

    rr_peak_count = 0  # PPG_nose信号中的累加波峰个数
    peak_index = []  # 波峰索引
    for i in range(len(index_arr)):
        if PPG_nose[index_arr[i]] >= min_value_peak:
            peak_index.append(index_arr[i])
            rr_peak_count = rr_peak_count + 1
    # print('peak_index:', peak_index)

    peak_distance_sum = []  # 存储相邻波峰之间的距离
    for j in range(len(peak_index)):
        if j >= 1:
            peak_distance = peak_index[j] - peak_index[j - 1]
            peak_distance_sum.append(peak_distance)

    avg_peak_dis = np.mean(peak_distance)  # 相邻波峰之间的平均距离

    # 计算PPG_nose信号的小数部分
    decimal = (total_num - peak_index[len(peak_index) - 1] + peak_index[0]) / avg_peak_dis
    # 计算一分钟的呼吸率
    rr_value = (rr_peak_count + decimal - 1) / total_num * (fps * 60)

    return rr_value


# 辅助函数，用于在视频帧上绘制感兴趣区域并获取人脸特征点。
def draw_ROI_line(x_data_arr, y_data_arr, image, index_ROI):
    xmin = x_data_arr[index_ROI[0]] * image.shape[1]
    xmax = x_data_arr[index_ROI[0]] * image.shape[1]
    ymin = y_data_arr[index_ROI[0]] * image.shape[0]
    ymax = y_data_arr[index_ROI[0]] * image.shape[0]

    for kk in range(len(index_ROI) - 1):
        x1 = int(x_data_arr[index_ROI[kk]] * image.shape[1])
        y1 = int(y_data_arr[index_ROI[kk]] * image.shape[0])
        x2 = int(x_data_arr[index_ROI[kk + 1]] * image.shape[1])
        y2 = int(y_data_arr[index_ROI[kk + 1]] * image.shape[0])
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 1)  # 连线

        # 求最大最小值
        if x1 >= xmax:
            xmax = x1
        else:
            xmin = x1

        if y1 >= ymax:
            ymax = y1
        else:
            ymin = y1

    # print('xmin = ', xmin)
    # print('xmax = ', xmax)
    # print('ymin = ', ymin)
    # print('ymax = ', ymax)
    img_ROI = image[int(ymin):int(ymax), int(xmin):int(xmax)]

    # 初始状态的位置信息 [x, y, w, h]
    w = xmax - xmin
    h = ymax - ymin
    init_state = [xmin, ymin, w, h]

    return img_ROI, init_state


# 辅助函数，用于在视频帧上绘制感兴趣区域并获取人脸特征点。
def get_face_landmarks(face_landmarks):
    # https://so.muouseo.com/qa/pvw0v2yxx6j1.html
    x_data_arr, y_data_arr, z_data_arr = [], [], []
    for landmark in face_landmarks.landmark:
        x = landmark.x
        y = landmark.y
        z = landmark.z
        x_data_arr.append(x)
        y_data_arr.append(y)
        z_data_arr.append(z)

    return x_data_arr, y_data_arr, z_data_arr


# 主函数，整合上述所有步骤，从红外视频中监测和计算呼吸率
def main():
    #################### mediapipe人脸检测 #####################
    import mediapipe as mp
    mp_drawing = mp.solutions.drawing_utils
    mp_face_mesh = mp.solutions.face_mesh

    # For static images:
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        min_detection_confidence=0.5)
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    # For webcam input:
    face_mesh = mp_face_mesh.FaceMesh(
        min_detection_confidence=0.5, min_tracking_confidence=0.5)
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    #################### mediapipe人脸检测 #####################

    # 目标追踪算法初始化
    model_path = '../models/model_siamfc.pth'
    trk = TrackerSiamFC(net_path=model_path)
    datapath_infrared = '../video/example_dsh.mp4'  # init_state =  [158, 368, 60, 39]

    img_arr = read_video_infrared(datapath_infrared)
    print('len(img_arr):', len(img_arr))
    total_num = len(img_arr)
    ppg_infrared_nose = []
    face_mark = 0
    for i in range(total_num):
        image = img_arr[i]
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = face_mesh.process(image)

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # cv2.imshow('image', img)

        #################### mediapipe人脸检测 #####################
        if face_mark == 0:
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # 获取特征点
                    # face_landmarks_str = str(face_landmarks)
                    x_data_arr, y_data_arr, z_data_arr = get_face_landmarks(face_landmarks)
                    for k in range(len(x_data_arr)):
                        # cv2.circle(image, pt_pos, 1, (0, 255, 0), 1) # 画点
                        # 人脸地标点参考 https://developers.google.com/mediapipe/solutions/vision/face_landmarker/
                        nose = [165, 391, 371, 142, 165]  # 可以手动选取
                    nose_roi, init_state = draw_ROI_line(x_data_arr, y_data_arr, image, nose)
                    print('init_state = ', init_state)
                    if len(init_state) != 0 and init_state[3] > 5:  # 初始化追踪模型；并标记被检测到人脸
                        trk.init(image, init_state)
                        face_mark = 1
                        cv2.imshow('nose_roi', nose_roi)
                        signal_infrared_nose = get_avg_gray_pixel(nose_roi)
                        ppg_infrared_nose.append(signal_infrared_nose)
                        # cv2.waitKey(0)
        #################### mediapipe人脸检测 #####################
        else:
            ####追踪鼻子ROI ####
            pos = trk.update(image)
            pos = _x1y1wh_to_xyxy(pos)
            pos = [int(l) for l in pos]
            ####追踪鼻子ROI ####

            # 分割鼻子ROI
            img_infrared = image
            nose_roi = img_infrared[pos[1]:pos[3], pos[0]:pos[2]]

            # 计算ROI像素均值
            signal_infrared_nose = get_avg_gray_pixel(nose_roi)
            # 呼吸信号
            ppg_infrared_nose.append(signal_infrared_nose)

            # cv2.imshow('image', image)
            cv2.imshow('nose_roi', nose_roi)
            if cv2.waitKey(5) & 0xFF == 27:
                break

    # 方法一： 1.1 先平滑处理，再对信号进行预处理
    ppg_infrared_nose = np.array(ppg_infrared_nose)
    signal_smooth = smooth_data(ppg_infrared_nose)
    ppg_nose = infrared_preprocessing(signal_smooth)

    # 1.2 波峰检测
    indices = find_peaks(ppg_nose, height=None, threshold=None, distance=5,
                         prominence=None, width=None, wlen=None, rel_height=None,
                         plateau_size=None)

    # 1.3 剔除错误波峰
    rate1 = 0.25  # 根据数据分布调整该参数
    rr1 = eliminate_abnormal_peaks(indices[0], ppg_nose, rate1, total_num, FPS)

    print('indices:', indices)
    print('RR_value0 = ', rr1)


if __name__ == "__main__":
    main()
