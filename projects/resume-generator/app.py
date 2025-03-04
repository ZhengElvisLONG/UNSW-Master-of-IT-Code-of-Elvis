import os
import re
import time
import logging
import subprocess
import requests
import streamlit as st
from jinja2 import Template
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError

# ==============================
# 配置日志记录
# ==============================
logging.basicConfig(
    filename='resume_generator.log',
    level=logging.DEBUG,  # 调试时记录DEBUG信息
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# DeepSeek API 配置，推荐使用 DeepSeek 官方示例的地址
BASE_URL = "https://api.deepseek.com"  # 或者 "https://api.deepseek.com/v1"

# ==============================
# 工具函数
# ==============================
def parse_markdown(md_content: str) -> dict:
    """
    解析Markdown格式的职位描述，支持更灵活的格式：
    根据星号开头的标题提取内容，列表项以“- ”分割。
    """
    data = {}
    mapping = {
        "职位描述": "job_desc",
        "硬技能": "hard_skills",
        "简历关键词": "keywords"
    }
    for key, field in mapping.items():
        pattern = rf"\*{key}：\*\s*(.*?)(?=\n\*|$)"
        match = re.search(pattern, md_content, re.DOTALL)
        if match:
            content = match.group(1).strip()
            if field == "job_desc":
                data[field] = content
                logging.debug(f"解析 {key} 成功：{data[field][:50]}...")
            else:
                items = re.findall(r"-\s*(.*)", content)
                data[field] = [item.strip() for item in items if item.strip()]
                logging.debug(f"解析 {key} 成功：{data[field]}")
        else:
            logging.warning(f"未能解析到 {key} 部分，请检查Markdown格式。")
            data[field] = "" if field == "job_desc" else []
    return data

def build_prompt(base_resume: str, job_data: dict) -> str:
    """
    根据简历原文和职位描述数据组装正式Prompt，增加对空列表的容错处理
    """
    job_desc = job_data.get("job_desc", "无")
    hard_skills = job_data.get("hard_skills", [])
    keywords = job_data.get("keywords", [])
    hard_skills_str = ', '.join(hard_skills) if hard_skills else "无"
    keywords_str = ', '.join(keywords) if keywords else "无"

    prompt = f"""
你是一个资深且擅长运用AI技术的HR，具有丰富的候选人筛选经验。你已经回顾过许多候选人的简历，并总结了他们的共同优势。根据不同工种的岗位描述（JD）和筛选标准，按照麦肯锡原则（从重要到不重要）为应届硕士毕业生定制简历。这个简历需要突出软技能和硬技能，筛选过程中，必须能够体现以下关键能力和关键词。简历应当控制在一页之内。
请根据以下信息优化简历：
- 目标岗位描述：{job_desc}
- 硬技能要求：{hard_skills_str}
- 关键词：{keywords_str}

原始简历内容：
{base_resume}

要求：
1. 突出硬技能和相关经验
2. 使用关键词优化描述
3. 保持简洁和专业
"""
    logging.debug(f"生成Prompt成功，长度：{len(prompt)}字符")
    return prompt

def fill_latex_template(template_path: str, data: dict) -> str:
    """
    填充LaTeX模板，若模板读取或渲染出错，则记录详细日志
    """
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
    except Exception as e:
        logging.exception(f"读取模板文件 {template_path} 失败")
        raise
    try:
        template = Template(template_content)
        rendered = template.render(data)
        logging.debug("LaTeX模板渲染成功。")
        return rendered
    except Exception as e:
        logging.exception("LaTeX模板渲染失败")
        raise

# ==============================
# DeepSeek API 调用函数
# ==============================
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def call_deepseek_api(prompt: str, api_key: str, stream_mode: bool = True) -> str:
    """
    调用DeepSeek API的函数，增加详细日志记录和异常堆栈信息，方便调试各类异常。
    stream_mode 为 True 时启用流式输出，False 则直接获取完整响应（适用于测试连接）。
    """
    if not api_key:
        error_msg = "API密钥不能为空，请到DeepSeek控制台获取有效密钥"
        logging.error(error_msg)
        raise ValueError(error_msg)
    
    # 根据 DeepSeek 的 OpenAI 兼容格式进行校验
    if api_key.startswith("sk-"):
        if len(api_key) != 35:
            error_msg = "API密钥格式错误，应为35位字符串（以sk-开头）"
            logging.error(error_msg)
            raise ValueError(error_msg)
    else:
        if len(api_key) != 64:
            error_msg = "API密钥格式错误，应为64位字符串"
            logging.error(error_msg)
            raise ValueError(error_msg)
    
    if not prompt:
        error_msg = "提示词内容不能为空"
        logging.error(error_msg)
        raise ValueError(error_msg)
    if len(prompt) > 4000:
        error_msg = f"提示词过长（当前{len(prompt)}字符），最大允许4000字符"
        logging.error(error_msg)
        raise ValueError(error_msg)

    logging.info("调用DeepSeek API开始...")
    url = f"{BASE_URL}/chat/completions"
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 8000,
        "stream": stream_mode  # 根据参数决定是否启用流式输出
    }
    try:
        response = requests.post(
            url=url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "ResumeGenerator/1.0"
            },
            json=payload,
            timeout=60
        )
    except requests.exceptions.Timeout as e:
        logging.exception("API请求超时异常")
        raise ConnectionError("API请求超时，请检查网络连接并稍后重试")
    except requests.exceptions.ConnectionError as e:
        logging.exception("网络连接失败异常")
        logging.debug(f"请求URL: {url}")
        raise ConnectionError("网络连接失败，请检查本地网络或DeepSeek服务状态")
    except requests.exceptions.SSLError as e:
        logging.exception("SSL证书验证失败异常")
        raise ConnectionError("SSL证书验证失败，请检查系统时间或更新证书库")
    except requests.exceptions.RequestException as e:
        logging.exception("未知网络错误")
        raise ConnectionError(f"未知网络错误: {str(e)}")

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        try:
            response_data = response.json()
            error_details = response_data.get("error", {}).get("message", "无错误详情")
        except Exception:
            error_details = response.text[:200] + "..."
        error_msg = (
            f"API请求失败 [{response.status_code}]: {e}\n"
            f"错误详情：{error_details}\n"
            f"请求ID：{response.headers.get('X-Request-ID', '无')}"
        )
        logging.error(error_msg)
        raise ConnectionError(error_msg)

    try:
        response_data = response.json()
    except ValueError as e:
        error_info = (
            f"响应解析失败，状态码：{response.status_code}，原始响应：{response.text[:200]}...\n"
            "可能服务器返回了非JSON格式响应"
        )
        logging.exception("响应解析失败")
        raise ValueError(error_info)

    if not isinstance(response_data, dict):
        error_msg = f"响应数据结构异常，期望字典类型，实际得到：{type(response_data)}"
        logging.error(error_msg)
        raise ValueError(error_msg)
    if "choices" not in response_data:
        error_msg = "响应数据缺少关键字段：choices，完整响应：" + str(response_data)[:200]
        logging.error(error_msg)
        raise KeyError(error_msg)
    choices = response_data["choices"]
    if not isinstance(choices, list) or len(choices) == 0:
        error_msg = "choices字段为空或类型错误，期望非空列表"
        logging.error(error_msg)
        raise IndexError(error_msg)
    first_choice = choices[0]
    if "message" not in first_choice:
        error_msg = "choice条目缺少message字段"
        logging.error(error_msg)
        raise KeyError(error_msg)
    if "content" not in first_choice["message"]:
        error_msg = "message字段缺少content内容"
        logging.error(error_msg)
        raise ValueError(error_msg)

    content = first_choice["message"]["content"]
    if not content.strip():
        error_msg = "API返回内容为空，可能原因：触发内容过滤或模型生成失败"
        logging.error(error_msg)
        raise ValueError(error_msg)

    if len(content) < 100:
        error_msg = (
            f"生成内容过短（仅{len(content)}字符），可能原因：原始简历与岗位不匹配或Prompt设计不合理\n"
            f"生成内容：{content[:200]}..."
        )
        logging.error(error_msg)
        raise ValueError(error_msg)
    if "抱歉" in content or "无法" in content:
        error_msg = f"检测到模型拒绝响应：\n{content[:500]}\n建议检查Prompt及请求参数。"
        logging.error(error_msg)
        raise ValueError(error_msg)

    logging.info("DeepSeek API调用成功。")
    return content

