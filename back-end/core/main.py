from math import sqrt
import cv2
import numpy as np
import torch
from tqdm import *
from core.net.emotion_predict import detect_emotion
from core.process.rr_monitor import get_face_landmarks, draw_ROI_line, get_avg_gray_pixel
from core.process.rr_monitor import _x1y1wh_to_xyxy, smooth_data
from core.process.rr_monitor import infrared_preprocessing, eliminate_abnormal_peaks
from database import insertDatas
from process.signal_processing import SignalProcessing
from scipy.signal import find_peaks
from core.net.Siamfc import TrackerSiamFC
import mediapipe as mp
import multiprocessing
from net.model_CNN import FaceCNN

from datetime import datetime

import sys
sys.path.append("..")  # 将上级目录添加到模块搜索路径中

detection_model_path = 'models/caseharden_frontal_face_default.xml'
classification_model_path = 'models/model_emotion.pkl'
face_detection = cv2.CascadeClassifier(detection_model_path)


def calculate_emotion(video_frames, length, face_detection, emotion_classifier):
    emotion = detect_emotion(video_frames, length, face_detection, emotion_classifier)
    return emotion


def calculate_HR(ppg_signals, length, times, fps):
    buffer_size = 100
    ppg_signals = ppg_signals[-buffer_size:len(ppg_signals)]
    length = len(ppg_signals)
    times = times[-buffer_size:len(times)]

    sp = SignalProcessing()
    data_buffer = ppg_signals  # Buffer to store signal data

    detrended_data = sp.signal_detrending(data_buffer)
    interpolated_data = sp.interpolation(detrended_data, times)
    normalized_data = sp.normalization(interpolated_data)
    fft_of_interest, freqs_of_interest = sp.fft(normalized_data, fps)

    max_arg = np.argmax(fft_of_interest)
    # bpm = freqs_of_interest[max_arg] * 60  # Convert from Hz to bpm
    bpm = freqs_of_interest[max_arg]  # Convert from Hz to bpm
    return bpm


# 计算呼吸率
def calculate_RR(ppg_signals, length, fps):
    signal_smooth = smooth_data(ppg_signals)
    ppg_signals = infrared_preprocessing(signal_smooth)
    # 波峰检测
    indices = find_peaks(ppg_signals, height=None, threshold=None, distance=5,
                         prominence=None, width=None, wlen=None, rel_height=None,
                         plateau_size=None)
    # 剔除错误波峰
    rate = 0.25  # 根据数据分布调整该参数
    rr = eliminate_abnormal_peaks(indices[0], ppg_signals, rate, total_num=length, fps=fps)

    return rr


def calculate_SpO2(frame, frame_length, A=100, B=5):
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

    return sp


# 读取给定的视频帧
def process_video(file_path, chunk_duration=10):
    vc = cv2.VideoCapture(file_path)  # 读取视频文件
    fps = vc.get(cv2.CAP_PROP_FPS)  # 获取视频的帧率
    total_frames = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))  # 获取视频的总帧数
    chunk_frames = int(chunk_duration * fps)  # 每次读取的帧数
    remaining_frames = total_frames  # 剩余帧数
    times = []
    # 加载表情识别模型
    emotion_classifier = torch.load(classification_model_path)
    monitor_results = []
    while remaining_frames > 0:
        video_npy = []  # 存储视频帧的列表
        count_images_num = 0  # 已经读取的帧数

        # 读取视频帧直到达到每次读取的帧数或者读取完成
        while count_images_num < chunk_frames and remaining_frames >= 0:
            rival, frame = vc.read()  # rival: 捕获是否成功;  frame: 捕获到的一帧图像
            if rival:
                video_npy.append(frame)
                count_images_num += 1
                remaining_frames -= 1
                times.append((1.0 / fps) * count_images_num)
            else:
                break

        # 如果读取到了帧，则调用函数处理
        if video_npy:
            video_npy = np.array(video_npy)
            emotion = calculate_emotion(video_npy, count_images_num, face_detection, emotion_classifier)
            ppg_signal = get_ppg_infrared(video_npy, count_images_num)

            # 创建多个进程，分别处理不同的数据
            with multiprocessing.Pool(processes=3) as pool:
                result_sp02 = pool.apply(calculate_SpO2, (video_npy, len(video_npy)))
                result_rr = pool.apply(calculate_RR, (ppg_signal, len(video_npy), fps))
                result_hr = pool.apply(calculate_HR, (ppg_signal, len(video_npy), times, fps))
            # 将处理结果整合起来
            final_result = {
                "emotion": emotion,
                "hr": result_hr,
                "rr": result_rr,
                "spo2": result_sp02,
                'time': str(datetime.now())
            }
            monitor_results.append(final_result)
            print(final_result)
            # insertDatas(1, emotion, result_hr, result_rr, result_sp02, datetime.now())
            # emotion = calculate_emotion(video_npy, count_images_num, face_detection, emotion_classifier)
            # sp = calculate_SpO2(ppg_signal, len(ppg_signal))
            # rr = calculate_RR(ppg_signals=ppg_signal, length=len(video_npy), fps=fps)
            # hr = calculate_HR(ppg_signals=ppg_signal, length=len(video_npy), times=times, fps=fps)
            # print("当前视频段的呼吸率: ", emotion)
    vc.release()
    return monitor_results


