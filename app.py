import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Topic(BaseModel):
    topic: str

@app.post("/generate-post")
async def generate_post_api(data: Topic):
    topic = data.topic

    try:
        # Заголовок
        title_prompt = f"Придумай привлекательный заголовок для блога на тему: {topic}"
        title_resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": title_prompt}],
            max_tokens=60,
            temperature=0.7
        )
        title = title_resp.choices[0].message.content.strip()

        # Мета-описание
        meta_prompt = f"Напиши мета-описание (до 150 символов) для статьи с заголовком: {title}"
        meta_resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": meta_prompt}],
            max_tokens=100,
            temperature=0.7
        )
        meta = meta_resp.choices[0].message.content.strip()

        # Основной текст
        content_prompt = f"""Напиши развернутую статью на тему '{topic}' с заголовком '{title}'.
Статья должна быть:
- С подзаголовками
- С короткими абзацами
- Интересной, доступной и полезной
- Объём не менее 1000 символов
"""
        post_resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": content_prompt}],
            max_tokens=1500,
            temperature=0.7
        )
        content = post_resp.choices[0].message.content.strip()

        return {
            "title": title,
            "meta_description": meta,
            "post_content": content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"status": "ok"}
