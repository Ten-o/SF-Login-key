# TEN_JD_SCAN

## 项目简介

TEN_JD_SCAN 是一个用于接码和打码的工具，支持自动化扫描验证码。

- **接码平台**：[椰子接码](http://h5.yezi66.net:90/)
- **打码平台**：[TT OCR](https://www.ttocr.com/)

> **注意**：目前邀请功能不生效，可能是接码平台的号码已被邀请完。

## 目录结构

```bash
TEN_JD_SCAN/                # 根目录
├── SF_task.py          # 打码平台版本（推荐，0.01 元/次）
├── SF_task_model.py     # 自己打码版本（能用，但效率较低）
├── model.onnx          # 预训练的 ONNX 模型
└── README.md           # 项目说明文档
```

## 使用说明

### 1. 运行打码平台版本（推荐）
```bash
python SF_task.py
```
该版本使用 [TT OCR](https://www.ttocr.com/) 进行验证码识别，推荐使用。

### 2. 运行本地打码版本（效率较低）
```bash
python SF_task_model.py
```
该版本使用 `model.onnx` 进行验证码识别，不依赖第三方打码平台，但识别效率相对较低。


## 注意事项
1. **邀请功能暂不可用**，请自行获取可用的接码号码。
2. **建议使用 `SF_task.py`**，因其调用外部打码平台，识别率较高。
3. `model.onnx` 适用于 `SF_task_model.py`，可用于本地验证码识别。

## 反馈与支持
如有问题或建议，请提交 Issue 或联系维护者。



