import multiprocessing


def process_emotion(data):
    # 处理情绪数据的函数
    return [emotion * 2 for emotion in data]


def process_heart_rate(data):
    # 处理心率数据的函数
    return [heart_rate * 1.5 for heart_rate in data]


def process_breathing_rate(data):
    # 处理呼吸率数据的函数
    return [breathing_rate * 0.8 for breathing_rate in data]


def process_blood_oxygen(data):
    # 处理血氧饱和度数据的函数
    return [blood_oxygen + 5 for blood_oxygen in data]


def main():
    # 假设 sensor_data 是传感器采集的数据列表
    sensor_data = [50, 60, 70, 80, 90]

    # 创建多个进程，分别处理不同的数据
    with multiprocessing.Pool(processes=4) as pool:
        result_emotion = pool.apply(process_emotion, (sensor_data,))
        result_heart_rate = pool.apply(process_heart_rate, (sensor_data,))
        result_breathing_rate = pool.apply(process_breathing_rate, (sensor_data,))
        result_blood_oxygen = pool.apply(process_blood_oxygen, (sensor_data,))

    # 将处理结果整合起来
    final_result = {
        "emotion": result_emotion,
        "heart_rate": result_heart_rate,
        "breathing_rate": result_breathing_rate,
        "blood_oxygen": result_blood_oxygen
    }
    print(final_result)


if __name__ == "__main__":
    main()
