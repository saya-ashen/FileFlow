# 第一阶段：构建阶段
FROM python:3.12-slim-bullseye as build-stage

WORKDIR /usr/src/app

# 安装构建工具和依赖
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# 使用虚拟环境来安装Python依赖
RUN python -m venv /venv

# 安装Python依赖
COPY requirements.txt .
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# 第二阶段：运行阶段
FROM python:3.12-slim-bullseye as run-stage

# 拷贝虚拟环境到新的基础镜像
COPY --from=build-stage /venv /venv

# 设置必要的环境变量
ENV VIRTUAL_ENV=/venv
ENV PATH="/venv/bin:$PATH"
ENV DEFAULT_CAPACITY=1099511627776 
ENV ALGORITHM=HS256
ENV JWT_SECRET_KEY=secret
ENV JWT_REFRESH_SECRET_KEY=refresh_secret

# 设置工作目录
WORKDIR /usr/src/app

# 复制应用
COPY . .

# 指定容器需要监听的端口
EXPOSE 8000

# 运行应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
