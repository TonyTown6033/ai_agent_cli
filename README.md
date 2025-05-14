# AGenius Chat 🚀（智能对话助理）

AGenius Chat 是一款极客向的 OpenAI 多轮对话命令行工具，支持文本对话、图片分析、智能文件插入等多种 AI 交互方式，让你的终端会说话！

## 功能特性

- **多轮对话记忆**：自动保留最近 5 轮（10 条消息）上下文，连续提问无压力。
- **图片处理**：通过 Base64 编码上传图片，AI 自动分析图片内容。
- **智能文件插入**：在对话中通过 `@` 选择文件，支持图片和文本/代码自动插入与识别。
- **自定义模型与温度**：支持选择不同的语言模型（如 `gpt-4o-mini`、`deepseek`），可调节 `temperature` 控制生成内容的随机性。
- **管道输入支持**：支持通过管道传递输入数据，适合脚本化和自动化场景。
- **交互式文件选择器**：命令行弹窗选择文件，支持目录浏览、数字选择、`../` 返回上级目录。

---

## 安装依赖

1. 确保已安装 Python 3.7 及以上版本。
2. 安装依赖：
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

### 2. 查看帮助

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

#### **管道输入**
支持通过管道传递输入数据，例如：
```bash
echo "你好，今天的天气怎么样？" | python ag.py chat
```

#### **图片处理**
上传图片并获取 AI 的分析结果：
```bash
python ag.py process-image --image path/to/your/image.jpg
```

#### **智能文件插入对话**
在问题中使用 `@`，可弹出文件选择器，插入图片或文本/代码文件，AI 自动识别内容：
```bash
python ag.py smart-chat --question "请帮我分析这段代码 @"
```
- 插入图片时，AI 会自动描述图片内容。
- 插入文本/代码时，AI 会读取文件前 1000 字符并参与对话。

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
3. **文件插入**：`smart-chat` 支持图片和文本/代码文件，图片将自动转为 Base64，文本/代码自动截断。
4. **错误处理**：如遇错误，请检查 API 密钥、网络连接或终端输出的错误信息。

---

## 依赖列表

- click
- openai
- Pillow
- 其他依赖见 `requirements.txt`