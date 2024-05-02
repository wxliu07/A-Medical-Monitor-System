'''
遇到问题没人解答？小编创建了一个Python学习交流QQ群：778463939
寻找有志同道合的小伙伴，互帮互助,群里还有不错的视频学习教程和PDF电子书！
'''
# from time import sleep
# from tqdm import tqdm
# # 这里同样的，tqdm就是这个进度条最常用的一个方法
# # 里面存一个可迭代对象
# for i in tqdm(range(1, 500)):
#    # 模拟你的任务
#    sleep(0.01)
# sleep(0.5)
import h5py

with h5py.File('/core/video/IPPG.hdf5', 'r') as fin:
    # 查询datasheet
    print(fin.keys())

    # # 读取某个dataesheet
    # key = 'dataset1'
    # dset = fin[key]
    # a_get = dset['a']

# 查看该datasheet中数据名称、格式等参数
# print(dset.dtype)
