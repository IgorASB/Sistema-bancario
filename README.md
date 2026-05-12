# 🏦 Sistema Bancário em Python (POO)

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Paradigma](https://img.shields.io/badge/Paradigma-POO-6A0DAD?style=for-the-badge)]()
[![Interface](https://img.shields.io/badge/Interface-CLI-black?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Concluído-28a745?style=for-the-badge)]()

</div>

> Sistema bancário desenvolvido em Python com Programação Orientada a Objetos. Permite cadastro de usuários, criação de múltiplas contas, depósitos e saques com limites configuráveis por período do dia, extrato detalhado e gerenciamento de limites.

---

## ⚙️ Funcionalidades

### Menu Inicial
- **1 — Novo usuário** – Cadastra cliente com CPF (11 dígitos), nome completo, data de nascimento e endereço
- **2 — Nova conta** – Cria conta para CPF já cadastrado. Agência fixa `0001`, número sequencial
- **3 — Acessar conta** – Lista contas do CPF informado e abre a selecionada
- **0 — Encerrar sistema** – Finaliza o programa

### Menu Bancário
- **D — Depositar** – Adiciona saldo respeitando limite acumulado por período
- **S — Sacar** – Retira saldo obedecendo limite por saque (R$ 500), limite diário (3 saques) e saldo disponível
- **E — Extrato** – Exibe todas as movimentações com data/hora, saldo e totais do período
- **L — Limites** – Consulta ou altera limites de depósito e saque por período
- **LC — Listar contas** – Exibe todas as contas do sistema
- **Q — Sair da conta** – Retorna ao menu inicial

---

## 💼 Regras de Negócio

| Regra | Detalhe |
|---|---|
| Limite por saque | R$ 500,00 fixo por transação |
| Limite diário de saques | 3 saques por dia (reset à meia-noite) |
| Período Tarde (12h–17h59) | Depósito/saque máx. acumulado: R$ 5.000,00 |
| Período Noite (18h–11h59) | Depósito/saque máx. acumulado: R$ 2.000,00 |
| CPF | Apenas 11 dígitos numéricos, único por usuário |
| Data de nascimento | Formato `dd-mm-aaaa` |

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.10 ou superior — verifique com `python --version`

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/IgorASB/Sistema-bancario.git
cd Sistema-bancario

# 2. Execute
python sistema_bancario.py
```

---

## 🧠 Conceitos de Python Aplicados

| Conceito | Aplicação no Projeto |
|---|---|
| Classes e Objetos | `Cliente`, `Conta`, `ConfiguracaoLimites` representam entidades do domínio |
| Métodos de classe (`@classmethod`) | Gerenciamento de limites globais por período via `ConfiguracaoLimites` |
| Encapsulamento | Lógica de validação de saldo e limites encapsulada nos métodos da `Conta` |
| Dicionários | Armazenamento de clientes e contas em memória (`clientes`, `contas`) |
| `datetime` | Controle de período do dia e reset de limites diários |
| Funções auxiliares | Validação de CPF, nome e data com expressões regulares (`re`) |

---

## 📁 Estrutura do Projeto

```
Sistema-bancario/
├── sistema_bancario.py   # Código-fonte principal
└── README.md
```

---

## 👤 Autor

Feito por **Igor Amaral** — Estudante de Ciência da Computação

[![GitHub](https://img.shields.io/badge/GitHub-IgorASB-181717?style=flat&logo=github)](https://github.com/IgorASB)
