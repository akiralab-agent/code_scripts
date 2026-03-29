"""Rota dinâmica para execução de scripts via POST /run/{script_name}/."""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.services.script_runner import run_script

router = APIRouter()


@router.post("/run/{script_name}/")
async def run_script_endpoint(script_name: str, request: Request):
    """Executa um script pelo nome, repassando o body da requisição.

    O body é recebido como JSON genérico, sem tipagem fixa, e enviado
    integralmente como `payload` para a função `main(payload)` do script.
    """
    # Recebe o body como JSON genérico (dict ou lista)
    body = await request.json()

    # Garante que o payload seja um dict
    if not isinstance(body, dict):
        payload = {"data": body}
    else:
        payload = body

    try:
        result = run_script(script_name, payload)
        return JSONResponse(content={"status": "success", "result": result})
    except FileNotFoundError as exc:
        return JSONResponse(
            status_code=404,
            content={"status": "error", "message": str(exc)},
        )
    except ValueError as exc:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(exc)},
        )
    except AttributeError as exc:
        return JSONResponse(
            status_code=422,
            content={"status": "error", "message": str(exc)},
        )
    except TypeError as exc:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(exc)},
        )
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Erro ao executar o script: {exc}"},
        )
