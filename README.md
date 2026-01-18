# 项目说明

## uv 导出依赖为 requirement.txt

```shell
uv export --format requirements.txt --no-dev --no-hashes --output-file requirements.txt
```

## 构建镜像文件

```shell
docker build -t sandbox-dev .
```

- 如果本地构建超时，可以配置代理

```shell
# 声明代理变量(开启命令行代理，以电脑上的实际代理端口为准)
export http_proxy=http://127.0.0.1:7897
export https_proxy=http://127.0.0.1:7897
```

### 启动容器

```shell
docker run -d -p 6001:8080 -p 5900:5900 -p 5901:5901 -p 9222:9222 --name sandbox-dev sandbox-dev
```

- 端口参数介绍
- 6001:8080: web访问端口
- 5900: vnc 默认端口
- 5901: 将VNC转换为Websocket
- 9222: chrome devtools
