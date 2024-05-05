<template>
    <div class="login-container">
        <div class="image-section">
            <!-- Image section remains empty here as it's handled via CSS -->
        </div>
        <div class="login-section">
            <div class="header-text">计算机辅助医疗监护系统</div>
            <el-card class="login-card">
                <el-form class="login-form" label-position="left">
                    <el-form-item label="账号" required>
                        <el-input
                            v-model="loginForm.username"
                            placeholder="请输入账号"
                            style="width: 305px"
                        ></el-input>
                    </el-form-item>
                    <el-form-item label="密码" required>
                        <el-input
                            v-model="loginForm.password"
                            type="password"
                            placeholder="请输入密码"
                            style="width: 305px"
                        ></el-input>
                    </el-form-item>
                    <el-button
                        :disabled="loading"
                        type="primary"
                        class="login-button"
                        @click="login"
                        style="width: 355px"
                        >登录</el-button
                    >
                    <div class="forget-section">
                        <a class="forget-password">忘记密码</a>
                        <a class="recover-password">立即找回</a>
                    </div>
                </el-form>
            </el-card>
        </div>
        <div class="info-section">
            <el-link :icon="Share" type="primary" class="info-link">
                <el-icon><Share /></el-icon>&nbsp;关于项目</el-link
            >
            <div class="copyright">@copyright 2024 lwx</div>
        </div>
    </div>
</template>

<script>
import { ref } from "vue";
import { reactive } from "vue-demi";
import { useStore } from "vuex";
import { useRouter } from "vue-router"; // 导入vue-router用于导航
import { ElMessage } from "element-plus";
import { getCurrentInstance } from "vue-demi";
import axios from "axios";

export default {
    name: "LoginPage",
    setup() {
        const userlist = [
            {
                path: "/",
                name: "home",
                label: "首页",
                icon: "HomeFilled",
                url: "home/HomePage",
            },
            {
                path: "/user",
                name: "user",
                label: "个人信息",
                icon: "UserFilled",
                url: "user/UserPage",
            },
            {
                path: "/monitorPage",
                name: "monitorPage",
                label: "信息监测",
                icon: "Platform",
                url: "monitor/Monitor",
            },
            {
                path: "/other",
                label: "数据纵览",
                icon: "Operation",
                children: [
                    {
                        path: "/hrPage",
                        name: "hrPage",
                        label: "心率",
                        icon: "DArrowRight",
                        url: "data/HRPage",
                    },
                    {
                        path: "/rrPage",
                        name: "rrPage",
                        label: "呼吸率",
                        icon: "DArrowRight",
                        url: "data/RRPage",
                    },
                    {
                        path: "/spo2Page",
                        name: "spo2Page",
                        label: "血氧饱和度",
                        icon: "DArrowRight",
                        url: "data/SpO2Page",
                    },
                ],
            },
        ];
        const adminlist = [
            {
                path: "/userControlPage",
                name: "userControlPage",
                label: "用户管理",
                icon: "UserFilled",
                //url: "admin/UsersControlPage"
            },
            {
                path: "/userInfolPage",
                name: "userInfolPage",
                label: "监测信息",
                icon: "Platform",
                // url: "admin/UserInfoPage"
            },
            {
                path: "/usersVideoPage",
                name: "usersVideoPage",
                label: "视频记录",
                icon: "Operation",
                //url: "admin/UsersVideoPage"
            },
        ];

        const router = useRouter(); // 获取router实例，用于页面跳转
        const loginForm = ref({
            username: "",
            password: "",
        }); // 创建响应式的表单数据对象
        const loading = ref(false); // 控制按钮的加载状态

        const loginSuccess = () => {
            ElMessage({
                showClose: true,
                message: "登陆成功",
                type: "success",
                duration: 3000,
            });
            setTimeout(() => {
                // router.push("/home"); // 3秒后跳转到首页
            }, 3000); // 3000毫秒后执行，与消息持续时间相同
        };

        const loginFail = () => {
            ElMessage({
                showClose: true,
                message: "登陆失败, 用户名或密码错误.",
                type: "error",
                duration: 3000,
            });
        };

        const { proxy } = getCurrentInstance();
        const store = useStore();
        // 登录方法
        const login = async () => {
            loading.value = true;
            try {
                // 检查用户名和密码是否为空
                if (!loginForm.value.username || !loginForm.value.password) {
                    throw new Error("账号和密码不能为空");
                }

                // 模拟登录逻辑，实际开发中应将用户数据发送到后端进行验证
                console.log(
                    "Logging in with:",
                    loginForm.value.username,
                    loginForm.value.password
                );

                // 检查是否用户
                axios({
                    method: "GET",
                    url: "http://127.0.0.1:5000/api/database/isUser",
                    params: {
                        username: loginForm.value.username,
                        password: loginForm.value.password,
                    },
                })
                    .then((result) => {
                        console.log(result);
                        if (result.data.code === 200) {
                            console.log("成功");
                            store.commit("setMenu", userlist);
                            // store.commit("addMenu", router);
                            router.push({ name: "home" });
                            loginSuccess();
                        } else {
                            // 若不是用户，检查是否管理员
                            axios({
                                method: "GET",
                                url: "http://127.0.0.1:5000/api/database/isAdmin",
                                params: {
                                    username: loginForm.value.username,
                                    password: loginForm.value.password,
                                },
                            })
                                .then((result2) => {
                                    console.log(result2);
                                    if (result2.data.code === 200) {
                                        console.log("管理员成功");
                                        store.commit("setMenu", adminlist);
                                       
                                        router.push({
                                            name: "userControlPage",
                                        });
                                        loginSuccess();
                                    } else {
                                        // 如果也不是管理员
                                        loginFail();
                                    }
                                })
                                .catch((err) => {
                                    loginFail();
                                    console.error(err);
                                });
                        }
                    })
                    .catch((err) => {
                        loginFail();
                        console.error(err);
                    });
            } catch (error) {
                alert(error.message); // 显示错误信息
            } finally {
                loading.value = false;
            }
        };

        return {
            loginForm,
            loading,
            login,
        };
    },
};
</script>

<style scoped>
.login-container {
    display: flex;
    min-height: 100vh;
    overflow: hidden;
}

.image-section {
    width: 900px;
    flex-grow: 2;
    background: url("../assets/images/loginBackground.png") no-repeat center
        center;
    background-size: cover;
    clip-path: polygon(0 0, 100% 0, 60% 120%, 0 100%);
    background-color: #fff;
}

.header-text {
    color: #409eff;
    font-size: 30px;
    text-align: center;
    margin: 20px 0;
    margin-right: 40px;
    margin-bottom: 20px;
}

.login-section {
    flex-basis: 500px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: #fff;
    padding-top: 5vh;
}

.login-card {
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    width: 100%;
    max-width: 450px;
    margin-right: 70px;
}

.login-form {
    margin: 20px;
}

.login-button {
    width: 100%;
}

.forget-section {
    margin-top: 10px;
    text-align: right;
    font-size: 0.8rem;
}

.forget-password,
.recover-password {
    color: #409eff;
    margin: 0 5px;
}

.forget-password:hover,
.recover-password:hover {
    text-decoration: underline;
}

.info-section {
    color: #999;
    font-size: 0.8rem;
    text-align: left;
    position: absolute;
    bottom: 30px;
    left: 67%;
    transform: translateX(-50%);
}

.info-link {
    color: #409eff;
    display: block;
    bottom: 10px;
}
</style>
