import google.generativeai as genai

PROMPT_TEMPLATE = """你是一位技術部落格摘要助手。請根據以下英文技術文章，完成兩件事：
1. 將文章標題翻譯成繁體中文
2. 用2-3句繁體中文摘要文章的核心技術重點

請以這個格式回覆（只輸出這兩行，不要其他文字）：
[中文標題]
[中文摘要]

---
標題：{title}
內容：{body}
"""

def summarize_article(title: str, body: str, api_key: str) -> dict:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = PROMPT_TEMPLATE.format(title=title, body=body[:2000])
        response = model.generate_content(prompt)
        lines = response.text.strip().split("\n", 1)
        zh_title = lines[0].strip() if lines else title
        zh_summary = lines[1].strip() if len(lines) > 1 else ""
        return {"zh_title": zh_title, "zh_summary": zh_summary}
    except Exception as e:
        print(f"[summarizer] Gemini error: {e}")
        return {"zh_title": title, "zh_summary": ""}
