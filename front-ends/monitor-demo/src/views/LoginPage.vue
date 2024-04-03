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
            <el-input placeholder="请输入账号"></el-input>
          </el-form-item>
          <el-form-item label="密码" required>
            <el-input type="password" placeholder="请输入密码"></el-input>
          </el-form-item>
          <el-button type="primary" class="login-button">登录</el-button>
          <div class="forget-section">
            <a class="forget-password">忘记密码</a>
            <a class="recover-password">立即找回</a>
          </div>
        </el-form>
      </el-card>
    </div>
    <div class="info-section">
      <a href="#" class="info-link">关于项目</a>
      <div class="copyright">@copyright 2024 lwx</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
};
</script>

<style scoped>
.login-container {
  display: flex;
  min-height: 100vh;
  overflow: hidden;
}

.image-section {
  flex-grow: 1;
  background: url('../assets/images/loginBackground.png') no-repeat center center;
  background-size: cover;
  clip-path: polygon(0 0, 100% 0, 60% 100%, 0 100%);
}

.header-text {
  color: #409eff;
  font-size: 30px;
  text-align: center;
  margin: 20px 0;
  margin-right: 40px;
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
  max-width: 500px;
  margin-right: 40px;
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
  left: 50%;
  transform: translateX(-50%);
}

.info-link {
  color: #409eff;
  display: block;
}
</style>
