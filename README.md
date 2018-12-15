# img_upload_for_Markdown
自动上传Markdown中的图片到SMMS图床或者腾讯云cos

### 相关依赖：

```
Python3
requests
cos-python-sdk-v5    https://github.com/tencentyun/cos-python-sdk-v5
```

### 使用方法：

```
python imgupload tx/smms/clearline <filename.md>
```

本来是专为Hexo博客用的，所以默认的`imgupload`中设置的是寻找路径`\source\_posts\`的文件。

使用腾讯云对象存储需要在`UploadImg.ini`中设置`secret_id`、`secret_key`、`region`、`Bucket`

上传腾讯云对象存储默认建立一个以文件名命名的文件夹存放图片。

### Hexo博客使用方法

下载`uploadparser.py`、`imgupload`、`UploadImg.ini`放到博客根目录。如果使用腾讯云cos的话先填好`secret_id`、`secret_key`、`region`、`Bucket`

以smms图床为例，在写完文章`hexo g -d`以前，输入`python imgupload smms article.md`，等待上传完成。

### 参数解释

`tx`： 腾讯云cos

`smms`：smms图床

`clearline`： 清除markdown文件中的空行

`local` ：使用相对引用图片，目前不可用。

### 使用示例

!(示例)[https://i.loli.net/2018/12/15/5c14e4dc68061.gif]


  