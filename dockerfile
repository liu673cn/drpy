# 基于的基础镜像-在dockerhub找
# FROM silverlogic/python3.8
FROM python:3.8-slim-buster
# 添加描述信息
MAINTAINER python3.8+drpy+supervisord by "hjdhnx"
# 设置app文件夹是工作目录
WORKDIR /root/sd/pywork/dr_py
# 复制文件及目录过去
COPY . /root/sd/pywork/dr_py
# 配置一下国内的agt源
# 移动旧的源
RUN cp /etc/apt/sources.list /etc/apt/sources.list.bac
# 更换国内源 bullseye debian11 https://mirrors.bfsu.edu.cn/help/debian/
# RUN cat <<EOF > /etc/apt/sources.list
# # 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
# deb https://mirrors.bfsu.edu.cn/debian/ bullseye main contrib non-free
# # deb-src https://mirrors.bfsu.edu.cn/debian/ bullseye main contrib non-free
# deb https://mirrors.bfsu.edu.cn/debian/ bullseye-updates main contrib non-free
# # deb-src https://mirrors.bfsu.edu.cn/debian/ bullseye-updates main contrib non-free
#
# deb https://mirrors.bfsu.edu.cn/debian/ bullseye-backports main contrib non-free
# # deb-src https://mirrors.bfsu.edu.cn/debian/ bullseye-backports main contrib non-free
#
# deb https://mirrors.bfsu.edu.cn/debian-security bullseye-security main contrib non-free
# # deb-src https://mirrors.bfsu.edu.cn/debian-security bullseye-security main contrib non-free
# EOF
RUN mkdir -p /etc/autostart
ADD sources.list /etc/apt/
ADD app.sh /etc/autostart/

# RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
# armv7安装gcc
# RUN apt-get install gcc-arm-linux-gnueabihf g++-arm-linux-gnueabihf -y
RUN chmod +x /etc/autostart/app.sh && apt-get clean && apt-get update && apt-get install -y vim
# 执行指令，换源并安装依赖 设置默认pip源
RUN pip install -i https://mirrors.cloud.tencent.com/pypi/simple --upgrade pip \
    && pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple

# 执行指令，安装依赖
RUN pip install -r requirements.txt
# 切换容器时区
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
# 设置语言支持中文打印
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
EXPOSE 5705 9001
# docker build -f dockerfile -t hjdhnx/drpy:mini .  构建命令,非此文件内命令
# docker build -f dockerfile -t hjdhnx/drpy_mini .  构建命令,非此文件内命令
# docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -f dockerfile -t hjdhnx/drpy:mini_arm64 .
# docker buildx build --platform linux/arm/v7 -f dockerfile -t hjdhnx/drpy_mini:armv7 .
# 启动命令,非此文件内命令
# docker run -it -p 5705:5705 -p 9001:9001 -v /home/pywork/dr_py:/root/sd/pywork/dr_py --restart=always --name drpy -d hjdhnx/drpy:mini
# docker run -it -p 5705:5705 -p 9001:9001 -v /home/pywork/dr_py:/root/sd/pywork/dr_py --restart=always --name drpy -d hjdhnx/drpy_mini
# ENV LC_ALL=zh_CN.utf8
# ENV LANG=zh_CN.utf8
# ENV LANGUAGE=zh_CN.utf8
# RUN localedef -c -f UTF-8 -i zh_CN zh_CN.utf8
# 执行命令
# CMD [ "python", "/root/sd/pywork/dr_py/app.py" ]
# supervisord -c /root/sd/pywork/dr_py/super/flask.conf
# CMD [ "supervisord","-c", "/root/sd/pywork/dr_py/super/flask.conf" ]
# ENTRYPOINT supervisord -c /root/sd/pywork/dr_py/super/flask.conf
# ENTRYPOINT -c /root/sd/pywork/dr_py/super/flask.conf
# CMD /bin/bash
# 启动容器时，执行脚本
ENTRYPOINT ["/etc/autostart/app.sh","flask"]
# CMD supervisord -c /root/sd/pywork/dr_py/super/flask.conf && /bin/bash

