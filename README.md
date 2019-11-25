## 原力流媒体后台接口


### [官方文档](https://www.docin.com/p-508238174.html)

```
# 安装
python setup.py install

# 使用
import fypy
forcetv = fypy.ForceTv(server='http://127.0.0.1:6000')
print forcetv.query_server_list()
```

#### 异常说明:
code | node
---|---
 4| 数据库操作错误
 9| 接口授权错误
 10| 频道不存在
 11| 方法不存在
 12| 其他错误
 
#### 异常捕捉
```
import fypy
forcetv = fypy.ForceTv(server='http://127.0.0.1:6000')
try:
    print forcetv.query_server_list() 
except fypy.ForceTvException as e:
    print e.code # 错误代码
    print e.msg # 错误信息
```
 