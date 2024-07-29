# 自动构建 更纱黑体 SC Nerd 字体

## 说明

因为我家里电脑是 Ubuntu 系统，所以该自动脚本目前只支持 Ubuntu 系统，其它系统请自行修改。

## 使用方法：

```sh
# 删除 build 目录
python3 build.py clean

# 执行依赖安装
python3 build.py deps

# 自动下载构建
python3 build.py build
```

## 感谢

[更纱黑体](https://github.com/be5invis/Sarasa-Gothic)

[FontPatcher](https://github.com/ryanoasis/nerd-fonts?tab=readme-ov-file#font-patcher)

[py7zr](https://github.com/miurahr/py7zr)
