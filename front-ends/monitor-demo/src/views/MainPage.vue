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

                <el-divider class="mydivider" />

                <!-- 每个主界面部分 -->
                <el-main class="right-main">
                    <router-view />
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script>
import { defineComponent, onUpdated } from "vue";
import CommonHeader from "../components/CommonHeader.vue";
import CommonAside from "../components/CommonAside.vue";
import CommonTab from "../components/CommonTab.vue";
import { useStore } from "vuex";

export default defineComponent({
    components: {
        CommonHeader,
        CommonAside,
        CommonTab,
    },

    setup() {
        const store = useStore(); // 确保从 Vuex 获取 store 实例

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

        onUpdated(() => {
            store.commit("setMenu", userlist); // 提交到 Vuex
        });
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

    & > .el-container {
        height: 100%;

        & > .el-aside {
            height: 100%;
        }
    }
}

.el-main {
    padding: 0 !important;
}

.mydivider {
    margin-top: 0px;
    margin-bottom: 10px;
}
</style>
