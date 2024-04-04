<template>
  <el-header>
    <div class="l-content">
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
    let store = useStore();
    const router = useRouter();

    let getImageUrl = (user) => {
      console.log(import.meta.url);
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
// header整体
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  background: rgb(43, 141, 197);
}

// 左侧
.l-content {
  display: flex;
  align-items: center;
  .el-button {
    margin-right: 20px;
  }
  h3 {
    color: #fff;
  }
}

// 右侧
.r-content {
  .user {
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
}

:deep(.bread span) {
  color: #fff !important;
  cursor: pointer !important;
}

</style>