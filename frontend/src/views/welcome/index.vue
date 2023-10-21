<script setup lang="ts">
import { baseUrlApi } from "@/api/utils";
import { http } from "@/utils/http";
import PureTable from "@pureadmin/table";
import qs from "qs";
import { onMounted, ref } from "vue";

export type FilesResult = {
    /** 是否请求成功 */
    success: boolean;
    path: string;
    total: number;
    items: any[];
};

export type DownloadResult = {
    /** 是否请求成功 */
    success: boolean;
    /** 下载的文件 */
    file: Blob;
};

const tableData = ref([]);
// 在 'onMounted' 钩子中发起 HTTP 请求
onMounted(async () => {
    try {
      const response = await http.request<FilesResult>("get", baseUrlApi("/api/list/"));
      const items = response.items;
      items.forEach(item => {
        item.type = item.type === 0 ? '文件夹' : '文件';
      });
        tableData.value = response.items;
    } catch (error) {
        console.error('There was an error fetching the data:', error);
    }
});

const tableRef = ref();
const multipleSelection = ref([]);
const toggleSelection = (rows?: any) => {
    const { toggleRowSelection, clearSelection } = tableRef.value.getTableRef();
    if (rows) {
        rows.forEach(row => {
            toggleRowSelection(row, undefined);
        });
    } else {
        clearSelection();
    }
};
const handleSelectionChange = val => {
    multipleSelection.value = val;
};
const handleRowClick = async row => {
  if (row.type === '文件夹') {
    try {
      const response = await http.request<FilesResult>("get", baseUrlApi("/api/list/") + row.name);
      const items = response.items;
      items.forEach(item => {
        item.type = item.type === 0 ? '文件夹' : '文件';
      });
      tableData.value = response.items;
    } catch (error) {
      console.error('There was an error fetching the data:', error);
    }
  } else {
    alert('这是一个文件，无法打开！');
  }
};
const handleDownload = async () => {
  if (multipleSelection.value.length === 0) {
        alert('请至少选择一项进行下载！');
        return;
    }

    // 获取所有选中文件的文件名
    const selectedFiles = multipleSelection.value.map(item => item.name);

    try {
      // 发送请求并指定响应类型为 blob，这是处理文件下载的关键, 使用get请求
        const response = await http.request<Blob>("get", baseUrlApi("/api/download/"), {
            responseType: 'blob',
            params: {
                files: selectedFiles
          },
            paramsSerializer: params => {
              return qs.stringify(params, { arrayFormat: 'repeat' });
            }
        });
      // 检查是否实际上没有返回文件（可能是一个错误响应）
                if (response.size === 0) {
            throw new Error('没有文件可供下载，或发生了其他错误。');
        }

        // 检查是否为单个文件下载并获取文件类型
        const isSingleFile = multipleSelection.value.length === 1;
        const fileType = isSingleFile ? 'application/octet-stream' : 'application/zip';

        // 如果是单个文件，使用文件的实际名称，否则使用默认的压缩包名称
        const defaultFileName = isSingleFile ? selectedFiles[0] : 'files.zip';

        // 从响应中提取文件
        const file = new Blob([response], { type: fileType });

        // 创建指向该文件的URL
        const fileURL = URL.createObjectURL(file);

        // 创建一个链接并设置URL和默认的文件名
        const link = document.createElement('a');
        link.href = fileURL;
        link.setAttribute('download', defaultFileName); 

        // 将链接添加到页面中，触发点击事件并移除链接
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

    } catch (error) {
        console.error('下载文件时出错:', error);
        alert('下载文件时出错');
    }

};
const handleUpload = async () => {
    // 创建一个文件输入控件
    const input = document.createElement('input');
    input.type = 'file';
    input.click();

    input.onchange = async () => {
        // 检查是否选择了文件
        if (!input.files || input.files.length === 0) {
            return;
        }

        // 创建一个FormData实例来包装文件数据
        const formData = new FormData();
        formData.append('file', input.files[0]); // 注意这里的字段名是 'file'
      console.log("formData", formData)
        console.log("file", input.files[0])
        try {
            // 发送请求到您的后端服务
          const response = await http.request<FilesResult>("post", baseUrlApi("/api/upload/"),
            { data: formData, headers: { 'Content-Type': 'multipart/form-data' } });
          
            if (response.success === true) {
                alert('上传成功！');
            // 刷新页面
                window.location.reload();
            } else {
                console.error('上传失败:', response);
            }
        } catch (error) {
            console.error('上传文件时出错:', error);
        }
    };
};

const handleNewFolder = async () => {
    const folderName = prompt('请输入文件夹名称：');
    if (!folderName) {
        return;
    }

    try {
        const response = await http.request<FilesResult>("post",baseUrlApi("api/mkdir/"+ folderName) , {
        });

        if (response.success === true) {
            alert('创建成功！');
            // 刷新页面
            window.location.reload();
        } else {
            console.error('创建失败:', response);
        }
    } catch (error) {
        console.error('创建文件夹时出错:', error);
    }
};

const columns: TableColumnList = [
    {
        type: "selection",
        align: "left"
    },
    {
        label: "名称",
        prop: "name"
    },
    {
        label: "大小",
        prop: "size"
    },
  {
    label: "类型",
    prop: "type"
    }
];
</script>

<template>
      <pure-table ref="tableRef" :data="tableData" :columns="columns"
                @selection-change="handleSelectionChange" 
                @row-click="handleRowClick" height="360"> </pure-table>
  <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px;">
            <div>
                <el-button @click="toggleSelection(tableData)">全选</el-button>
                <el-button @click="toggleSelection()">清除</el-button>
            </div>
            <div>

                <el-button type="primary" icon="el-icon-download" @click="handleNewFolder">新建文件夹</el-button>
                <el-button type="primary" icon="el-icon-download" @click="handleDownload">下载</el-button>
                <el-button type="primary" icon="el-icon-download" @click="handleUpload">上传</el-button>
            </div>
        </div>
</template>

