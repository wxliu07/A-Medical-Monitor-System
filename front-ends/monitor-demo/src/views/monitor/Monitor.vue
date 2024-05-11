<template>
    <el-col class="monitor-data">
        <el-tabs
            v-model="activeName"
            class="demo-tabs"
            @tab-click="handleClick"
            type="border-card"
        >
            <!-- <el-tab-pane label="方法1" name="first">
                <el-card shadow="always" class="method-card method1">
                    <el-text
                        class="mx-1 method-title"
                        type="primary"
                        size="large"
                        style="font-size: 18px"
                        >实时监测</el-text
                    >
                    <el-steps
                        style="margin-top: 20px; margin-right: 0px"
                        :active="1"
                        space="400px"
                        finish-status="success"
                        direction="horizontal"
                    >
                        <el-step
                            title="Step 1"
                            description="开启权限"
                        ></el-step>
                        <el-step
                            title="Step 2"
                            description="开启前置"
                        ></el-step>
                        <el-step
                            title="Step 3"
                            description="实时检测"
                        ></el-step>
                        <el-step
                            title="Step 4"
                            description="显示结果"
                        ></el-step>
                    </el-steps>

                    <div class="video-recorder">
             
                        <video src="" id="srcvideo" ></video>
                    </div>

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
                        ></el-table-column>
                    </el-table>
                </el-card>
            </el-tab-pane> -->

            <el-tab-pane label="方法2" name="first">
                <el-card    v-loading="loading" 
                            element-loading-text="文件处理中, 请等待..."
                            shadow="always" class="method-card method2">
                    <el-text
                        class="mx-1 method-title"
                        type="primary"
                        size="large"
                        style="font-size: 18px"
                        >上传文件</el-text
                    >
                    <div class="method2-content">
                        <el-steps
                            style="height: 100%; margin-top: 20px"
                            :active="1"
                            space="400px"
                            finish-status="success"
                        >
                            <el-step
                                title="Step 1"
                                description="选择文件"
                            ></el-step>
                            <el-step
                                title="Step 2"
                                description="上传文件"
                            ></el-step>
                            <el-step
                                title="Step 3"
                                description="等待检测"
                            ></el-step>
                            <el-step
                                title="Step 4"
                                description="查看结果"
                            ></el-step>
                        </el-steps>

                        <el-upload
                            class="upload-demo"
                            drag
                            show-file-list
                            action="http://127.0.0.1:5000/api/uploadFile"
                            :on-success="handleUploadSuccess"
                            :on-error="handleUploadError"
                            :before-upload="beforeUpload"
                        >
                            <el-icon class="el-icon--upload"
                                ><upload-filled
                            /></el-icon>
                            <div class="el-upload__text">
                                拖拽文件到此处 <em>或点击此处按钮进行上传</em>
                            </div>
                            <!-- <el-button size="large" type="primary">点击上传</el-button> -->
                            <template #tip>
                                <div class="el-upload__tip">
                                    请选择人脸面部视频文件进行上传
                                </div>
                            </template>
                        </el-upload>
                    </div>

                    <el-table :data="tableDataByUpload" :key="isUpdate" border>
                        <el-table-column
                            v-for="(val, key) in monitorTableLable"
                            :key="key"
                            :prop="key"
                            :label="val"
                        >
                        </el-table-column>
                    </el-table>
                </el-card>
            </el-tab-pane>
        </el-tabs>
    </el-col>
</template>

<script>
import { reactive, ref, onMounted } from "vue";
import { nextTick } from 'vue';
import axios from "axios";
import { ElButton, ElMessage } from "element-plus";