# 目标追踪算法初始化
model_path = 'models/model_siamfc.pth'
trk = TrackerSiamFC(net_path=model_path)


def get_ppg_infrared(video_frames, image_nums):
    # mediapipe人脸检测
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(  # 确定最小置信值
        min_detection_confidence=0.5, min_tracking_confidence=0.5)

    ppg_infrared_nose = []  # 原始PPG信号
    face_mark = False  # 是否检测到人脸
    for i in tqdm(range(image_nums)):
        image = video_frames[i]
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)  # 水平翻转, 转换RGB

        image.flags.writeable = False  # 禁止写
        results = face_mesh.process(image)  # 人脸关键点检测
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if not face_mark:
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    x_data_arr, y_data_arr, z_data_arr = get_face_landmarks(face_landmarks)
                    nose = [165, 391, 371, 142, 165]  # 可以手动选取
                    nose_roi, init_state = draw_ROI_line(x_data_arr, y_data_arr, image, nose)
                    if len(init_state) != 0 and init_state[3] > 5:  # 初始化追踪模型；并标记被检测到人脸
                        trk.init(image, init_state)
                        face_mark = 1
                        # cv2.imshow('nose_roi', nose_roi)
                        signal_infrared_nose = get_avg_gray_pixel(nose_roi)
                        ppg_infrared_nose.append(signal_infrared_nose)
        else:
            # 追踪鼻子ROI
            pos = trk.update(image)
            pos = _x1y1wh_to_xyxy(pos)
            pos = [int(l) for l in pos]

            # 分割鼻子ROI
            img_infrared = image
            nose_roi = img_infrared[pos[1]:pos[3], pos[0]:pos[2]]

            # 计算ROI像素均值
            signal_infrared_nose = get_avg_gray_pixel(nose_roi)

            # 呼吸信号
            ppg_infrared_nose.append(signal_infrared_nose)
    return np.array(ppg_infrared_nose)


def calculate_the_RMSE(predicted_data, actual_data):
    """
    该函数用于计算均方根误差
    Parameters
    ----------
    predicted_data : 一维列表
        预测数据.
    actual_data : 一维列表
        真实数据.
    Returns
    -------
    RMSE : 浮点型
        均方根误差.
    """
    # 定义一个变量用于存储所有样本的平方误差之和
    the_sum_of_error = 0
    # 开始逐渐遍历每一个样本
    for i in range(len(actual_data)):
        # 计算预测数据与真实数据的误差
        predition_error = predicted_data[i] - actual_data[i]
        # 不断累加求和，计算所有样本的平方误差之和
        the_sum_of_error += predition_error ** 2
    # 计算所有样本的均方根误差
    rmse = sqrt(the_sum_of_error / float(len(actual_data)))
    return rmse


def calculate_the_MAE(predicted_data, actual_data):
    """
    该函数用于计算平均绝对误差
    Parameters
    ----------
    predicted_data : 一维列表
        预测数据.
    actual_data : 一维列表
        真实数据.
    Returns
    -------
    MAE : 浮点型
        平均绝对误差.
    """
    # 定义一个变量用于存储所有样本的绝对误差之和
    the_sum_of_error = 0
    # 开始逐渐遍历每一个样本
    for i in range(len(actual_data)):
        # 不断累加求和，计算所有样本的绝对误差之和
        the_sum_of_error += abs(predicted_data[i] - actual_data[i])
    # 计算所有样本的平均绝对误差
    MAE = the_sum_of_error / float(len(actual_data))
    return MAE


if '__main__' == __name__:
    # # 定义一组真实数据
    # actual_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # # 定义一组预测数据
    # predicted_data = [2, 4, 3, 5, 4, 6, 5, 7, 6, 8]
    # # 调用calculate_the_MAE函数计算平均绝对误差
    # Mean_Absolute_Error = calculate_the_MAE(predicted_data, actual_data)
    # # 调用calculate_the_RMSE函数计算均方根误差
    # RMSE = calculate_the_RMSE(predicted_data, actual_data)
    #
    # print(Mean_Absolute_Error, RMSE)
    # results = [{'emotion': 'happy', 'hr': 86.31368631368632, 'rr': 17.824541860005354, 'spo2': 95.0, 'time': '2024-05-05 16:06:46.819341'}, {'emotion': 'happy', 'hr': 57.54245754245755, 'rr': 17.269316049803855, 'spo2': 94.94, 'time': '2024-05-05 16:07:11.991577'}]
    # 遍历数据列表，逐个提取数据并插入到数据库中
    # for data in results:
    #     emotion = data['emotion']
    #     hr = data['hr']
    #     rr = data['rr']
    #     spo2 = data['spo2']
    #     time = datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S.%f')  # 将时间字符串转换为datetime对象
    #     user_id = 1  # 假设用户ID为1，你可以根据实际情况设置
    #
    #     # 调用插入函数将数据插入到数据库中
    #     result = insertDatas(user_id, emotion, hr, rr, spo2, time)
    results = process_video("video/example_dsh.mp4", chunk_duration=20)
