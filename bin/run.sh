#!/bin/bash
#------------------------------------------------
# 运行 docker 服务（由于需要实时解析局域网 IP，需要 sudo 权限执行）
# sudo bin/run.sh
#           [-p ${PROTOCOL}]            # 页面使用 http/https 协议（默认 http）
#           [-d ${DOMAIN}]              # 服务域名
#           [-i ${IP}]                  # 服务器 IP（默认通过网卡取内网 IP，如果需要公网访问，需设置为公网 IP）
#------------------------------------------------

PROTOCOL="http"
DOMAIN="web.music.com"
INTER_IP=""


set -- `getopt p:d:i: "$@"`
while [ -n "$1" ]
do
  case "$1" in
    -p) PROTOCOL="$2"
        shift ;;
    -d) DOMAIN="$2"
        shift ;;
    -i) INTER_IP="$2"
        shift ;;
  esac
  shift
done

if [[ -z "${INTER_IP}" ]]; then
  interface=("en0" "eth0")
  for int in "${interface[@]}"; do
    if INTER_IP=$(ifconfig "$int" 2>/dev/null | awk '/inet / {print $2}'); then
      break
    fi
  done

  if [[ -z "${INTER_IP}" ]]; then
    INTER_IP="127.0.0.1"
  fi
fi


# 修改本地 hosts 文件，在本地解析域名
function set_dns {
  DNS_FILE="/etc/hosts"
  domain=$1
  inter_ip=$2
  
  if [ `grep -c "${domain}" ${DNS_FILE}` -ne '0' ]; then
      FROM_REG="^[0-9.]* ${domain}$"
      TO_STR="${inter_ip} ${domain}"
      sed -i '' -E "s/${FROM_REG}/${TO_STR}/" ${DNS_FILE}
      if [ ! $? = 0 ]; then
        echo "In order to update the inter IP in local hosts, please use 'sudo' ..."
      fi
  else
      echo "${inter_ip} ${domain}" >> ${DNS_FILE}
  fi
}


# 写入 docker-compose 的 .env 文件
function set_env {
  ENV_FILE=".env"
  domain=$1
  inter_ip=$2
  protocol=$3

  echo "DOMAIN=${domain}" > ${ENV_FILE}
  echo "INTER_IP=${inter_ip}" >> ${ENV_FILE}
  echo "PROTOCOL=${protocol}" >> ${ENV_FILE}
}


set_dns $DOMAIN $INTER_IP
set_env $DOMAIN $INTER_IP $PROTOCOL

docker-compose up -d

docker ps
echo "Docker is running: ${PROTOCOL}://${DOMAIN}"
