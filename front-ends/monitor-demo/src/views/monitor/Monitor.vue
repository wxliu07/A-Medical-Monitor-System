<template>
  <el-col class="monitor-data">
    <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick" type="border-card">
      <el-tab-pane label="方法1" name="first">
        <el-card shadow="always" class="method-card method1">
          <el-text class="mx-1 method-title" type="primary" size="large" style="font-size: 18px;">实时监测</el-text>
          <el-steps style="margin-top: 20px; margin-right: 0px;" :active="1" space="400px" finish-status="success"
            direction="horizontal">
            <el-step title="Step 1" description="开启权限"></el-step>
            <el-step title="Step 2" description="开启前置"></el-step>
            <el-step title="Step 3" description="实时检测"></el-step>
            <el-step title="Step 4" description="显示结果"></el-step>
          </el-steps>

          <div class="video-input-container">
            <input type="text" placeholder="视频源输入" />
            <el-button @click="checkPermission">查看权限</el-button>
            <el-button @click="startDetection">开始检测</el-button>
          </div>

          <el-table :data="pagedTableData" border stripe :default-sort="{ prop: 'date', order: 'descending' }"
            :header-cell-style="{ color: '#409EFF' }">
            <el-table-column v-for="(val, key) in monitorTableLable" :key="key" :prop="key"
              :label="val"></el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="方法2" name="second">
        <el-card shadow="always" class="method-card method2">
          <el-text class="mx-1 method-title" type="primary" size="large" style="font-size: 18px;">上传文件</el-text>
          <div class="method2-content">
            <el-steps style="height: 100%; margin-top: 20px;" :active="1" space="400px" finish-status="success">
              <el-step title="Step 1" description="选择文件"></el-step>
              <el-step title="Step 2" description="上传文件"></el-step>
              <el-step title="Step 3" description="等待检测"></el-step>
              <el-step title="Step 4" description="查看结果"></el-step>
            </el-steps>

            <el-upload class="upload-demo" drag  show-file-list 
              action="http://127.0.0.1:5000/api/uploadFile" 
              :on-success="handleUploadSuccess"
              :on-error="handleUploadError"
              :before-upload="beforeUpload">
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                拖拽文件到此处 <em>或点击此处按钮进行上传</em>
              </div>
              <el-button size="large" type="primary">点击上传</el-button>
              <template #tip>
                <div class="el-upload__tip">
                  请选择人脸面部视频文件进行上传
                </div>
              </template>
            </el-upload>


          </div>


          <el-table :data="tableDataByUpload" border>
            <el-table-column v-for="(val, key) in monitorTableLable" :key="key" :prop="key" :label="val">
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>





  </el-col>
</template>



<script>
import { reactive, ref, } from "vue";
import axios from 'axios';

export default {
  setup() {
    const monitorDataByLoad = ref([]);
    const monitorTableLable = reactive({
      emotion: 'Emotion',
      hr: 'Heart Rate',
      rr: 'Respiratory Rate',
      spo2: 'SpO2',
      time: 'Time'
    });

    const activeName = ref('first')
    const handleClick = (tab, event) => {
      // console.log(tab, event);
    }

    const pagedTableData = ref()
    const tableDataByUpload = ref()

    const uploadFileData = ref([])

    // 定义文件状态
    const file = ref(null);

    // 处理文件上传
    const handleFileUpload = (files, event) => {
      console.log(files, event);
      uploadFileData.value = files;  // 存储上传的文件列表
    };

    // 上传文件
    // 上传文件
    const uploadFile = async () => {
      if (!uploadFileData.value || uploadFileData.value.length === 0) {
        console.error('没有选择任何文件');
        return;
      }

      try {
        const formData = new FormData();
        // 假设tableDataByUpload已经包含了通过el-upload选择的文件数组
        uploadFileData.value.forEach(file => {
          formData.append('files', file.raw);
        });

        const response = await axios.post('http://127.0.0.1:5000/api/uploadFile', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        console.log('上传成功:', response.data);
      } catch (error) {
        console.error('上传失败:', error.message);
      }
    };


    const checkPermission = () => {
      // Implement the method to check for camera permissions
    };

    const startDetection = () => {
      // Implement the method to start detection
    };

    const beforeUpload = (file) => {
      console.log(file);
    };

    const handleUploadSuccess = (response, file, event) => {
      console.log(response, file, event);
    };


    const handleUploadError = (err, file, event) => {
      console.log(err, file, event);
    };

    return {
      handleFileUpload,
      uploadFile,
      monitorTableLable,
      monitorDataByLoad,
      pagedTableData,
      checkPermission,
      startDetection,
      tableDataByUpload,
      activeName,
      handleClick,
      uploadFileData,

      beforeUpload,
      handleUploadSuccess,
      handleUploadError
    };
  }
};
</script>

<style scoped>
.method-card {
  margin-bottom: 20px;
  margin-right: 15px;
  box-shadow: 1px 4px 6px rgba(0, 0, 0, 0.1),
    4px 1px 6px rgba(0, 0, 0, 0.1);
}

.method-title {
  color: #409EFF;
  font-weight: bold;
  margin-bottom: 30px;
}

.video-input-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 30px 0px;
  background-color: #f0f0f0;
  padding: 20px;
  border-radius: 5px;
}

.method2-content {

  align-items: center;
}

.upload-button {
  margin-top: 20px;
}

.demo-tabs>.el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}



</style>
