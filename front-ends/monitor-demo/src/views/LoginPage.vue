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
            <el-input v-model="loginForm.username" placeholder="请输入账号"></el-input>
          </el-form-item>
          <el-form-item label="密码" required>
            <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
          </el-form-item>
          <el-button :disabled="loading" type="primary" class="login-button" @click="login">登录</el-button>
          <div class="forget-section">
            <a class="forget-password">忘记密码</a>
            <a class="recover-password">立即找回</a>
          </div>
        </el-form>
      </el-card>
    </div>
    <div class="info-section">
      <el-link :icon="Edit" type="primary" class="info-link">关于项目</el-link>
      <div class="copyright">@copyright 2024 lwx</div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router'; // 导入vue-router用于导航
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default {
  name: 'LoginPage',
  setup() {
    const router = useRouter(); // 获取router实例，用于页面跳转
    const loginForm = ref({
      username: '',
      password: '',
    }); // 创建响应式的表单数据对象
    const loading = ref(false); // 控制按钮的加载状态


    const loginSuccess = () => {
      showClose: true,
      ElMessage({
        showClose: true,
        message: '登陆成功',
        type: 'success',
        duration: 1500
      })
    }

    const loginFail = () => {
      ElMessage({
        showClose: true,
        message: '登陆失败, 用户名或密码错误.',
        type: 'error',
        duration: 1500,
      })
    }

    // 登录方法
    const login = async () => {
      loading.value = true;
      try {
        console.log(event)
        // 检查用户名和密码是否为空
        if (!loginForm.value.username || !loginForm.value.password) {
          throw new Error('账号和密码不能为空');
        }
        // 模拟登录逻辑，实际开发中应将用户数据发送到后端进行验证
        console.log('Logging in with:', loginForm.value.username, loginForm.value.password);
        
        const response = axios({
          method: 'GET',
          url: 'http://127.0.0.1:5000/api/database/isUser',
          params: {
            username: loginForm.value.username,
            password: loginForm.value.password
          }
        }).then((result) => {
          if(result.data.code === 200){
            console.log('成功');
            loginSuccess();
            router.push('/home'); // 使用router实例跳转，这里假设你的Home页面路由为 '/home'
          } 
          else {
            loginFail()
          }
        }).catch((err) => {
          console.log(err)
        });
        console.log(response);
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
  width: 80%;
  flex-grow: 1;
  background: url('../assets/images/loginBackground.png') no-repeat center center;
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
}

.login-section {
  flex-basis: 600px;
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
  max-width: 600px;
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
  bottom: 10px;
  left: 68%;
  transform: translateX(-50%);
}

.info-link {
  color: #409eff;
  display: block;
}
</style>
