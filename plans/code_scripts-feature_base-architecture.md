# Plano de acao - Base FastAPI com execucao de scripts

## Objetivo
Criar a base de uma aplicacao em Python com FastAPI, sem banco de dados, contendo:
- estrutura inicial de pastas;
- uma API `run/{script_name}/`;
- uma pasta `scripts/` com scripts executaveis;
- um script `teste.py` como exemplo;
- repasse do body da requisicao para o script, sem tipagem fixa.

## Estrutura prevista
```text
app/
  main.py
  api/
    routes/
      run.py
  services/
    script_runner.py
scripts/
  teste.py
plans/
  code_scripts-feature_base-architecture.md
requirements.txt
README.md
```

## Ordem de execucao
1. Criar a estrutura base de pastas e arquivos da aplicacao.
2. Configurar o ponto de entrada do FastAPI em `app/main.py`.
3. Implementar a rota dinamica `POST /run/{script_name}/`.
4. Criar uma camada de servico para localizar e executar scripts da pasta `scripts/`.
5. Definir o contrato de comunicacao entre API e script.
6. Criar `scripts/teste.py` como referencia funcional.
7. Validar o fluxo completo com um teste manual simples.

## Etapas de implementacao

### 1. Base do projeto
- Criar a estrutura de pastas `app/`, `app/api/routes/`, `app/services/` e `scripts/`.
- Adicionar os `__init__.py` necessarios, se desejado para organizacao do pacote.
- Criar `requirements.txt` com o minimo necessario, como `fastapi` e `uvicorn`.

### 2. Arquivo principal da API
- Implementar `app/main.py` com a instancia do FastAPI.
- Registrar o router responsavel pela execucao de scripts.
- Manter a aplicacao enxuta, sem configuracoes de banco ou dependencias nao utilizadas.

### 3. Endpoint dinamico
- Criar a rota `POST /run/{script_name}/`.
- Receber o body como JSON generico, sem schema tipado.
- Encaminhar o nome do script e o body bruto para a camada de execucao.

### 4. Execucao de scripts
- Implementar um servico que resolva o arquivo `{script_name}.py` dentro de `scripts/`.
- Bloquear caminhos invalidos ou tentativas de path traversal.
- Executar o script de forma padronizada e capturar seu retorno.

### 5. Contrato entre API e scripts
- Definir um contrato simples para os scripts, por exemplo uma funcao `main(payload)` que recebe o body e retorna um valor serializavel.
- Carregar e executar o script dinamicamente usando importacao controlada.
- Retornar na API exatamente o resultado produzido pelo script, desde que seja compativel com JSON.

### 6. Script de exemplo
- Criar `scripts/teste.py`.
- Implementar logica simples para demonstrar que o payload recebido pela API chega ao script.
- Exemplo esperado: devolver uma mensagem e ecoar o body recebido.

### 7. Validacao
- Subir a aplicacao localmente com `uvicorn`.
- Testar `POST /run/teste/` com um body JSON qualquer.
- Confirmar:
  - que o script correto foi localizado;
  - que o payload foi repassado sem tipagem fixa;
  - que a resposta da API reflete o retorno do script.

## Riscos e cuidados
- Seguranca: impedir que o parametro da rota permita executar arquivos fora da pasta `scripts/`.
- Padronizacao: definir claramente como cada script deve expor sua funcao executavel.
- Serializacao: garantir que o retorno dos scripts seja compativel com resposta JSON.
- Tratamento de erro: responder adequadamente para script inexistente, erro de execucao ou retorno invalido.

## Dependencias
- Python 3.10+ ou versao compativel com FastAPI adotada no projeto.
- `fastapi`
- `uvicorn`

## Criterios de aceite
- Existe uma aplicacao FastAPI inicializavel localmente.
- Existe a pasta `scripts/`.
- A rota `POST /run/{script_name}/` esta funcional.
- O body da requisicao e recebido sem tipagem fixa e enviado ao script.
- O arquivo `scripts/teste.py` existe e demonstra o fluxo completo.
- A API retorna o resultado produzido pelo script.
