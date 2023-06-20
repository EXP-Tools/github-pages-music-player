#!/bin/bash
# ----------------------------------------

# 复制挂载目录的配置文件到 nginx
MOUNT_DIR="/tmp/nginx/etc"
SITE_ETC_DIR="/etc/nginx/conf.d"
cp -r ${MOUNT_DIR}/* ${SITE_ETC_DIR}


# 以 HTTP/HTTPS 协议启动 nginx
HTTP_CONF="${SITE_ETC_DIR}/web_http.conf"
HTTPS_CONF="${SITE_ETC_DIR}/web_https.conf"
WEB_CONF="${SITE_ETC_DIR}/default.conf"
rm -f ${WEB_CONF}
if [[ ${PROTOCOL} = "https" ]]; then
    mv ${HTTPS_CONF} ${WEB_CONF}
    rm -f ${HTTP_CONF}
else
    mv ${HTTP_CONF} ${WEB_CONF}
    rm -f ${HTTPS_CONF}
fi
sed -i "s/YOUR_DOMAIN/${NGINX_DOMAIN}/g" ${WEB_CONF}



# 启动系统日志
service rsyslog start

# 启动 nginx
nginx


