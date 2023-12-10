# 开幕式音乐标准化 | AudioNormalizer

## 使用方法

运行后会打开一个文件夹选择框，选择音频文件夹，该文件夹下产生一个`music`文件夹，并将处理后的音频产生在`music`文件夹下。

## 实现功能

1. 将文件夹内所有音频、视频文件统一格式`.mp3`

2. 统一音频响度

## 实现逻辑

### 预处理

定义支持的后缀名列表`support_suffix`，该列表应该包含所有所使用的音视频库中所有支持的格式，且可能包含音频的文件的文件名后缀。

### 主逻辑

打开一个文件夹选择框，选择音频文件夹，选择一个文件夹`folder`

新建子文件夹`music`

遍历`folder`下的所有文件后缀在`support_suffix`列表的文件：

- 提取音频 <small>（若失败，在命令行中输出）</small>

- 计算音频平均响度

- 通过计算将音频增益或负增益，将音频平均响度调整为设定值

- 将处理后的音频保存到`music`文件夹下，文件名不变，格式后缀为`.mp3`

调用资源管理器打开`music`文件夹

## 构建

构建之前请选择一个ffmpeg版本放在相同的文件夹下，作为默认ffmpeg

```shell
nuitka --standalone --mingw64 --show-memory --show-progress --include-data-files=ffmpeg.exe=ffmpeg.exe --plugin-enable=tk-inter --output-dir=o AudioNormalizer.py
```
