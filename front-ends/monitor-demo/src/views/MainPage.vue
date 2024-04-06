<template>
  <div class="common-layout">
    <el-container class="lay-container">
      <!-- 左侧主要 -->
      <common-aside class="aside-main" />

      <!-- 右侧主要 -->
      <el-container>
        <!-- 头部 -->
        <common-header />

        <!-- tab面包屑 -->
        <common-tab />

        <!-- 每个主界面部分 -->
        <el-main class="right-main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>


<script>
import { defineComponent } from "vue";
import CommonHeader from "../components/CommonHeader.vue";
import CommonAside from "../components/CommonAside.vue";
import CommonTab from "../components/CommonTab.vue"

export default defineComponent({
  components: {
    CommonHeader,
    CommonAside,
    CommonTab,
  },

});
</script>

<style lang="scss" scoped>
.el-container {
  flex-wrap: wrap;
  align-items: flex-start;
  height: 100%;
  margin-right: 5px;
}

.common-layout {
  
  .lay-container {
    margin-right: 0px;
    flex-wrap: nowrap;
    

    .right-main {
      height: 100%;
    }
  }

  height: 100%;

  &>.el-container {
    height: 100%;

    &>.el-aside {
      height: 100%;
    }
  }
}

.el-main {
  padding: 0 !important; // 强制设置内边距为0
}
</style>