<template>
    <el-form :model="form" label-width="120px">
        <el-form-item label="用户名">
            <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="密码">
            <el-input v-model="form.pass" />
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="onSubmit">登录</el-button>
            <el-button>注册</el-button>
        </el-form-item>
    </el-form>
</template>

<script lang="ts" setup>
import { reactive } from 'vue';

// do not use same name with ref
const form = reactive({
    name: '',
    pass: '',
})

const onSubmit = () => {
    /*try {
        const res = fetch('http://localhost:8000/api/token', {
            method: 'POST',
            body: JSON.stringify(form),
        });
    } catch (error) {
        if (error instanceof Error) {
            console.log('error message: ', error.message);
            return error.message;
        } else {
            console.log('unexpected error: ', error);
            return 'An unexpected error occurred';
        }
    }*/
    const { data: post, refresh } = useFetch('http://localhost:8000/api/token', {
        method: 'POST',
        body: JSON.stringify(form),
    });
}
</script>


<style>
.page-index {
    padding-top: 60px;
    text-align: center;
}
</style>
