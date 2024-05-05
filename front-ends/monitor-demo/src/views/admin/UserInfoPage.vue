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
            emotion: "情绪",
            hr: "心率",
            rr: "呼吸率",
            spo2: "血氧饱和度"
        });
        const currentPage = ref(1);


        const getMonitorData = async () => {
            try {
                const response = await axios.get(
                    "http://127.0.0.1:5000/api/database/getAllMonitorData",
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
