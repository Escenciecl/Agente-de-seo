from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analizar_pagina(pagina):
    prompt = f"""Eres un experto SEO. Analiza esta página web y da recomendaciones específicas.

URL: {pagina['url']}
Título: {pagina['title']}
Meta descripción: {pagina['meta_desc']}
H1: {pagina['h1']}
Código HTTP: {pagina['status_code']}

Responde en español con:
1. PROBLEMAS: Lista los problemas SEO que encuentras
2. ACCIONES: Lista las acciones concretas a tomar, en orden de prioridad
3. PRIORIDAD: Alta, Media o Baja

Sé específico y directo."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content

def analizar_sitio_completo():
    from database import get_client, save_recommendation
    db = get_client()
    pages = db.table("pages").select("*").execute().data
    
    print(f"Analizando {len(pages)} páginas con IA...\n")
    
    for pagina in pages:
        print(f"Analizando: {pagina['url']}")
        analisis = analizar_pagina(pagina)
        print(analisis)
        print("-" * 50)
        
        save_recommendation(
            page_url=pagina['url'],
            type='seo',
            priority=5,
            description=analisis
        )
    
    print("\nAnálisis completo. Recomendaciones guardadas en Supabase.")

