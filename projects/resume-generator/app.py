import os
import re
import subprocess
import streamlit as st
from jinja2 import Template
import requests

# Markdown解析函数
def parse_markdown(md_content):
    data = {}
    desc_match = re.search(r"\*职位描述：\*\s*(.*?)\n\*", md_content, re.DOTALL)
    if desc_match:
        data["job_desc"] = desc_match.group(1).strip()
    hard_skills_match = re.search(r"\*硬技能：\*\s*((?:- .*\n)+)", md_content)
    if hard_skills_match:
        data["hard_skills"] = [s.strip() for s in hard_skills_match.group(1).split("- ") if s.strip()]
    keywords_match = re.search(r"\*简历关键词：\*\s*((?:- .*\n)+)", md_content)
    if keywords_match:
        data["keywords"] = [s.strip() for s in keywords_match.group(1).split("- ") if s.strip()]
    return data

# Prompt组装函数
def build_prompt(base_resume, job_data):
    prompt = f"""
    请根据以下信息优化简历：
    - 目标岗位描述：{job_data['job_desc']}
    - 硬技能要求：{', '.join(job_data['hard_skills'])}
    - 关键词：{', '.join(job_data['keywords'])}
    
    原始简历内容：
    {base_resume}
    
    要求：
    1. 突出硬技能和相关经验
    2. 使用关键词优化描述
    3. 保持简洁和专业
    """
    return prompt

# DeepSeek API调用函数
def call_deepseek_api(prompt, api_key):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API调用失败：{response.status_code}")

# LaTeX模板填充函数
def fill_latex_template(template_path, data):
    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())
    return template.render(data)

# 主函数
def main():
    st.title("自动化简历生成系统")
    
    # 上传简历母版
    base_resume_file = st.file_uploader("上传简历母版（Markdown格式）", type="md")
    if base_resume_file:
        base_resume = base_resume_file.read().decode("utf-8")
    
    # 选择职位需求
    job_files = {
        "网络工程师": "data/job_network_engineer.md",
        "大数据工程师": "data/job_data_scientist.md"
    }
    job_name = st.selectbox("选择职位需求", list(job_files.keys()))
    if job_name:
        with open(job_files[job_name], "r", encoding="utf-8") as f:
            job_data = parse_markdown(f.read())
    
    # 输入DeepSeek API密钥
    api_key = st.text_input("输入DeepSeek API密钥")
    
    # 生成简历
    if st.button("生成简历"):
        if not api_key:
            st.error("请输入DeepSeek API密钥")
        else:
            with st.spinner("生成中..."):
                # 组装Prompt
                prompt = build_prompt(base_resume, job_data)
                # 调用DeepSeek API
                optimized_resume = call_deepseek_api(prompt, api_key)
                # 填充LaTeX模板
                latex_content = fill_latex_template("templates/resume_template.tex", {
                    "name": "张三",
                    "contact": "zhangsan@email.com",
                    "experiences": [
                        {"company": "XX科技公司", "position": "全栈工程师", "duration": "2020.01 - 至今", "details": "负责前后端开发，使用Python和JavaScript。"},
                        {"company": "YY网络公司", "position": "网络工程师", "duration": "2018.06 - 2019.12", "details": "负责网络架构设计和维护。"}
                    ],
                    "skills": job_data["hard_skills"]
                })
                # 保存并编译LaTeX
                os.makedirs("output", exist_ok=True)
                with open("output/resume.tex", "w", encoding="utf-8") as f:
                    f.write(latex_content)
                subprocess.run(["xelatex", "resume.tex"], cwd="output")
                # 提供下载链接
                st.success("生成完成！")
                with open("output/resume.pdf", "rb") as f:
                    st.download_button("下载简历", f, file_name="resume.pdf")

if __name__ == "__main__":
    main()