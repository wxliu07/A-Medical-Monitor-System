<template>
    <div>
        <el-card style="width: 800px; margin-top: 10px; margin-left: 10px;" shadow="hover">
            <el-form label-width="70px" size="large" label-position="left">
                <el-upload class="avatar-uploader" :action="'http://localhost:9090/file/upload'" :show-file-list="false"
                    :on-success="handleAvatarSuccess">
                    <img v-if="form.avatarUrl" src="../../assets/images/user.png" class="avatar">
                    <i v-else class="el-icon-plus avatar-uploader-icon" />
                </el-upload>
                <el-form-item label="用户名" style="margin-left: 200px; margin-top: -160px">
                    <el-input v-model="form.username" disabled autocomplete="off" style="width: 455px"></el-input>
                </el-form-item>
                <el-form-item label="昵称" style="margin-left: 200px">
                    <el-input v-model="form.nickname" autocomplete="off" style="width: 455px"></el-input>
                </el-form-item>
                <el-form-item label="性别" style="margin-left: 200px; height: 40px;">
                    <el-select v-model="form.sex" placeholder="请选择您的性别" style="width: 455px; height: 40px;">
                        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="邮箱" style="margin-left: 200px">
                    <el-input v-model="form.email" autocomplete="off" style="width: 455px"></el-input>
                </el-form-item>
                <el-form-item label="电话" style="margin-left: 200px">
                    <el-input v-model="form.phone" autocomplete="off" style="width: 455px"></el-input>
                </el-form-item>
                <el-form-item label="地址" style="margin-left: 200px;">
                    <el-input type="textarea" v-model="form.address" autocomplete="off" style="width: 455px; height: 40px;"></el-input>
                </el-form-item>
                <div class="buttons-container">
    <el-button type="primary" @click="save">保 存</el-button>
    <el-button type="primary" @click="return1">返回主页</el-button>
</div>


            </el-form>
        </el-card>
    </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';

export default {
    name: "Person",
    setup() {
        const form = reactive({
            username: 'liu',
            nickname: '刘文旭',
            sex: '男',
            email: 'wenxuliu@mail.hfut.edu.dn',
            phone: '123456',
            address: '安徽·宣城',
            avatarUrl: '../../assets/images/user.png', // 头像固定地址
        });

        const options = ref([{
            value: '男',
            label: '男'
        }, {
            value: '女',
            label: '女'
        }]);

        const validatePhone = /^1[3,4,5,6,7,8,9][0-9]{9}$/;

        // 替代原来的 mounted 钩子
        onMounted(() => {
            // 获取地理位置代码...
        });

        // 替代原来的 methods
        const load = () => {
            // 加载数据代码...
        };

        const save = () => {
            // 保存数据代码，函数体已移除
        };

        const return1 = () => {
            // 返回主页代码，函数体已移除
        };

        // 确保返回所有在模板中使用的响应式数据和函数
        return {
            form,
            options,
            validatePhone,
            load,
            save,
            return1,
        };
    }
}
</script>


<style>
.avatar-uploader {
    text-align: left;
    padding-bottom: 0px;
}

.avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.avatar-uploader .el-upload:hover {
    border-color: #409EFF;
}

.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 138px;
    height: 100px;
    line-height: 138px;
    text-align: center;
}

.avatar {
    width: 160px;
    height: 160px;
    display: block;
}

.el-form-item label {
    text-align: left;
    position: relative;
    font-size: 16px; /* 调整字体大小 */
    color: #4a4a4a;
    font-weight: bold;
    padding-left: 10px; /* 确保文本与星号之间的间距 */
}

.el-form-item label::before {
    content: "*";
    color: red;
    position: absolute;
    left: 0;
    margin-right: 0px; /* 星号与文本之间的距离 */
}

.el-input, .el-select {
    width: 100px;
    height: 35px; /* 统一输入框和选择框的高度 */
    font-weight: normal;
}

.el-button {
    height: 28px; /* 按钮高度 */
    width: 80px; /* 按钮宽度 */
}

.el-form-item {
    margin-bottom: 30px;
    display: flex;
    align-items: center;
}

.el-form-item:first-child {
    margin-top: 0px; /* 调整用户名项与头像对齐 */
}

.el-card {
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.buttons-container {
    text-align: right;
    margin-top: auto;
    margin-right: 30px;
}
</style>

