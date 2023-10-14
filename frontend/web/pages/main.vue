<template>
    <div class="common-layout">
        <el-container>
            <el-header>
                <Banner />

            </el-header>
            <el-container>
                <el-aside width="200px">Aside</el-aside>
                <el-container>
                    <el-main>

                        <FilesTable />
                    </el-main>
                    <el-footer>Footer</el-footer>
                </el-container>
            </el-container>
        </el-container>
    </div>
</template>


<style>
.page-index {
    padding-top: 60px;
    text-align: center;
}
</style>

