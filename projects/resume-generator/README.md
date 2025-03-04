# **自动化简历生成系统**

## **项目简介**
本项目是一个基于 **DeepSeek API** 和 **LaTeX** 的自动化简历生成系统。用户可以通过上传简历母版（Markdown格式）、选择职位需求（Markdown格式）和本地LaTeX模板，调用DeepSeek API生成优化后的简历内容，并自动填充到LaTeX模板中，最终生成PDF格式的简历文件。

### **核心功能**
1. **简历母版上传**：支持Markdown格式的简历母版。
2. **职位需求选择**：提供预定义的职位需求文件，支持自定义。
3. **LaTeX模板支持**：使用本地LaTeX模板生成美观的PDF简历。
4. **DeepSeek API集成**：调用DeepSeek API优化简历内容。
5. **PDF生成与下载**：自动编译LaTeX文件并生成PDF，提供下载链接。

---

## **文件结构**
```
resume-generator/                  # 项目根目录
├── data/                          # 数据文件
│   ├── base_resume.md             # 简历母版
│   ├── job_network_engineer.md    # 网络工程师职位需求
│   ├── job_data_scientist.md      # 大数据工程师职位需求
├── templates/                     # LaTeX模板
│   ├── resume_template.tex        # LaTeX简历模板
├── output/                        # 生成的文件
│   ├── resume.pdf                 # 最终生成的PDF
├── app.py                         # 主程序（Streamlit界面）
├── requirements.txt               # 依赖文件
├── README.md                      # 项目说明文档
```

---

## **快速开始**

### **1. 安装依赖**
确保已安装 Python 3.7 或更高版本，然后运行以下命令安装依赖：
```bash
pip install -r requirements.txt
```
安装 LaTeX 环境
#### **Windows 系统**
1. 下载并安装 [MiKTeX](https://miktex.org/download) 或 [TeX Live](https://www.tug.org/texlive/)。
   - MiKTeX 是 Windows 上常用的 LaTeX 发行版，安装简单。
   - TeX Live 是跨平台的 LaTeX 发行版，功能更全面。
2. 安装完成后，确保将 LaTeX 的安装路径添加到系统的环境变量中。
   - 默认情况下，MiKTeX 的安装路径为 `C:\Program Files\MiKTeX 2.9\miktex\bin\x64\`。
   - 添加环境变量的方法：
     1. 右键点击“此电脑” -> “属性” -> “高级系统设置” -> “环境变量”。
     2. 在“系统变量”中找到 `Path`，点击“编辑”。
     3. 添加 MiKTeX 或 TeX Live 的 `bin` 目录路径（如 `C:\Program Files\MiKTeX 2.9\miktex\bin\x64\`）。
     4. 点击“确定”保存。

#### **macOS 系统**
1. 安装 [MacTeX](https://www.tug.org/mactex/)，这是 macOS 上常用的 LaTeX 发行版。
2. 安装完成后，LaTeX 命令会自动添加到系统路径中。

#### **Linux 系统**
1. 安装 TeX Live：
   ```bash
   sudo apt-get install texlive-full
   ```
2. 安装完成后，LaTeX 命令会自动添加到系统路径中。

### **2. 配置DeepSeek API密钥**
1. 注册并登录 [DeepSeek](https://www.deepseek.com/) 获取API密钥。
2. 在运行程序时，将API密钥输入到界面中。

### **3. 运行项目**
在终端中运行以下命令启动Streamlit界面：
```bash
streamlit run app.py
```
打开浏览器，访问 `http://localhost:8501`。

---

## **使用指南**

### **1. 上传简历母版**
- 点击“上传简历母版”按钮，选择Markdown格式的简历文件（参考 `data/base_resume.md`）。

### **2. 选择职位需求**
- 在下拉菜单中选择预定义的职位需求（如“网络工程师”），或上传自定义的职位需求文件。

### **3. 输入DeepSeek API密钥**
- 在输入框中填写您的DeepSeek API密钥。

### **4. 生成简历**
- 点击“生成简历”按钮，系统将自动调用DeepSeek API优化简历内容，并生成PDF文件。
- 生成完成后，点击“下载简历”按钮即可下载PDF文件。

---

## **配置文件说明**

### **1. 简历母版 (`data/base_resume.md`)**
- 使用Markdown格式编写简历母版，包含基本信息、工作经验和技能等内容。

### **2. 职位需求文件 (`data/job_*.md`)**
- 使用Markdown格式编写职位需求，包含职位描述、筛选标准、硬技能、软技能和关键词等内容。

### **3. LaTeX模板 (`templates/resume_template.tex`)**
- 使用Jinja2语法编写LaTeX模板，支持动态填充内容。

---

## **自定义与扩展**

### **1. 添加新的职位需求**
1. 在 `data/` 目录下创建一个新的Markdown文件（如 `job_custom.md`）。
2. 按照以下格式编写职位需求：
   ```markdown
   **自定义职位**  

   *职位描述：* 描述职位的主要职责。  

   *筛选标准：* 列出学历、专业等要求。  

   *硬技能：*  
   - 技能1  
   - 技能2  

   *软技能：*  
   - 技能1  
   - 技能2  

   *简历关键词：*  
   - 关键词1  
   - 关键词2  
   ```
3. 在 `app.py` 中更新 `job_files` 字典，添加新的职位选项。

### **2. 修改LaTeX模板**
1. 打开 `templates/resume_template.tex` 文件。
2. 根据需要修改模板内容，确保使用Jinja2语法标记动态字段（如 `{{ name }}`）。

---

## **注意事项**
1. **DeepSeek API调用限制**：确保API密钥有效，并注意API调用的频率限制。
2. **LaTeX环境**：确保系统已安装LaTeX（如TeX Live或MiKTeX），并支持 `xelatex` 命令。
3. **文件路径**：确保所有文件路径正确，尤其是上传文件和模板文件。
4. **错误处理**：如果生成失败，检查终端日志或Streamlit界面提示。

---

## **常见问题**

### **1. LaTeX编译失败**
- 确保系统已安装LaTeX环境。
- 检查 `output/resume.tex` 文件内容是否正确。

### **2. DeepSeek API调用失败**
- 检查API密钥是否正确。
- 确保网络连接正常。

### **3. 界面无法打开**
- 确保Streamlit已正确安装。
- 检查端口 `8501` 是否被占用。

---

## **技术支持**
如有任何问题或建议，请联系：
- 邮箱：elvislongzheng@gmail.com
---

## **许可证**
本项目基于 MIT 许可证开源。详情请参阅 [LICENSE](LICENSE) 文件。
