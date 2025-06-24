
from typing import Optional
from fastapi import APIRouter, requests
import httpx
from pydantic import BaseModel, Field

router = APIRouter()

class Consulta(BaseModel):
    pregunta : Optional[str] = Field(None, min_length=3)


@router.post("/pregunta")
async def consultar(consulta: Consulta):
    print("consulta", consulta)
    """Consulta al modelo local Ollama"""
    pregunta = f"""
        Pregunta: {consulta.pregunta}
        Condicion: A base de la pregunta responde una respuesta corta
"""
    async with httpx.AsyncClient(timeout=60) as client:
        response_final = await client.post(f"http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": pregunta,
            "stream": False,
            "options": {"temperature": 0.2, "num_predict":64}
        })

    respuesta = response_final.json()["response"].strip()
    print(respuesta)
    return {
        "respuesta": respuesta
    }