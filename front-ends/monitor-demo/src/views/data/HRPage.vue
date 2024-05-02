<template>
    <el-card class="echarts-card">
        <div ref="chart" style="width: 100%; height: 400px;"></div>
    </el-card>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import * as echarts from 'echarts';

export default {
    setup() {
        const chart = ref(null);

        onMounted(async () => {
            try {
                const response = axios({
                    method: 'GET',
                    url: 'http://127.0.0.1:5000/api/database/getHrDataByUid',
                    params: {
                        uid: 1
                    }
                }).then((result) => {
                    if (result.data.code === 200) {
                        console.log(result.data.data);
                        const data = result.data.data;
                        initChart(data)
                    }
                    else {
                        console.log('失败');
                    }
                }).catch((err) => {
                    console.log(err);
                });

            } catch (error) {
                console.error('Error fetching data:', error);
            }
        });

        function initChart(data) {
            const hrValues = data.map(item => item.hr);
            const minHr = Math.min(...hrValues) - 15;
            const maxHr = Math.max(...hrValues) + 15;

            const myChart = echarts.init(chart.value);
            myChart.setOption({
                tooltip: {
                    trigger: 'axis',
                },
                xAxis: {
                    type: 'category',
                    data: data.map(item => item.time),
                    axisLabel: {
                        show: false,
                    },
                    axisTick: {
                        show: false,
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#999',
                        },
                    },
                },
                yAxis: {
                    type: 'value',
                    min: minHr,
                    max: maxHr,
                    axisLabel: {
                        formatter: '{value} bpm',
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#999',
                        },
                    },
                    splitLine: {
                        lineStyle: {
                            type: 'dashed',
                        },
                    },
                },
                series: [{
                    data: hrValues,
                    type: 'line',
                    smooth: true,
                    showSymbol: false,
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0, color: 'lightblue'
                        }, {
                            offset: 1, color: 'white'
                        }])
                    },
                }],
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true,
                },
            });
        }

        return {
            chart,
        };
    },
};
</script>

<style scoped>
.echarts-card {
    margin: 30px 0;
}
</style>