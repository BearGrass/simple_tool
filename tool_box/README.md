# simple tool box
## deploy dev env

```bash
# 修改成腾讯云镜像源
npm config set registry http://mirrors.cloud.tencent.com/npm/

# 验证命令
npm config get registry

# 安装其他项目依赖
npm install

# 安装 flask 依赖
pip install flask

```

## start
```bash
npm run server

# 用另外一个终端
npm start
```