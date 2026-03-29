"""Serviço responsável por localizar e executar scripts da pasta scripts/."""

import importlib.util
import sys
from pathlib import Path

# Diretório base onde os scripts ficam armazenados.
SCRIPTS_DIR = Path(__file__).resolve().parent.parent.parent / "scripts"


def _validate_script_name(script_name: str) -> Path:
    """Valida o nome do script e retorna o caminho absoluto do arquivo.

    - O nome deve conter apenas caracteres alfanuméricos, underscores e hífens.
    - O arquivo deve existir dentro da pasta scripts/.
    - Impede path traversal e acesso a arquivos fora do diretório permitido.
    """
    # Verifica se o nome é seguro (sem /, .., etc.)
    safe_name = script_name.replace("-", "_")
    if not safe_name.isidentifier():
        raise ValueError(
            f"Nome de script inválido: '{script_name}'. "
            "Use apenas letras, números, underscores e hífens."
        )

    script_path = (SCRIPTS_DIR / f"{script_name}.py").resolve()

    # Garante que o caminho resolvido está dentro de SCRIPTS_DIR
    if not str(script_path).startswith(str(SCRIPTS_DIR.resolve())):
        raise ValueError("Caminho de script inválido: acesso fora do diretório permitido.")

    if not script_path.is_file():
        raise FileNotFoundError(f"Script não encontrado: '{script_name}.py'")

    return script_path


def run_script(script_name: str, payload: dict) -> dict:
    """Localiza, carrega e executa um script pelo nome.

    Cada script deve expor uma função `main(payload: dict) -> dict`.
    O `payload` recebido da API é repassado diretamente para a função main do script.

    Retorna o dicionário produzido pelo script.
    """
    script_path = _validate_script_name(script_name)

    module_name = f"scripts.{script_name.replace('-', '_')}"

    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Falha ao carregar o script: '{script_name}.py'")

    module = importlib.util.module_from_spec(spec)

    # Registra o módulo no sys.modules para evitar problemas de re-importação
    sys.modules[module_name] = module

    spec.loader.exec_module(module)

    if not hasattr(module, "main"):
        raise AttributeError(
            f"O script '{script_name}.py' não possui a função 'main(payload)'."
        )

    result = module.main(payload)

    if not isinstance(result, dict):
        raise TypeError(
            f"O script '{script_name}.py' deve retornar um dicionário (dict). "
            f"Recebido: {type(result).__name__}"
        )

    return result
