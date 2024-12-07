# Golden Raspberry Awards API

## Descrição

Esta é uma aplicação FastAPI que fornece um endpoint para calcular os intervalos de prêmios ganhos pelos produtores na categoria de "Pior Filme" do Golden Raspberry Awards.

## Requisitos

- Python 3.10 ou superior
- `pip` para instalação de dependências

## Configuração do Ambiente

1. **Clone o repositório**

   ```bash
   git clone https://github.com/rafael-pardinho/golden-raspberry-awards-api.git
   cd golden-raspberry-awards-api.git
   ```

2. **Crie um ambiente virtual**

   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual**

   - No Linux/MacOS:
     ```bash
     source venv/bin/activate
     ```
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

5. **Coloque o arquivo CSV**
   Certifique-se de que o arquivo `movielist.csv` está localizado no caminho `data/movielist.csv`. O formato esperado é delimitado por `;`.

## Executando a Aplicação

1. **Inicie o servidor FastAPI**

   ```bash
   uvicorn app:app --reload
   ```

2. **Acesse os endpoints**

   - Documentação Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Documentação ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Testando o Endpoint

O endpoint principal é:

- **GET /producers/intervals**: Retorna os produtores com os menores e maiores intervalos entre dois prêmios consecutivos.

### Exemplo de Resposta

```json
{
  "min": [
    {
      "producer": "Producer 1",
      "interval": 1,
      "previousWin": 2008,
      "followingWin": 2009
    }
  ],
  "max": [
    {
      "producer": "Producer 2",
      "interval": 5,
      "previousWin": 2000,
      "followingWin": 2005
    }
  ]
}
```

## Estrutura do Projeto

- **`app.py`**: Arquivo principal da aplicação.
- **`test_api.py`**: Arquivo para rodar o teste da API.
- **`requirements.txt`**: Lista de dependências Python.
- **`data/movielist.csv`**: Arquivo CSV contendo os dados dos filmes.

## Testes

1. Certifique-se de que o ambiente virtual está ativado.
2. Rode os testes utilizando o seguinte comando:
   ```bash
   pytest test_api.py
   ```

## Dependências

- `fastapi`
- `uvicorn`
- `pytest`
- `httpx`

Instale todas as dependências usando:

```bash
pip install -r requirements.txt
```

## Observações

- Certifique-se de que o arquivo CSV esteja no formato correto e no caminho esperado.
- Esta aplicação usa o banco de dados SQLite em memória. Todos os dados serão perdidos ao encerrar a aplicação.

