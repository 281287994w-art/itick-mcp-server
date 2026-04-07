# 使用 Python 3.14 作为基础镜像
FROM python:3.14-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    ITICK_API_BASE=https://api.itick.org

# 安装系统依赖和 uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && ln -s /root/.local/bin/uv /usr/local/bin/uv \
    && ln -s /root/.local/bin/uvx /usr/local/bin/uvx

# 复制项目文件
COPY pyproject.toml requirements.txt ./

# 使用 uv 安装依赖（更快）
RUN uv pip install --system --no-cache-dir -r requirements.txt

# 复制剩余项目文件
COPY . .

# 暴露 HTTP 端口（FastMCP streamable-http 默认使用 8000）
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# 默认以 HTTP 模式启动
CMD ["python", "server.py", "--transport", "http"]
