# Powershell
#-----------------------------------------------------------------
# 生成任意字符串的 SHA256
# 用于设置文章密码
#-----------------------------------------------------------------
# 命令执行示例：
#   bin/to_sha256.ps1 "123456"
#-----------------------------------------------------------------

Param (
    [Parameter(Mandatory=$true)]
    [string]
    $anyString
)

$hasher = [System.Security.Cryptography.HashAlgorithm]::Create('sha256')
$hash = $hasher.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($anyString))

$hashString = [System.BitConverter]::ToString($hash)
$hashString.Replace('-', '').ToLower()

