import numpy as np
from scipy import signal


class SignalProcessing:
    def __init__(self):
        self.a = 1

    def extract_color(self, ROIs):
        """
        从 ROI 中提取绿色的平均值
        """
        # r = np.mean(ROI[:,:,0])
        g = []
        for ROI in ROIs:
            g.append(np.mean(ROI[:, :, 1]))
        # b = np.mean(ROI[:,:,2])
        # return r, g, b
        output_val = np.mean(g)
        return output_val

    def normalization(self, data_buffer):
        """
        规范化输入数据缓冲区
        """

        # normalized_data = (data_buffer - np.mean(data_buffer))/np.std(data_buffer)
        normalized_data = data_buffer / np.linalg.norm(data_buffer)

        return normalized_data

    def signal_detrending(self, data_buffer):
        """
        删除整体趋势
        """
        detrended_data = signal.detrend(data_buffer)

        return detrended_data

    def interpolation(self, data_buffer, times):
        """
        插值数据缓冲器，使信号变得更加周期性（无频谱泄漏）
        """
        buffer_len = len(data_buffer)

        even_times = np.linspace(times[0], times[-1], buffer_len)

        interp = np.interp(even_times, times, data_buffer)
        interpolated_data = np.hamming(buffer_len) * interp
        return interpolated_data

    def fft(self, data_buffer, fps):

        buffer_len = len(data_buffer)

        freqs = float(fps) / buffer_len * np.arange(buffer_len / 2 + 1)

        freqs_in_minute = 60. * freqs

        raw_fft = np.fft.rfft(data_buffer * 30)
        fft = np.abs(raw_fft) ** 2

        interest_idx = np.where((freqs_in_minute > 50) & (freqs_in_minute < 180))[0]
        print(freqs_in_minute)
        interest_idx_sub = interest_idx[:-1].copy()  # advoid the indexing error
        freqs_of_interest = freqs_in_minute[interest_idx_sub]

        fft_of_interest = fft[interest_idx_sub]
        return fft_of_interest, freqs_of_interest

    def butter_bandpass_filter(self, data_buffer, lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = signal.butter(order, [low, high], btype='band')

        filtered_data = signal.lfilter(b, a, data_buffer)

        return filtered_data
