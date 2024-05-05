<template>
    <el-aside
        :width="$store.state.isCollapse ? '205px' : '64px'"
        class="common-layout"
    >
        <el-menu
            class="el-menu-vertical-demo"
            :collapse="!$store.state.isCollapse"
            :collapse-transition="false"
        >
            <div v-show="$store.state.isCollapse" class="header-title">
                <img
                    src="../assets/icons/home-icon.png"
                    alt="Home"
                    class="header-icon"
                />
                <h3>Monitor.</h3>
            </div>
            <!-- <h3 v-show="!$store.state.isCollapse">后台</h3> -->

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
                <template #title>
                    <component class="icons" :is="item.icon"></component>
                    <span style="font-weight: bold; color: #606266">{{
                        item.label
                    }}</span>
                </template>
                <el-menu-item-group>
                    <el-menu-item
                        :index="subItem.path"
                        v-for="(subItem, subIndex) in item.children"
                        :key="subIndex"
                        @click="clickMenu(subItem)"
                    >
                        <component class="icons" :is="subItem.icon"></component>
                        <span style="font-weight: normal">{{
                            subItem.label
                        }}</span>
                    </el-menu-item>
                </el-menu-item-group>
            </el-sub-menu>
        </el-menu>
    </el-aside>
</template>

<script>
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
    setup() {
        const store = useStore();
        const router = useRouter();
        const list = [
            {
                path: "/home",
                name: "home",
                label: "首页",
                icon: "HomeFilled",
                url: "UserManage/UserManage",
            },
            {
                path: "/user",
                name: "user",
                label: "个人信息",
                icon: "UserFilled",
                url: "UserManage/UserManage",
            },
            {
                path: "/monitorPage",
                name: "monitorPage",
                label: "信息监测",
                icon: "Platform",
                url: "UserManage/UserManage",
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
                        url: "Other/PageOne",
                    },
                    {
                        path: "/rrPage",
                        name: "rrPage",
                        label: "呼吸率",
                        icon: "DArrowRight",
                        url: "Other/PageTwo",
                    },
                    {
                        path: "/spo2Page",
                        name: "spo2Page",
                        label: "血氧饱和度",
                        icon: "DArrowRight",
                        url: "Other/PageTwo",
                    },
                ],
            },
        ];

        const asyncList = list;
        // const asyncList = store.state.menu; // 异步列表

        // 有子列表
        const noChildren = () => {
            return asyncList.filter((item) => !item.children);
        };

        // 无子列表
        const hasChildren = () => {
            return asyncList.filter((item) => item.children);
        };

        // 路由跳转
        const clickMenu = (item) => {
            router.push({
                name: item.name,
            });
            // vuex 来管理
            store.commit("selectMenu", item);
        };

        return {
            list,
            noChildren,
            hasChildren,
            clickMenu,
        };
    },
};
</script>

<style lang="scss" scoped>
.common-layout {
    background-color: #fafcff;
    box-shadow: 0.5px 1px 3px rgba(0, 0, 0, 0.4);
    margin-right: 8px;
}

.icons {
    width: 18px;
    height: 18px;
    margin-right: 10px;
}

.el-menu {
    border-right: none;
    background-color: #fafcff;

    .el-menu-item,
    .el-sub-menu .el-menu-item-group .el-menu-item {
        color: #606266;
        line-height: 48px;
        font-weight: bold;
        text-align: left;
    }

    .el-menu-item.is-active,
    .el-sub-menu .el-menu-item-group .el-menu-item.is-active {
        color: #409eff;
        border-left: 4px solid #409eff;
    }
}

.el-sub-menu .el-menu-item-group {
    .el-menu-item {
        margin-left: 20px;
    }
}

.header-title {
    display: flex;
    align-items: flex-end;
    justify-content: flex-start;
    margin-top: 25px;
    margin-left: 18px;
    margin-bottom: 10px;
    h3 {
        color: #409eff;
        font-weight: bold;
        font-size: 28px;
        margin: 0;
    }
}

.header-icon {
    width: 30px;
    height: 30px;
    margin-right: 10px;
    background-color: #fafafa;
    align-self: flex-end;
}
</style>
