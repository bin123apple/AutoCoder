# 使用官方 Java 11 JDK 镜像作为基础镜像
FROM openjdk:11-jdk

# 设置非交互模式，防止 apt-get 等命令在安装过程中等待用户输入
ENV DEBIAN_FRONTEND=noninteractive

# 安装必要的工具，比如构建和调试工具
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    maven \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

CMD ["/app/compile_run.sh"]
