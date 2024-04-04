<template>
    <el-row class="home" :gutter="20">
        <el-col :span="8" style="margin-top: 20px">
            <el-card shadow="hover">
                <div class="user">
                    <img src="../../assets/images/user.png" alt="" />
                    <div class="user-info">
                        <p class="name">Admin</p>
                        <p class="role">超级管理员</p>
                    </div>
                </div>
                <div class="login-info">
                    <p>上次登录时间:<span>2022-7-11</span></p>
                    <p>上次登录的地点:<span>北京</span></p>
                </div>
            </el-card>

        </el-col>


        <el-col :span="16" style="margin-top: 20px" class="right-num">
            <el-card shadow="hover" style="margin-top: 20px" height="450px">
                <el-table :data="monitorData">
                    <el-table-column v-for="(val, key) in monitorTableLable" :key="key" :prop="key" :label="val">
                    </el-table-column>
                </el-table>
            </el-card>
        </el-col>


        <div>
            <p>我是home部分</p>
            <input id="file" type="file" @change="handleFileUpload">
            <el-button :disabled="loading" type="primary" class="login-button" @click="uploadFile">上传文件</el-button>
        </div>

    </el-row>


</template>

<script>
import {
  getCurrentInstance,
  onMounted,
  reactive,
  ref,
} from "vue";
import axios from 'axios';

export default {
    setup() {
        // 定义文件状态
        const file = ref(null);

        let monitorData = ref([])

        const monitorTableLable = {
            emotion: 'Emotion',
            hr: 'Heart Rate',
            rr: 'Respiratory Rate',
            spo2: 'SpO2',
            time: 'Time'
        }
        
        const getMonitorData = () => {
            axios({
                method: 'GET',
                url: 'http://127.0.0.1:5000/api/database/getMonitorData',
                params: {
                    uid: 1,
                }
            }).then(response => {
                if (response.data && response.data.code === 300) {
                    console.log(response.data)
                    monitorData.value = response.data.data;
                }
                else {
                    console.error(response.data.info || 'Failed to fetch monitor data');
                }
            }
            )
                .catch(error => {
                    console.error('Error fetching monitor data:', error);
                }
                );
        }


        onMounted(() => {
            getMonitorData();
        });



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
            uploadFile,
            monitorData,
            monitorTableLable
        };
    }
};
</script>


<style lang="less" scoped>
.home {
    .user {
        display: flex;
        align-items: center;
        padding-bottom: 20px;
        border-bottom: 1px solid #ccc;
        margin-bottom: 20px;

        img {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            margin-right: 40px;
        }
    }

    .login-info {
        p {
            line-height: 30px;
            font-size: 14px;
            color: #999;

            span {
                color: #666;
                margin-left: 60px;
            }
        }
    }

    .num {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;

        .el-card {
            width: 32%;
            margin-bottom: 20px;
        }

        .icons {
            width: 80px;
            height: 80px;
            font-size: 30px;
            text-align: center;
            line-height: 80px;
            color: #fff;
        }

        .detail {
            margin-left: 15px;
            display: flex;
            flex-direction: column;
            justify-content: center;

            .num {
                font-size: 30px;
                margin-bottom: 10px;
            }

            .txt {
                font-size: 14px;
                text-align: center;
                color: #999;
            }
        }
    }

    .graph {
        margin-top: 20px;
        display: flex;
        justify-content: space-between;

        .el-card {
            width: 48%;
        }
    }
}
</style>