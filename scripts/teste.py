"""Script de exemplo para demonstrar o fluxo completo da API.

Este script expõe uma função `main(payload)` que recebe o body da
requisição POST e retorna uma resposta simples com eco do payload.
"""


def main(payload: dict) -> dict:
    """Função principal do script.

    Args:
        payload: Dicionário com os dados recebidos do body da requisição.

    Returns:
        Dicionário com mensagem de sucesso e eco do payload recebido.
    """
    return {
        "message": "Script executado com sucesso!",
        "echo": payload,
    }
