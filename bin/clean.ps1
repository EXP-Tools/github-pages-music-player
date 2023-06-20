# Powershell
#------------------------------------------------
# 清理镜像、日志
# bin/clean.ps1
#------------------------------------------------

Write-Host "clean logs ..."
Remove-Item -Recurse -Force logs

Write-Host "clean images ..."
docker images | Select-String "web-music" | ForEach-Object { docker rmi -f $_.ToString().Split(" ")[2] }
docker images | Select-String "none" | ForEach-Object { docker rmi -f $_.ToString().Split(" ")[2] }

Write-Host "finish ."
