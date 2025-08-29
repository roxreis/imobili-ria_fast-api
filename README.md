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

```sh
  
  app/
    api/
      routers/
        transactions.py
        parties.py
        comissoes.py
    interfaces/
        abstract/
            transaction_interface.py
        concrete/
            transaction_concrete.py
    repository/
        transactions.py   # operações de transações
        party.py
        commissions.py
    service/
        transactions.py   # operações de transações
        party.py
        commisson.py
    tests/
      unit/
        __init__.py
        test_commission.py   # operações de transações
        test_party.py
        test_transaction.py
    __init__.py
    alembic.ini
    database.py
    main.py
    models.py
    chemas.py
    validators.py
migrations/
  versions/
    0c635a74006a_create_tables.py
  env.py
  README  
  script.py.mako
```


---

## ⚙️ Configuração

### Variáveis de ambiente (`.env`)
Crie um arquivo `.env` na raiz do projeto com base em `.env.example`:

Banco de dados
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/pipeimob

Bearer Token fixo
API_SECRET_KEY=1234567890abcdef



---

## ▶️ Rodando o projeto

### Local (sem Docker)
Criar virtualenv
python -m venv venv
source venv/bin/activate

Instalar dependências
pip install -r requirements.txt

Iniciar servidor
uvicorn app.main:app --reload

Mudar nome .env.example para .env para carregar variáveis de ambiente



Verificar se está online em: http://localhost:8000

---

### Com Docker
docker compose build

docker compose up -d

Acesse em: se está online http://localhost:8000
### Não precisa rodar migration

---
## Documentação do Swagger
A documentação da API está disponível através do Swagger. 
Após iniciar os containers Docker, você pode acessar a documentação do Swagger pelo seguinte link:

http://localhost:8000/docs

### Authorized Swagger = 1234567890abcdef

## 🔑 Autenticação
Todos os endpoints da API requerem **Bearer Token**:  

Authorization: Bearer 1234567890abcdef


O valor de `API_SECRET_KEY` vem do `docker-compose.yml`.  




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
## 📋 Testes
Foram criados uniários com pytest.
Para rodar os testes:
```
docker compose exec api pytest app/tests/unit
```
