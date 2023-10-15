<template>
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" :ellipsis="false" @select="handleSelect">
        <el-menu-item index="0">
            <img style="width: 100px" src="/element-plus-logo.svg" alt="Element logo" />
        </el-menu-item>
        <div class="flex-grow" />
        <el-menu-item index="1">
            <ElButton type="primary">
                下载
            </ElButton>
        </el-menu-item>
        <el-menu-item index="2">
            <ElButton type="primary">
                上传
            </ElButton>
        </el-menu-item>
        <el-sub-menu index="3">
            <template #title>用户</template>
            <el-menu-item index="3-1">设置</el-menu-item>
            <el-menu-item index="3-2">退出</el-menu-item>
        </el-sub-menu>
    </el-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue';

const activeIndex = ref('1')
const handleSelect = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}
</script>

<style>
.flex-grow {
    flex-grow: 1;
}
</style>
