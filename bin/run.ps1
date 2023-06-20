# Powershell
#------------------------------------------------
# 运行 docker 服务（由于需要实时解析局域网 IP，需要管理员权限执行）
# sudo bin/run.ps1
#           [-p ${PROTOCOL}]            # 页面使用 http/https 协议（默认 http）
#           [-d ${DOMAIN}]              # 服务域名
#           [-i ${IP}]                  # 服务器 IP（默认通过网卡取内网 IP，如果需要公网访问，需设置为公网 IP）
#------------------------------------------------

param(
    [string]$Protocol = "http",
    [string]$Domain = "web.music.com",
    [string]$IP = ""
)


if (-not $IP) {
  $interfaces = @("Wi-Fi", "Ethernet", "以太网")
  foreach ($int in $interfaces) {
    if ($output = (ipconfig $int 2>$null | Select-String -Pattern 'IPv4 Address')) {
      $IP = $output -replace '.*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*', '$1'
      break
    }
  }

  if (-not $IP) {
    $IP = "127.0.0.1"
  }
}

function Set-Dns {
  param(
    [string]$Domain,
    [string]$InterIP
  )

  $dns_file = "C:\Windows\System32\drivers\etc\hosts"
  if (Select-String -Path $dns_file -Pattern $Domain) {
    $from_reg = "^[0-9.]* ${Domain}$"
    $to_str = "${InterIP} ${Domain}"
    (Get-Content -Path $dns_file) -replace $from_reg, $to_str | Set-Content -Path $dns_file
    if (-not $?) {
      Write-Host "In order to update the inter IP in local hosts, please use 'Run as administrator' ..."
    }
  } else {
    Add-Content -Path $dns_file -Value "$InterIP $Domain"
  }
}

function Set-Env {
  param(
    [string]$Domain,
    [string]$InterIP,
    [string]$Protocol
  )

  $env_file = ".env"
  "DOMAIN=$Domain" | Out-File -Encoding utf8 -FilePath $env_file
  "INTER_IP=$InterIP" | Out-File -Encoding utf8 -Append -FilePath $env_file
  "PROTOCOL=$Protocol" | Out-File -Encoding utf8 -Append -FilePath $env_file
  Write-Host "$InterIP $Domain"
}

Set-Dns -Domain $Domain -InterIP $IP
Set-Env -Domain $Domain -InterIP $IP -Protocol $Protocol



docker-compose up -d

docker ps
Write-Host "Docker is running: ${Protocol}://${Domain}"
