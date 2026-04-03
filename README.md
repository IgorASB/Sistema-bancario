# Sistema Bancário em Python (POO)

Sistema bancário desenvolvido em Python utilizando Programação Orientada a Objetos. Permite cadastro de usuários, criação de múltiplas contas, depósitos, saques com limites configuráveis por período do dia, extrato detalhado e gerenciamento de limites.

## Funcionalidades

### Menu Inicial
- **1 - Novo usuário** – Cadastra cliente com CPF (11 dígitos, apenas números), nome completo (apenas letras, espaços e hífens), data de nascimento (dd-mm-aaaa) e endereço.
- **2 - Nova conta** – Cria uma conta bancária para um CPF já cadastrado. Agência fixa `0001`, número sequencial.
- **3 - Acessar conta** – Exibe todas as contas do CPF informado e permite escolher qual acessar (se houver apenas uma, acessa automaticamente).
- **0 - Encerrar sistema** – Finaliza o programa.

### Menu Bancário (após acessar uma conta)
- **D - Depositar** – Adiciona saldo, respeitando limite acumulado por período (tarde/noite).
- **S - Sacar** – Retira saldo obedecendo:
  - Limite máximo por saque: R$ 500,00
  - Limite diário: 3 saques
  - Limite acumulado por período (ex.: R$ 5.000 na tarde, R$ 2.000 na noite)
  - Saldo disponível
- **E - Extrato** – Mostra todas as movimentações com data/hora, saldo atual e totais do período.
- **L - Limites** – Consulta ou altera os limites de depósito e saque para os períodos da tarde (12h às 18h) e noite (18h às 12h).
- **LC - Listar contas** – Exibe todas as contas do sistema (agência, número, titular, saldo).
- **Q - Sair da conta** – Retorna ao menu inicial.

## Regras de Negócio

- **Limites por período (acumulativos)**:
  - Tarde (12:00 – 17:59): depósito máximo R$ 5.000,00 / saque máximo R$ 5.000,00 (total no período)
  - Noite (18:00 – 11:59): depósito máximo R$ 2.000,00 / saque máximo R$ 2.000,00 (total no período)
  - Os totais são zerados automaticamente quando o período muda.
- **Limite por transação de saque**: R$ 500,00 fixo.
- **Limite diário de saques**: 3 saques por dia (reset à meia-noite).
- Validações:
  - CPF: apenas números e exatamente 11 dígitos.
  - Nome: apenas letras (incluindo acentuadas), espaços e hífens.
  - Data de nascimento: formato `dd-mm-aaaa`.
  - Valores positivos para depósitos e saques.
  - Saldo suficiente para saque.
  - CPF único por usuário.

## Estrutura do Código

- **Classe `ConfiguracaoLimites`** (métodos de classe): gerencia os limites globais por período, consulta e alteração.
- **Classe `Cliente`**: armazena CPF, nome, data de nascimento e endereço.
- **Classe `Conta`**: controla número, agência, saldo, extrato, limites diários e acumulados por período.
- **Funções auxiliares**: `validar_cpf()`, `validar_nome()`, `limpar_tela()`, `criar_usuario()`, `criar_conta()`, `acessar_conta()`, `listar_contas()`, menus.
- **Estruturas globais**: dicionários `clientes` e `contas`, `proximo_numero_conta`, `conta_atual`.
