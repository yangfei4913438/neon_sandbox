# 1.使用ubuntu基础镜像来源
FROM ubuntu:24.04

# 2.安装过程避免交互式提示、设置主机名+默认编码（整合环境变量）
ENV DEBIAN_FRONTEND=noninteractive \
    HOSTNAME=sandbox \
    LANG=zh_CN.UTF-8 \
    LANGUAGE=zh_CN:zh \
    LC_ALL=zh_CN.UTF-8

# 3.将ubuntu默认的apt软件源地址统一换成阿里云镜像源
RUN sed -i 's|http://archive.ubuntu.com/ubuntu/|http://mirrors.aliyun.com/ubuntu/|g' /etc/apt/sources.list && \
    sed -i 's|http://security.ubuntu.com/ubuntu/|http://mirrors.aliyun.com/ubuntu/|g' /etc/apt/sources.list && \
    sed -i 's|http://ports.ubuntu.com/ubuntu-ports/|http://mirrors.aliyun.com/ubuntu-ports/|g' /etc/apt/sources.list

# 4.更新和安装基础软件后并移除依赖
RUN apt-get update &&  \
    # 安装基础依赖(含add-apt-repository所需的software-properties-common) \
    apt-get install -y --no-install-recommends \
    sudo bc curl wget gnupg software-properties-common supervisor \
    xterm socat xvfb x11vnc websockify\
    fonts-noto-cjk fonts-noto-color-emoji language-pack-zh-hans locales && \
    # 生成中文字符集 \
    locale-gen zh_CN.UTF-8 && \
    # 添加 dead snakes PPA(安装Python3.13) \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    # 添加 chromium 浏览器源 \
    add-apt-repository ppa:xtradeb/apps -y && \
    # 添加 node.js 24.x 版本(LTS) 源 \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_24.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
    # 更新软件源 \
    apt-get update && \
    # 安装Python 3.13版本(非uv) \
    apt-get install -y --no-install-recommends python3.13 python3.13-venv python3.13-dev && \
    # # 用Python内置的 ensure pip 模块安装pip(避免pip版本过旧) \
    python3.13 -m ensurepip --upgrade && \
    ln -sf /usr/local/bin/pip3.13 /usr/bin/pip3 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 100 && \
    # 为pip3配置阿里云镜像源 \
    pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    # 安装node.js 24.x 版本(LTS) \
    apt-get install -y --no-install-recommends nodejs && \
    # 将npm镜像源设置为阿里云镜像源 \
    npm config set registry https://registry.npmmirror.com && \
    # 安装 chromium 浏览器 \
    apt-get install -y --no-install-recommends chromium && \
    # 清理所有apt缓存, 减小镜像体积 \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 5.创建用户ubuntu并赋予sudo权限(24版本已经自带这个用户，所以不需要手动再创建一次)
RUN echo "ubuntu ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu && \
    chmod 0440 /etc/sudoers.d/ubuntu && \
    chmod -R 755 /etc/supervisor

# 6. 设置工作空间并调整权限（ubuntu用户可读写）
WORKDIR /sandbox
RUN chown -R ubuntu:ubuntu /sandbox

# 7.拷贝项目依赖文件并安装（切换到ubuntu用户，降低权限风险）
COPY --chown=ubuntu:ubuntu requirements.txt .
RUN apt-get remove -y python3-typing-extensions && \
    pip3 install --no-cache-dir -r requirements.txt

# 8.拷贝整个项目文件（保持权限一致）
COPY --chown=ubuntu:ubuntu . .

# 9.拷贝supervisord配置文件（路径统一，避免冲突）
COPY --chown=ubuntu:ubuntu supervisord.conf /etc/supervisor/conf.d/sandbox.conf

# 10.暴露端口: 8080(FastAPI) 9222(CDP) 5900(vnc) 5901(Websocket)
EXPOSE 8080 9222 5900 5901

# 11.额外的环境变量配置
ENV CHROME_ARGS="" \
    UVI_ARGS=""

# 12.切换到ubuntu用户（安全最佳实践，避免root运行）
USER ubuntu

# 13.使用supervisor管理所有进程(指定项目目录下的配置文件作为启动文件)
CMD ["supervisord", "-n", "-c", "/sandbox/supervisord.conf"]