<script setup lang="ts">
</script>

<template>
    <div class="display-logo" flex="~" gap-2 items-center>
        <img class="logo" src="https://element-plus.org/images/element-plus-logo.svg" />
        <el-icon>
            <ElIconPlus />
        </el-icon>
        <NuxtLogo class="logo" />
    </div>
</template>

<style>
.display-logo {
    display: flex;
    justify-content: center;
    align-items: center;
}

.logo {
    max-height: 3rem;
}
</style>
