
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
   uvicorn app.frameworks_and_drivers.api.api:app --reload
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

## Arquitetura do Projeto

Este projeto segue os princípios da **Clean Architecture**. A arquitetura foi organizada para promover a separação de responsabilidades e a independência entre as camadas.

### Estrutura

- **Domain (Camada de Domínio)**: Contém as regras de negócio fundamentais. 
  - **`entities/movie.py`**: Define a entidade `Movie` com os atributos necessários.

- **Use Cases (Casos de Uso)**: Implementa a lógica de aplicação.
  - **`use_cases/producer_intervals.py`**: Calcula os intervalos entre prêmios consecutivos para os produtores.

- **Interface Adapters (Adaptadores de Interface)**: Faz a ponte entre o domínio e os frameworks ou tecnologias externas.
  - **`repositories/movie_repository.py`**: Interage com o banco de dados para buscar os dados.
  - **`controllers/producer_controller.py`**: Controla o fluxo de dados entre os casos de uso e os endpoints.

- **Frameworks e Drivers**: Contém detalhes específicos de infraestrutura.
  - **`database/sqlite_handler.py`**: Gerencia a conexão com o banco de dados SQLite.
  - **`api/api.py`**: Define os endpoints da aplicação usando FastAPI.

### Justificativa para a Clean Architecture

1. **Independência de Frameworks**: A lógica de negócio não depende diretamente do FastAPI ou SQLite, permitindo substituí-los facilmente.
2. **Testabilidade**: Cada camada é isolada, facilitando a criação de testes unitários.
3. **Facilidade de Manutenção**: A separação de responsabilidades torna o código mais organizado e menos propenso a erros ao evoluir.
4. **Reutilização**: As regras de negócio e os casos de uso podem ser reutilizados em diferentes contextos (ex.: APIs REST, serviços de backend).

## Testes

1. Certifique-se de que o ambiente virtual está ativado.
2. Rode os testes utilizando o seguinte comando:
   ```bash
   pytest
   ```

---
