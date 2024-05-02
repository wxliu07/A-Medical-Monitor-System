# 导入包
from math import sqrt


def compute_emotion(video_segment):
    # 模拟情绪识别
    # time.sleep(2)
    return "情绪：平静"


def computeRR(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        return lines


def computeHR(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        return lines


def computeSpO2(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        return lines


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
    RMSE = sqrt(the_sum_of_error / float(len(actual_data)))
    return RMSE


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
    # 定义一组真实数据
    actual_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # 定义一组预测数据
    predicted_data = [2, 4, 3, 5, 4, 6, 5, 7, 6, 8]
    # 调用calculate_the_MAE函数计算平均绝对误差
    Mean_Absolute_Error = calculate_the_MAE(predicted_data, actual_data)
    # 调用calculate_the_RMSE函数计算均方根误差
    RMSE = calculate_the_RMSE(predicted_data, actual_data)

    print(Mean_Absolute_Error, RMSE)
