# Harbor历史镜像删除
## _步骤_
### 配置文件修改 
#### 文件：lib/setting.py
```
# LOG自定义参数
LOG_LEVEL = "INFO"
LOG_DIR = "/tmp"
LOG_FILE = "install.log"
# HARBOR
HARBOR_URL = '127.0.0.1:9090'
HARBOR_USER = 'admin'
HARBOR_PASSWORD = 'Harbor12345d'

```