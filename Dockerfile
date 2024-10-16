# 使用 Python 的官方基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 文件到容器中
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制当前目录下的所有文件到容器的工作目录中
COPY . .

# 开放 Flask 应用的端口
EXPOSE 5000

# 设置环境变量，告诉 Flask 运行在开发模式
ENV FLASK_ENV=development

# 启动 Flask 应用
CMD ["flask", "run", "--host=0.0.0.0"]
