# 使用最新的Ubuntu镜像作为基础镜像
FROM ubuntu:latest

# 设置非交互模式，防止apt-get等命令在安装过程中等待用户输入
ENV DEBIAN_FRONTEND=noninteractive

# 更新软件包列表，并安装必要的软件包
RUN apt-get update && \
    apt-get install -y cmake git build-essential libomp-dev

# 克隆Google Test的源码，编译并安装
RUN git clone https://github.com/google/googletest.git /googletest && \
    cd /googletest && \
    cmake . && \
    make && \
    make install

# 设置工作目录为/project
WORKDIR /app

# 复制当前目录下的所有文件到容器的/project目录中
COPY . /app/

# 编译C++程序，这里假设主要的C++文件名为script.cpp，并且生成的可执行文件名为test
# 注意：-L/usr/local/lib选项指定了库文件的搜索路径，这在某些情况下可能是必要的
# RUN g++ -fopenmp script.cpp -L/usr/local/lib -lgtest -lgtest_main -pthread -o test

# 容器启动时默认执行的命令
# CMD ["./test"]
CMD ["/app/compile_run.sh"]

