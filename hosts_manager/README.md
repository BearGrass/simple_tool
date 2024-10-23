# host管理
## 依赖
```
pip install ping3
```

## 示例
> 需要注意的是，修改hosts文件通常需要管理员/root权限，所以在运行程序时可能需要使用sudo（Linux/macOS）或以管理员身份运行（Windows）。

```
python main.py add --ip 192.168.1.1 --domain example.com
python main.py remove --domain example.com
python main.py list
python main.py backup
python main.py restore --backup-file /path/to/backup/file
python main.py test --ip 192.168.1.1 --domain example.com
python main.py validate --ip 192.168.1.1 --domain example.com
```