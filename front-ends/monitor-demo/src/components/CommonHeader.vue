<template>
  <el-header >
    <div class="l-content">
       <!-- 在按钮左边添加文本 -->
       <div class="welcome-texts">
        <div class="welcome">Good Morning Mr.Liu!</div>
        <div class="user-greeting">Hello Mr.Liu, welcome back!</div>
      </div>

      <!-- 图标的展示 -->
      <el-button size="small" plain @click="handleCollapse">
        <el-icon :size="20">
          <Menu />
        </el-icon>
      </el-button>



      <el-breadcrumb separator="/" class="bread">
        <!-- 首页是一定存在的所以直接写死 -->
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>

        <el-breadcrumb-item :to="current.path" v-if="current">{{
          current.label
        }}</el-breadcrumb-item>
      </el-breadcrumb>

    </div>



    <div class="r-content">
      <el-input placeholder="输入搜索内容" style="width: 280px" prefix-icon="el-icon-search">
        <template #prefix>
        <el-icon class="el-input__icon"><search /></el-icon>
      </template>
      </el-input>
      <!-- 用户信息和下拉菜单 -->
      <el-dropdown>
        <span class="el-dropdown-link">
          <img :src="getImageUrl('user')" alt="用户头像" class="user" />
        </span>

        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>个人中心</el-dropdown-item>
            <el-dropdown-item @click="handleLoginOut">退出</el-dropdown-item>
          </el-dropdown-menu>
        </template>

      </el-dropdown>

    </div>
  </el-header>
</template>


<script>
import { computed } from "vue-demi";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  setup(){
    const store = useStore();
    const router = useRouter();

    let getImageUrl = (user) => {
      // console.log(import.meta.url);
      // console.log(new URL("../assets/images/user.png", import.meta.url));
      // return new URL(`../assets/images/${user}.png`, import.meta.url).href;
      return require(`@/assets/images/${user}.png`);
    };

    // 折叠
    let handleCollapse = () => {
      // 调用vuex中的mutations
      store.commit("updateIsCollapse");
    };


    // 退出登陆
    let handleLoginOut = () => {
      store.commit("cleanMenu");
      router.push({
        name: "login",
      });
    };

    const current = computed(() => {
      return store.state.currentMenu;
    });


    return {
      getImageUrl,
      handleCollapse,
      handleLoginOut,
      current
    };
  }
};
</script>


<style lang="less" scoped>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 80px;
  background: #FAFAFA;
  border-bottom: 1px solid rgba(0, 0, 0, 0.2);
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
}

.l-content {
  display: flex;
  align-items: center;

  .welcome-texts {
    display: flex;
    flex-direction: column;
    margin-right: 30px;

    .welcome {
      font-size: larger;
      font-weight: bold;
      color: black;
    }

    .user-greeting {
      font-size: smaller;
      color: grey;
    }
  }
}

.r-content {
  display: flex;
  align-items: center;
  justify-content: flex-end;

  .el-input {
    width: 200px; // 可根据需要调整宽度
  }

  .user {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-left: 20px;
  }
}

:deep(.bread span) {
  color: #fff !important;
  cursor: pointer !important;
}

:deep(.el-dropdown-menu) {
  box-shadow: none !important; /* 移除阴影 */
  border: none !important; /* 移除边框 */
}

</style>
