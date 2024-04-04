<template>
  <el-aside :width="$store.state.isCollapse ? '160px' : '64px'">
    <el-menu
      class="el-menu-vertical-demo"
      background-color="#545c64"
      text-color="#fff"
      :collapse="!$store.state.isCollapse"
      :collapse-transition="false"
    >
      <h3 v-show="$store.state.isCollapse">后台管理</h3>
      <h3 v-show="!$store.state.isCollapse">后台</h3>

      <!-- 没有子菜单的 -->
      <el-menu-item
        :index="item.path"
        v-for="item in noChildren()"
        :key="item.path"
        @click="clickMenu(item)"
      >
        <component class="icons" :is="item.icon"></component>
        <span>{{ item.label }}</span>
      </el-menu-item>

      <!-- 有子菜单的 -->
      <el-sub-menu
        :index="item.label"
        v-for="item in hasChildren()"
        :key="item.path"
      >
        <!-- 一级菜单 -->
        <template #title>
          <!-- 动态引用图标 -->
          <component class="icons" :is="item.icon"></component>
          <span>{{ item.label }}</span>
        </template>

        <!-- 二级菜单 -->
        <el-menu-item-group>
          <el-menu-item
            :index="subItem.path"
            v-for="(subItem, subIndex) in item.children"
            :key="subIndex"
            @click="clickMenu(subItem)"
          >
            <component class="icons" :is="subItem.icon"></component>
            <span>{{ subItem.label }}</span>
          </el-menu-item>
        </el-menu-item-group>
      </el-sub-menu>
    </el-menu>
  </el-aside>
</template>

<script>
// import { useStore } from "vuex";
import { useRouter } from "vue-router"; 

export default {
  setup() {
    // const store = useStore();
    const router = useRouter();
    const list = [
      {
        path: "/user",
        name: "user",
        label: "用户管理",
        icon: "user",
        url: "UserManage/UserManage",
      },
      {
        label: "其他",
        icon: "location",
        path: "/other",
        children: [
          {
            path: "/page1",
            name: "datapage1",
            label: "页面1",
            icon: "setting",
            url: "Other/PageOne",
          },
          {
            path: "/page2",
            name: "datapage2",
            label: "页面2",
            icon: "setting",
            url: "Other/PageTwo",
          },
        ],
      },
    ];

    // 有子列表
    const noChildren = () => {
      return list.filter(
        (item) => !item.children
      )
    };


    // 无子列表
    const hasChildren = () => {
      return list.filter(
        (item) => item.children
      )
    };

    // 路由跳转
    const clickMenu = (item) => {
      router.push({
        name: item.name,
      });
      // vuex 来管理
      // store.commit("selectMenu", item);
    };

    return {
      list,
      noChildren,
      hasChildren,
      clickMenu
    }


  },
};
</script>


<style lang="scss" scoped>
// .类;  .标签来控制样式
.icons {
  width: 18px;
  height: 18px;
}
.el-menu {
  border-right: none;
  h3 {
    line-height: 48px;
    color: #fff;
    text-align: center;
  }
}
</style>