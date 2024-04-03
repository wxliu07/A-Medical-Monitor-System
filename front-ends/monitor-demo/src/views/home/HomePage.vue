<template>
    <div>
        <input id="file" type="file" @change="handleFileUpload">
        <el-button :disabled="loading" type="primary" class="login-button" @click="uploadFile">上传文件</el-button>
    </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
    setup() {
        // 定义文件状态
        const file = ref(null);

        // 处理文件上传
        const handleFileUpload = (event) => {
            file.value = event.target.files[0];
            console.log(event)
        };

        // 上传文件
        const uploadFile = async () => {
            try {
                const fileInput = document.getElementById('file'); // 假设你有一个id为file的<input type="file">
                if (!fileInput.files[0]) {
                    throw new Error('请选择要上传的文件');
                }

                const formData = new FormData();
                formData.append('file', fileInput.files[0]);

                const response = await axios.post('http://127.0.0.1:5000/api/uploadFile', formData);

                console.log('上传成功:', response.data);
            } catch (error) {
                console.error('上传失败:', error.message);
            }
        };


        return {
            handleFileUpload,
            uploadFile
        };
    }
};
</script>