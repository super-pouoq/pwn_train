#!/usr/bin/env bash
# 用法： ./pack_pwn.sh [目标目录]   # 不填则默认当前目录

set -euo pipefail
shopt -s nullglob

dir="${1:-.}"
cd "$dir"

for f in pwn[0-9]*; do
  # 只处理普通文件，跳过目录/链接
  [[ -f "$f" ]] || continue

  base="$f"                    # 文件名（不含路径）
  stem="${base%.*}"            # 去掉扩展名后的“基名”
  target_dir="$stem"

  # 如果没有扩展名（base == stem），需要临时改名避免同名阻塞
  if [[ "$base" == "$stem" ]]; then
    tmp="${base}.$RANDOM.$RANDOM.tmp"
    while [[ -e "$tmp" ]]; do
      tmp="${base}.$RANDOM.$RANDOM.tmp"
    done
    mv -- "$base" "$tmp"
    mkdir -p -- "$target_dir"
    mv -- "$tmp" "$target_dir/$base"   # 放回并恢复原名
  else
    mkdir -p -- "$target_dir"
    if [[ -e "$target_dir/$base" ]]; then
      echo "跳过：$target_dir/$base 已存在" >&2
    else
      mv -- "$base" "$target_dir/"
    fi
  fi
done

echo "整理完成：已将 pwn* 文件归档到同名文件夹中。"
