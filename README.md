# img_upload_for_Markdown
自动上传Markdown中的图片到SMMS图床或者腾讯云cos

### 安装：

```shell
1.安装Python3 和 pip
2.pip install requests
3.pip install -U cos-python-sdk-v5
```

### 使用方法：

下载`uploadparser.py`、`imgupload`、`UploadImg.ini`放到Markdown文档所在目录，如果使用腾讯云cos的话先填好`secret_id`、`secret_key`、`region`、`Bucket`。

本来是专为Hexo博客用的，设置的默认的扫描目录为`\source\_posts\`，请自行修改`imgupload`文件中的路径。

![image-20191230103144027](https://i.loli.net/2019/12/30/seRvFDcJW3yGnLT.png)

以smms图床为例，在写完文章`hexo g -d`以前，输入`python imgupload smms article.md`，等待上传完成。

```python
python imgupload tx/smms/clearline <filename.md>
```

![image-20191230104452385](https://i.loli.net/2019/12/30/qYfK3v7gRCuzh9S.png)

### 参数解释

`tx`： 腾讯云cos

`smms`：smms图床

`clearline`： 清除markdown文件中的空行

`local` ：使用相对引用图片，目前不可用。
