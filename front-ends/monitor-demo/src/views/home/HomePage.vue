<template>
    <el-row class="home">
        <el-col :span="24">
            <el-card shadow="always" class="user-card">
                <!-- 使用Flex布局容器包裹用户信息和描述信息 -->
                <div class="card-content">
                    <!-- 用户信息部分 -->
                    <div class="user-info">
                        <img
                            src="../../assets/images/user.png"
                            alt=""
                            class="user-image"
                        />
                        <div>
                            <p class="name">Mr.Liu</p>
                            <p>
                                上次登录时间:<span
                                    >&nbsp;&nbsp;&nbsp;&nbsp;{{
                                        yesterday
                                    }}</span
                                >
                            </p>
                            <p>
                                上次登录地点:<span
                                    >&nbsp;&nbsp;&nbsp;&nbsp;安徽·宣城</span
                                >
                            </p>
                        </div>
                    </div>
                    <!-- 描述信息部分 -->
                    <el-descriptions
                        title="Last Monitoring:"
                        class="user-descriptions"
                    >
                        <el-descriptions-item label="HR:"
                            >88 BPM</el-descriptions-item
                        >
                        <el-descriptions-item label="RR:"
                            >15 BPM</el-descriptions-item
                        >
                        <el-descriptions-item label="SpO2:">
                            96 BPM
                        </el-descriptions-item>
                        <el-descriptions-item label="Time: ">{{
                            yesterday
                        }}</el-descriptions-item>
                    </el-descriptions>
                </div>
            </el-card>
        </el-col>

        <el-col class="monitor-data">
            <el-card shadow="always" class="data-card">
                <el-table
                    :data="pagedTableData"
                    border
                    stripe
                    :default-sort="{ prop: 'date', order: 'descending' }"
                    :header-cell-style="{ color: '#409EFF' }"
                >
                    <el-table-column
                        v-for="(val, key) in monitorTableLable"
                        :key="key"
                        :prop="key"
                        :label="val"
                    >
                    </el-table-column>
                </el-table>

                <el-pagination
                    layout="prev, pager, next"
                    :total="monitorData.length"
                    :current-page="currentPage"
                    :page-size="8"
                    @current-change="handlePageChange"
                >
                </el-pagination>
            </el-card>
        </el-col>
    </el-row>
</template>

<script>
import { getCurrentInstance, onMounted, reactive, ref, computed} from "vue";
import axios from "axios";
import dayjs from "dayjs"; // 确保安装了dayjs库
import { useStore } from "vuex";

export default {
    setup() {
        const store = useStore();
        const monitorData = ref([]);
        const monitorTableLable = reactive({
            emotion: "Emotion",
            hr: "Heart Rate",
            rr: "Respiratory Rate",
            spo2: "SpO2",
            time: "Time",
        });
        const currentPage = ref(1);

        const yesterday = ref(dayjs().subtract(1, "day"));

        const getMonitorData = async () => {
            try {
                const response = await axios.get(
                    "http://127.0.0.1:5000/api/database/getMonitorDataByUid",
                    {
                        params: { uid: 1 },
                    }
                );
                monitorData.value = response.data.data;
            } catch (error) {
                console.error("Error fetching monitor data:", error);
            }
        };

        const pagedTableData = computed(() => {
            const start = (currentPage.value - 1) * 7;
            const end = currentPage.value * 7;
            return monitorData.value.slice(start, end);
        });

        const handlePageChange = (newPage) => {
            currentPage.value = newPage;
        };
      
        onMounted(() => {
            getMonitorData();
        });

        return {
            monitorData,
            monitorTableLable,
            yesterday,
            pagedTableData,
            handlePageChange,
            currentPage,
        };
    },
};
</script>

<style lang="less" scoped>
.home {
    width: 100%; 
    margin: 0 auto;
    padding: 10px 10px 0; 

    .el-card {
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1); 
        margin-bottom: 10px; 
    }

    .user-info {
        display: flex;
        align-items: center;
        padding-bottom: 20px;
        margin-top: 0; 

        img {
            width: 100px; 
            height: 100px;
            border-radius: 50%;
            margin-right: 20px; 
        }

        .name {
            font-weight: bold;
            font-size: 24px; 
            margin-bottom: 5px;
        }

        p {
            line-height: 1.5;
            font-size: 16px;
            color: #666;
            margin: 0;

            span {
                color: #409eff; 
            }
        }
    }

    .monitor-data {
        .el-table {
            min-height: 300px; 
            th {
                background-color: #f0f2f5; 
            }

            .el-table-column {
                text-align: center; 
            }
        }
    }
}

.el-table .el-table__header-wrapper tr th {
    color: #409eff !important;
}

.card-content {
    display: flex;
    justify-content: space-between; /* 确保子元素之间有空间 */
    align-items: flex-start; /* 对齐到顶部 */
}

.user-descriptions {
    flex-grow: 1; /* 允许描述信息部分占据剩余空间 */
    margin-top: 10px;
    margin-left: 40px; /* 与用户信息部分保持间距 */
}
</style>
