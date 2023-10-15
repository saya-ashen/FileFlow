<template>
    <el-table ref="multipleTableRef" :data="tableData" style="width: 100%" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" />
        <el-table-column label="Date" width="120">
            <template #default="scope">{{ scope.row.date }}</template>
        </el-table-column>
        <el-table-column property="name" label="Name" width="120" />
        <el-table-column property="address" label="Address" show-overflow-tooltip />
    </el-table>
    <div style="margin-top: 20px">
        <el-button @click="toggleSelection(tableData)">全选</el-button>
        <el-button @click="toggleSelection()">清除</el-button>
    </div>
</template>

<script lang="ts" setup>
import { ElTable } from 'element-plus';
import { ref } from 'vue';

interface User {
    date: string
    name: string
    address: string
}

const multipleTableRef = ref<InstanceType<typeof ElTable>>()
const multipleSelection = ref<User[]>([])
const toggleSelection = (rows?: User[]) => {
    if (rows) {
        rows.forEach((row) => {
            // TODO: improvement typing when refactor table
            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-expect-error
            multipleTableRef.value!.toggleRowSelection(row, undefined)
        })
    } else {
        multipleTableRef.value!.clearSelection()
    }
}
const handleSelectionChange = (val: User[]) => {
    multipleSelection.value = val
}

const tableData: User[] = [
    {
        date: '2016-05-03',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-02',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-04',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-01',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-08',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-06',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
    {
        date: '2016-05-07',
        name: 'Tom',
        address: 'No. 189, Grove St, Los Angeles',
    },
]
</script>




<!--<template>
    <el-table :data="tableData" height="250" style="width: 100%">
        <el-table-column prop="name" label="名称" width="180" />
        <el-table-column prop="size" label="大小" width="180" />
        <el-table-column prop="date" label="修改日期" />
    </el-table>
</template>



<script lang="ts" setup>
const tableData = [
    {
        date: '2016-05-03',
        name: 'Tom',
        size: 100,
    },
    {
        date: '2016-05-02',
        name: 'Tom',
        size: 100,
    },
    {
        date: '2016-05-04',
        name: 'Tom',
        size: 100,
    },
    {
        date: '2016-05-01',
        name: 'Tom',
        size: 100,
    },
    {
        date: '2016-05-08',
        name: 'Tom',
        size: 100,
    },
    {
        date: '2016-05-06',
        name: 'Tom',
        size: 100,
    },
    {
        date: '2016-05-07',
        name: 'Tom',
        size: 100,
    },
]
</script>
-->