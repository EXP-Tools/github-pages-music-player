FROM ubuntu:18.04
ENV TZ=Asia/Shanghai
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN apt-get clean && \
    apt-get update -y


# 安装系统 GBK 和 UTF-8 中文语言包
RUN apt-get install -y language-pack-zh-hans language-pack-zh-hans-base \
                    language-pack-gnome-zh-hans language-pack-gnome-zh-hans-base
RUN apt-get install -y locales && \
    echo 'zh_CN.GBK GBK' >> /etc/locale.gen && \
    echo 'zh_CN.UTF-8 UTF-8' >> /etc/locale.gen && \
    echo "LANG=zh_CN.UTF-8" >> /etc/environment && \
    locale-gen


# 安装环境必要工具
RUN apt-get install -y wget openjdk-8-jdk python3 python3-pip tzdata
RUN ln -s /usr/bin/python3 /usr/bin/python && \
    python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> /root/.bashrc && \
    echo "export JRE_HOME=${JAVA_HOME}/jre" >> /root/.bashrc && \
    echo "export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib" >> /root/.bashrc && \
    echo "export PATH=${JAVA_HOME}/bin:${PATH}" >> /root/.bashrc


# 使用 nginx 最新的源
RUN echo "deb https://nginx.org/packages/ubuntu/ bionic nginx" >> /etc/apt/sources.list && \
    echo "deb-src https://nginx.org/packages/ubuntu/ bionic nginx" >> /etc/apt/sources.list && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys ABF5BD827BD9BF62

    
# 安装系统必要工具
RUN apt-get update -y && \
    apt-get install -y curl rsyslog nginx apache2-utils openssh-server rsyslog



WORKDIR /
ADD ./nginx/bin /bin
RUN chmod 100 /bin/.docker-entrypoint.sh && \
    chmod 100 /bin/.wrapper.sh
ENTRYPOINT [ "/bin/.wrapper.sh" ]
