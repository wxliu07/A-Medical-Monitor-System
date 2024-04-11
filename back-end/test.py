# from utils import Result
# import json


# print(type(Result.success("sss")))
# res = json.loads(Result.success("sss"))
# print(res['code'])
#
# print(json.loads(Result.success(desc="sss")))
# print(json.loads(Result.success(desc="sss"))['code'])

from flask import Flask, request, jsonify
from multiprocessing import Process, Queue
import time
import uuid
import os
import cv2

app = Flask(__name__)

# 存储任务状态和结果
tasks = {}

def compute_heart_rate(video_segment):
    # 模拟心率计算
    time.sleep(2)  # 假装这需要一些处理时间
    return "心率80bpm"

def compute_respiration_rate(video_segment):
    # 模拟呼吸率计算
    time.sleep(2)
    return "呼吸率15rpm"

def compute_emotion(video_segment):
    # 模拟情绪识别
    time.sleep(2)
    return "情绪：平静"

def compute_oxygen_saturation(video_segment):
    # 模拟血氧饱和度计算
    time.sleep(2)
    return "血氧饱和度98%"

def process_video(task_id, video_path, output_queue):
    # 视频处理逻辑，同时处理多个方面
    functions = [compute_heart_rate, compute_respiration_rate, compute_emotion, compute_oxygen_saturation]
    results = {}
    for func in functions:
        result = func(video_path)  # 假设每个函数都接受视频路径作为输入
        results[func.__name__] = result
    output_queue.put(results)
    tasks[task_id] = ("完成", results)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        task_id = str(uuid.uuid4())
        video_path = f"./videos/{task_id}.mp4"
        if not os.path.exists('./videos'):
            os.makedirs('./videos')
        file.save(video_path)
        tasks[task_id] = ("处理中", None)
        output_queue = Queue()
        Process(target=process_video, args=(task_id, video_path, output_queue)).start()
        return jsonify({"message": "文件接收成功，开始处理", "task_id": task_id})
    else:
        return jsonify({"message": "文件上传失败"}), 400

@app.route('/status/<task_id>')
def get_status(task_id: str):
    status, result = tasks.get(task_id, ("未知任务", None))
    return jsonify({"status": status, "result": result})

if __name__ == '__main__':
    # app.run(debug=True)
    # task_id = str(uuid.uuid4())
    # task_id2 = str(uuid.uuid4())
    # print(task_id)
    # print(task_id2)


    # 读取视频文件
    video_capture = cv2.VideoCapture('example_dsh.mp4')

    # 检查视频是否成功打开
    if not video_capture.isOpened():
        print("Error: Could not open video file.")
        exit()

    # 获取视频的帧率和尺寸
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 创建视频编码器并设置参数
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter('output_video.mp4', fourcc, fps, (width, height))

    # 读取视频的前3秒内容
    end_time = 3.0
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break

        current_time = video_capture.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        if current_time > end_time:
            break

        output_video.write(frame)

    # 释放资源
    video_capture.release()
    output_video.release()


