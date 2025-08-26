# PipeImob FastAPI
Sistema API para transações imobiliárias construído com FastAPI, PostgreSQL, e arquitetura em camadas.

---

## Tecnologias utilizadas
- Python 3.11
- FastAPI
- SQLAlchemy + Alembic
- PostgreSQL
- Docker + docker-compose
- Pydantic (validação)

---

## 📂 Estrutura do projeto

´´´
app/
  main.py              # inicialização FastAPI
  models.py            # modelos SQLAlchemy
  schemas.py           # validações Pydantic
  database.py          # conexão e sessão
  crud/
     transactions.py   # operações de transações
     partes.py
     comissoes.py
  routers/
     transacoes.py
     partes.py
     comissoes.py
  core/
     config.py          # env settings
     auth.py            # Bearer token
     exceptions.py
alembic/               # migrations
tests/                 # pytest
docker-compose.yml
Dockerfile
.env.example
README.md
´´´


---

## ⚙️ Configuração

### Variáveis de ambiente (`.env`)
Crie um arquivo `.env` na raiz do projeto com base em `.env.example`:

Banco de dados
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/pipeimob

Bearer Token fixo
API_SECRET_KEY=changeme123



---

## ▶️ Rodando o projeto

### Local (sem Docker)
Criar virtualenv
python -m venv venv
source venv/bin/activate

Instalar dependências
pip install -r requirements.txt

Rodar migrações (Alembic)
alembic upgrade head

Iniciar servidor
uvicorn app.main:app --reload



Acesse em: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Com Docker
docker-compose up --build

docker compose exec api uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

- `main` é o arquivo Python que contém o FastAPI app (ex: `main.py`)
- `app` é o nome da instância FastAPI dentro do arquivo
- A flag `--reload` faz reiniciar o servidor automaticamente ao salvar alterações (use só em desenvolvimento)



Acesse em: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔑 Autenticação
Todos os endpoints da API requerem **Bearer Token**:  

Authorization: Bearer <API_SECRET_KEY>



O valor de `API_SECRET_KEY` vem do `.env`.  

---

## 📌 Endpoints principais

### Transações
- `POST /api/v1/transacoes`
- `GET /api/v1/transacoes` (filtros + paginação)
- `GET /api/v1/transacoes/{id}`
- `PUT /api/v1/transacoes/{id}`
- `PATCH /api/v1/transacoes/{id}/status`
- `DELETE /api/v1/transacoes/{id}`

### Partes
- `POST /api/v1/transacoes/{id}/partes`
- `DELETE /api/v1/partes/{id}`

### Comissões
- `POST /api/v1/transacoes/{id}/comissoes`
- `POST /api/v1/comissoes/{id}/pagar`

---

## 📋 Regras de Negócio
- Transação só pode ser **APROVADA** se tiver:
  - pelo menos **1 comprador**
  - pelo menos **1 vendedor**
  - pelo menos **1 corretor**

- Fluxo de status:
CRIADA -> EM_ANALISE -> APROVADA -> FINALIZADA

-> CANCELADA



- `valor_calculado` da comissão é sempre derivado de `valor_venda * percentual`.

---

## ☁️ Proposta de Deploy (AWS)

### Serviços utilizados
- **ECS Fargate** → execução dos containers da API
- **RDS (PostgreSQL)** → banco de dados gerenciado
- **ECR** → armazenamento da imagem Docker
- **Secrets Manager** → variáveis sensíveis (chaves, credenciais)
- **ALB (Application Load Balancer)** → entrada HTTPS
- **CloudWatch** → logs centralizados
- **IAM Roles** → permissões de acesso seguro

### Fluxo de deploy (CD)
1. Push no **GitHub** → GitHub Actions builda a imagem → envia para **ECR**.  
2. Serviço no **ECS (Fargate)** puxa a imagem e roda os containers.  
3. Banco em **RDS (PostgreSQL)**.  
4. Variáveis injetadas via **Secrets Manager**.  
5. Logs monitorados pelo **CloudWatch**.  

---

## ✅ Próximos passos
- Implementar regras em `partes.py` e `comissoes.py`
- Criar **migrations Alembic**
- Adicionar **testes pytest** para cobrir as regras de negócio