<template>
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
</template>

<script>
import { defineComponent, ref, reactive, onMounted, computed } from "vue";
import axios from "axios";

export default defineComponent({
    setup() {
        const monitorData = ref([]);
        const monitorTableLable = reactive({
            video_id: "项目",
            user_id: "用户id",
            video_url: "视频存放地址",
            record_time: "记录时间"
        });
        const currentPage = ref(1);


        const getMonitorData = async () => {
            try {
                const response = await axios.get(
                    "http://127.0.0.1:5000/api/database/getAllVideoData",
                );
                monitorData.value = response.data.data;
                console.log(monitorData.value)
            } catch (error) {
                console.error("Error fetching monitor data:", error);
            }
        };

        const pagedTableData = computed(() => {
            const start = (currentPage.value - 1) * 12;
            const end = currentPage.value * 12;
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
            pagedTableData,
            handlePageChange,
            currentPage,
        };
    },
});
</script>

<style scoped>
.el-table .cell {
    padding: 10px;
}
</style>
