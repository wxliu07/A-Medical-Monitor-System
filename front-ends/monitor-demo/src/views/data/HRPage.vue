<template>
    <div>
        HRPage
        <el-button type="primary" class="login-button" @click="isAdmin">测试</el-button>
    </div>
</template>

<script>
import { getCurrentInstance } from 'vue'

export default {
    setup() {
        const { proxy } = getCurrentInstance(); // vue3不能用this了
        const isAdmin = async () => {
            try {
                let res = await proxy.$api.isAdmin({
                    username: 'liu',
                    password: '123'
                })
                console.log(res)

            } catch (error) {
                console.log(error)
            }
        }

        return {
            isAdmin
        }
    }
};

</script>