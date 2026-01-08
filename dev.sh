#!/usr/bin/env bash


exec uvicorn app.main:app --host 0.0.0.0 --port 6001 --timeout-graceful-shutdown 0

# 解释
# 启动开发环境的命令
# 使用 . 替代路径中的 /，避免跨平台问题
# exec 表示用后面的命令替换当前 Shell 进程（执行完后直接退出，不残留多余进程），确保信号正确传递给 uvicorn 进程.
#
# 具体参数说明：
# uvicorn app.main:app
# --host 0.0.0.0 监听所有网络接口
# --port 6001 指定端口为 6001
# --timeout-graceful-shutdown 0 优化关闭速度，避免等待默认的 30 秒超时

# 注意
# 因为项目里面有子进程，所以不能加上 --reload 参数，否则会有问题