def test_deepseek_connection(api_key: str) -> bool:
    """
    发送简单的测试prompt（例如 "Hello, please confirm your connection."），
    检查API是否能正确返回响应。
    """
    test_prompt = "Hello, please confirm your connection."
    try:
        response = call_deepseek_api(test_prompt, api_key, stream_mode=False)
        logging.info("API连接测试成功，返回结果: " + response)
        return True
    except Exception as e:
        logging.exception("API连接测试失败")
        return False

# ==============================
# Streamlit 主界面
# ==============================
def main():
    st.title("自动化针对性简历生成系统")

    # 简历输入方式选择
    input_method = st.radio("选择简历输入方式", ["文件上传 (Markdown)", "直接输入"])
    base_resume = ""
    if input_method == "文件上传 (Markdown)":
        base_resume_file = st.file_uploader("上传简历母版（当前仅支持Markdown格式）", type="md")
        if base_resume_file:
            try:
                base_resume = base_resume_file.read().decode("utf-8")
                logging.debug("读取上传文件成功。")
            except Exception as e:
                st.error("读取文件失败，请检查文件编码。")
                logging.exception("读取上传文件失败")
                return
    else:
        base_resume = st.text_area("直接输入简历内容（Markdown格式）", height=300)

    if not base_resume:
        st.warning("请上传或输入简历内容。")
        return

    # 职位需求选择
    job_files = {
        "网络工程师": "data/job_network_engineer.md",
        "大数据工程师": "data/job_data_scientist.md"
    }
    job_name = st.selectbox("选择职位需求", list(job_files.keys()))
    job_data = {}
    if job_name:
        try:
            with open(job_files[job_name], "r", encoding="utf-8") as f:
                job_file_content = f.read()
            job_data = parse_markdown(job_file_content)
        except Exception as e:
            st.error("读取职位需求文件失败，请检查文件路径及格式。")
            logging.exception("读取职位需求文件失败")
            return

    # API密钥输入
    api_key = st.text_input("输入DeepSeek API密钥", type="password")

    # 增加测试API连接的按钮
    if st.button("测试API连接"):
        if not api_key:
            st.error("请输入DeepSeek API密钥")
            logging.error("API密钥未输入。")
        else:
            with st.spinner("测试中..."):
                if test_deepseek_connection(api_key):
                    st.success("API连接测试成功！")
                else:
                    st.error("API连接测试失败，请检查日志信息。")

    # 正式生成简历的按钮
    if st.button("生成简历"):
        if not api_key:
            st.error("请输入DeepSeek API密钥")
            logging.error("API密钥未输入。")
        else:
            with st.spinner("生成中..."):
                try:
                    prompt = build_prompt(base_resume, job_data)
                    optimized_resume = call_deepseek_api(prompt, api_key)
                    logging.debug("DeepSeek返回的优化简历内容：" + optimized_resume[:100] + "...")
                    
                    latex_data = {
                        "name": "张三",
                        "contact": "zhangsan@email.com",
                        "experiences": [
                            {"company": "XX科技公司", "position": "全栈工程师", "duration": "2020.01 - 至今", "details": "负责前后端开发，使用Python和JavaScript。"},
                            {"company": "YY网络公司", "position": "网络工程师", "duration": "2018.06 - 2019.12", "details": "负责网络架构设计和维护。"}
                        ],
                        "skills": job_data.get("hard_skills", []),
                        "optimized_resume": optimized_resume
                    }
                    latex_content = fill_latex_template("templates/resume_template.tex", latex_data)

                    os.makedirs("output", exist_ok=True)
                    output_tex_path = os.path.join("output", "resume.tex")
                    with open(output_tex_path, "w", encoding="utf-8") as f:
                        f.write(latex_content)
                    logging.debug("LaTeX文件保存成功： " + output_tex_path)

                    compile_proc = subprocess.run(
                        ["xelatex", "resume.tex"],
                        cwd="output",
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    if compile_proc.returncode != 0:
                        error_msg = f"LaTeX编译失败:\nSTDOUT: {compile_proc.stdout}\nSTDERR: {compile_proc.stderr}"
                        logging.error(error_msg)
                        st.error("LaTeX编译失败，请检查日志文件。")
                        return
                    else:
                        logging.info("LaTeX编译成功。")

                    st.success("生成完成！")
                    with open(os.path.join("output", "resume.pdf"), "rb") as f:
                        st.download_button("下载简历", f, file_name="resume.pdf")
                except RetryError as e:
                    underlying_err = e.last_attempt.exception()
                    st.error(f"生成失败: {underlying_err}")
                    logging.exception("生成失败")
                except Exception as e:
                    st.error(f"生成失败: {e}")
                    logging.exception("生成失败")

if __name__ == "__main__":
    main()
