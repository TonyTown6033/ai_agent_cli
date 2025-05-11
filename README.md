# OpenAI 多轮对话 CLI 工具

这是一个基于 OpenAI API 的多轮对话命令行工具，支持文本对话和图片处理功能。

## 功能特性

- **多轮对话**：支持上下文记忆，保留最近 5 轮对话历史。
- **图片处理**：通过 Base64 编码上传图片，并获取 AI 的分析结果。
- **自定义模型**：支持选择不同的语言模型（如 `gpt-4o-mini`）。
- **随机性控制**：通过 `temperature` 参数调整生成结果的随机性。

---

## 安装依赖

在运行项目之前，请确保安装以下依赖项：

1. 创建 `requirements.txt` 文件（已生成）：
   ```plaintext
   click==8.1.3
   openai==0.27.8
   Pillow==9.5.0
   ```

2. 使用以下命令安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

---

## 使用方法

### 1. 设置 API 密钥

在运行程序之前，需要设置 OpenAI 的 API 密钥。可以通过环境变量 `OPENAI_API_KEY` 设置：

#### Windows 命令行
```bash
set OPENAI_API_KEY=your_api_key_here
```

#### PowerShell
```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

---

### 2. 启动 CLI 工具

运行以下命令查看帮助：
```bash
python ag.py --help
```

---

### 3. 功能命令

#### **文本对话**
直接输入问题并获取回答：
```bash
python ag.py chat --question "你好，今天的天气怎么样？"
```

进入交互式对话模式：
```bash
python ag.py chat
```
输入 `q` 或 `quit` 退出会话模式。

#### **图片处理**
上传图片并获取 AI 的分析结果：
```bash
python ag.py process-image --image path/to/your/image.jpg
```

---

## 参数说明

| 参数名         | 默认值         | 说明                                   |
|----------------|----------------|----------------------------------------|
| `--model`      | `gpt-4o-mini`  | 选择语言模型（如 `deepseek` 或其他模型）|
| `--temperature`| `0.7`          | 生成结果的随机性（范围：0-2）          |

---

## 注意事项

1. **API 密钥安全性**：请勿将 API 密钥直接写入代码中，使用环境变量加载。
2. **图片格式**：确保上传的图片为支持的格式（如 JPEG）。
3. **错误处理**：如果出现错误，请检查 API 密钥是否正确，或查看终端输出的错误信息。