export default {
    setup() {
        const videoElement = ref(null);
        const mediaStream = ref(null);

        const startBtnEnabled = ref(true);
        const stopBtnEnabled = ref(true);
        const pauseBtnEnabled = ref(true);
        const resumeBtnEnabled = ref(true);

        const recorder = ref(null);
        const allChunks = ref([]);

        const monitorDataByLoad = ref([]);
        const monitorTableLable = reactive({
            emotion: "Emotion",
            hr: "Heart Rate",
            rr: "Respiratory Rate",
            spo2: "SpO2",
            time: "Time",
        });

        const loading = ref(false)
        const isUpdate = ref(false)

        onMounted(() => {
            if (!navigator.mediaDevices.getUserMedia) {
                ElMessage.error("浏览器不支持媒体设备访问");
                return;
            }
        
            /*
            navigator.mediaDevices.getUserMedia({
                video: true
            })
            .then(function(mediaStream) {
                var srcvideo = document.getElementById("srcvideo")
                srcvideo.srcObject = mediaStream;
                srcvideo.play()
            })*/
        });
        


        const startRecording = () => {
            const options = { mimeType: "video/webm" };
            recorder.value = new MediaRecorder(mediaStream.value, options);
            recorder.value.ondataavailable = (event) =>
                allChunks.value.push(event.data);
            recorder.value.start(10); // 每10ms收集一次数据

            startBtnEnabled.value = false;
            stopBtnEnabled.value = true;
            pauseBtnEnabled.value = true;
            resumeBtnEnabled.value = false;
        };

        const stopRecording = () => {
            recorder.value.stop();
            recorder.value.onstop = async () => {
                const blob = new Blob(allChunks.value, { type: "video/webm" });
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.style.display = "none";
                a.href = url;
                a.download = "recorded-video.webm";
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);

                startBtnEnabled.value = true;
                stopBtnEnabled.value = false;
                pauseBtnEnabled.value = false;
                resumeBtnEnabled.value = false;
                allChunks.value = [];
            };
        };

        const pauseRecording = () => {
            recorder.value.pause();
            pauseBtnEnabled.value = false;
            resumeBtnEnabled.value = true;
        };

        const resumeRecording = () => {
            recorder.value.resume();
            pauseBtnEnabled.value = true;
            resumeBtnEnabled.value = false;
        };

        const closeCamera = () => {
            if (mediaStream.value) {
                mediaStream.value.getTracks().forEach((track) => track.stop());
                videoElement.value.srcObject = null;
                mediaStream.value = null;
                startBtnEnabled.value = false;
                stopBtnEnabled.value = false;
                pauseBtnEnabled.value = false;
                resumeBtnEnabled.value = false;
                ElMessage.success("摄像头已关闭");
            }
        };

        const activeName = ref("first");
        const handleClick = (tab, event) => {
            // console.log(tab, event);
        };

        const pagedTableData = ref();
        const tableDataByUpload = ref([]);

        const uploadFileData = ref([]);

        // 定义文件状态
        const file = ref(null);

        // 处理文件上传
        const handleFileUpload = (files, event) => {
            console.log(files, event);
            uploadFileData.value = files; // 存储上传的文件列表
        };

        // 上传文件
        const uploadFile = async () => {
            if (!uploadFileData.value || uploadFileData.value.length === 0) {
                console.error("没有选择任何文件");
                return;
            }

            try {
                const formData = new FormData();
                // 假设tableDataByUpload已经包含了通过el-upload选择的文件数组
                uploadFileData.value.forEach((file) => {
                    formData.append("files", file.raw);
                });

                const response = await axios.post(
                    "http://127.0.0.1:5000/api/uploadFile",
                    formData,
                    {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        },
                    }
                );

                console.log("上传成功:", response.data);
            } catch (error) {
                console.error("上传失败:", error.message);
            }
        };

        // 上传文件前
        const beforeUpload = (file) => {
            console.log(file);
            loading.value = true;
        };

        // 上传文件成功
        const handleUploadSuccess = (response, file, event) => {
            console.log(response);
            loading.value = true;
            taskStatusPolling(response.data.task_id);  // 开始轮询
        };

        // 上传文件失败
        const handleUploadError = (err, file, event) => {
            console.log(err, file, event);
        };

        
        // 轮询
        const taskStatusPolling = (task_id) => {
            const interval = setInterval(async () => {
                try {
                    const response = await axios.get(`http://127.0.0.1:5000/status/${task_id}`);
                    console.log(response.data.code)
                    let res = response.data
                    if(response.data.code === 200) {
                        loading.value = false; // 设置loading为false
                        clearInterval(interval);
                        console.log(res.data.result)
                        tableDataByUpload.value.push(res.data.result)
                        isUpdate.value = !isUpdate.value;
                        console.log(tableDataByUpload.value)
                    }
                } catch (error) {
                    console.error("Error fetching status:", error);
                    clearInterval(interval);
                }
            }, 3000);  // Poll every 5 seconds
        };
        

        return {
            loading,
            monitorTableLable,
            monitorDataByLoad,
            pagedTableData,
            tableDataByUpload,
            activeName,
            uploadFileData,
            isUpdate,

            handleClick,
            handleFileUpload,
            uploadFile,
            beforeUpload,
            handleUploadSuccess,
            handleUploadError,
        };
    },
};
</script>

<style scoped>
.method-card {
    margin-bottom: 10px;
    margin-right: 15px;
    box-shadow: 1px 4px 6px rgba(0, 0, 0, 0.1), 4px 1px 6px rgba(0, 0, 0, 0.1);
}

.method-title {
    color: #409eff;
    font-weight: bold;
    margin-bottom: 30px;
}


.method2-content {
    align-items: center;
}

.upload-button {
    margin-top: 20px;
}

.demo-tabs > .el-tabs__content {
    padding: 32px;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
}

video {
    width: 300px;  /* 或100%，根据需要调整 */
    height: 350px; /* 根据实际情况调整 */
    border: 1px solid #ccc; /* 增加边框看清楚视频是否被渲染 */
}

el-table {
    height: 500px; /* 或其他足够显示所有数据的高度 */
}


</style>
