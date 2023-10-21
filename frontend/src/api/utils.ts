export const baseUrlApi = (url: string) => {
    const apiUrl = `/api/${url}`;  // 用于和Nginx代理配置相匹配的路径
    return process.env.NODE_ENV === "development"
        ? apiUrl
        : url; // 在生产环境中，仍然使用相同的代理路径
};
