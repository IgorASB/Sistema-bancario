from datetime import datetime
import os
import re

# ====================== CONFIGURAÇÃO DE LIMITES ======================
class ConfiguracaoLimites:
    """Armazena e gerencia os limites por período (tarde e noite)."""
    _limites = {
        'tarde': {'deposito': 5000.0, 'saque': 5000.0},
        'noite': {'deposito': 2000.0, 'saque': 2000.0}
    }

    @classmethod
    def obter_periodo_atual(cls):
        hora = datetime.now().hour
        if 12 <= hora < 18:
            return 'tarde'
        else:
            return 'noite'

    @classmethod
    def obter_limite_deposito(cls, periodo=None):
        if periodo is None:
            periodo = cls.obter_periodo_atual()
        return cls._limites[periodo]['deposito']

    @classmethod
    def obter_limite_saque(cls, periodo=None):
        if periodo is None:
            periodo = cls.obter_periodo_atual()
        return cls._limites[periodo]['saque']

    @classmethod
    def alterar_limite(cls, periodo, tipo, novo_valor):
        if novo_valor <= 0:
            print("Operacao falhou! O valor do limite deve ser positivo.")
            return False
        cls._limites[periodo][tipo] = novo_valor
        print(f"Limite de {tipo} no periodo {periodo} alterado para R$ {novo_valor:.2f}")
        return True

    @classmethod
    def exibir_limites(cls):
        print("\n--- CONSULTA DE LIMITES POR PERIODO ---")
        print(f"Periodo atual: {cls.obter_periodo_atual().upper()}")
        print("-" * 40)
        for periodo in ['tarde', 'noite']:
            print(f"{periodo.upper()}:")
            print(f"  Deposito maximo: R$ {cls._limites[periodo]['deposito']:.2f}")
            print(f"  Saque maximo:    R$ {cls._limites[periodo]['saque']:.2f}")
        print("-" * 40)

    @classmethod
    def menu_configuracao(cls):
        """Submenu para consultar e alterar limites."""
        while True:
            cls.exibir_limites()
            print("\nOpcoes:")
            print("[1] Consultar limites novamente")
            print("[2] Alterar limites")
            print("[0] Voltar ao menu bancario")
            op = input("Escolha: ").strip()
            if op == "0":
                break
            elif op == "1":
                continue
            elif op == "2":
                cls.menu_alteracao()
            else:
                print("Opcao invalida.")
            input("\nPressione Enter para continuar...")
            limpar_tela()

    @classmethod
    def menu_alteracao(cls):
        while True:
            print("\n--- ALTERAR LIMITES ---")
            print("[1] Alterar limite de DEPOSITO na TARDE")
            print("[2] Alterar limite de SAQUE na TARDE")
            print("[3] Alterar limite de DEPOSITO na NOITE")
            print("[4] Alterar limite de SAQUE na NOITE")
            print("[0] Voltar ao menu de limites")
            op = input("Escolha: ").strip()
            if op == "0":
                break
            try:
                if op == "1":
                    novo = float(input("Novo valor para deposito (tarde): R$ "))
                    cls.alterar_limite('tarde', 'deposito', novo)
                elif op == "2":
                    novo = float(input("Novo valor para saque (tarde): R$ "))
                    cls.alterar_limite('tarde', 'saque', novo)
                elif op == "3":
                    novo = float(input("Novo valor para deposito (noite): R$ "))
                    cls.alterar_limite('noite', 'deposito', novo)
                elif op == "4":
                    novo = float(input("Novo valor para saque (noite): R$ "))
                    cls.alterar_limite('noite', 'saque', novo)
                else:
                    print("Opcao invalida.")
            except ValueError:
                print("Valor invalido. Digite um numero.")
            input("\nPressione Enter para continuar...")
            limpar_tela()

# ====================== CLASSES PRINCIPAIS ======================
class Cliente:
    def __init__(self, cpf: str, nome: str, data_nascimento: str, endereco: str):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = endereco

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"

class Conta:
    AGENCIA = "0001"
    LIMITE_SAQUE_VALOR = 500.0
    LIMITE_SAQUES_DIA = 3

    def __init__(self, numero: int, cliente: Cliente):
        self.numero = numero
        self.cliente = cliente
        self.saldo = 0.0
        self.extrato = []
        self.numero_saques_hoje = 0
        self.data_ultimo_saque = datetime.now().date()
        self.periodo_atual = ConfiguracaoLimites.obter_periodo_atual()
        self.total_saques_periodo = 0.0
        self.total_depositos_periodo = 0.0

    def _resetar_limite_diario(self):
        hoje = datetime.now().date()
        if self.data_ultimo_saque != hoje:
            self.numero_saques_hoje = 0
            self.data_ultimo_saque = hoje

    def _resetar_limite_periodo(self):
        novo_periodo = ConfiguracaoLimites.obter_periodo_atual()
        if novo_periodo != self.periodo_atual:
            self.periodo_atual = novo_periodo
            self.total_saques_periodo = 0.0
            self.total_depositos_periodo = 0.0

    def _verificar_limite_horario_acumulado(self, valor, tipo_operacao):
        periodo = self.periodo_atual
        if tipo_operacao == 'deposito':
            limite = ConfiguracaoLimites.obter_limite_deposito(periodo)
            total_usado = self.total_depositos_periodo
        else:
            limite = ConfiguracaoLimites.obter_limite_saque(periodo)
            total_usado = self.total_saques_periodo

        if total_usado + valor > limite:
            restante = limite - total_usado
            return False, f"Operacao nao permitida no periodo {periodo.upper()}. Limite maximo acumulado e R$ {limite:.2f}. Voce ja utilizou R$ {total_usado:.2f} neste periodo. Pode movimentar no maximo mais R$ {restante:.2f}."
        return True, ""

    def depositar(self, valor: float) -> bool:
        self._resetar_limite_periodo()
        if valor <= 0:
            print("Operacao falhou! O valor do deposito deve ser positivo.")
            return False
        ok, msg = self._verificar_limite_horario_acumulado(valor, 'deposito')
        if not ok:
            print(f"Operacao falhou! {msg}")
            return False
        self.saldo += valor
        self.total_depositos_periodo += valor
        self.extrato.append(f"Deposito: +R$ {valor:.2f} - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Deposito de R$ {valor:.2f} realizado com sucesso!")
        return True

    def sacar(self, valor: float) -> bool:
        self._resetar_limite_periodo()
        self._resetar_limite_diario()
        if valor <= 0:
            print("Operacao falhou! O valor do saque deve ser positivo.")
            return False
        if valor > self.saldo:
            print("Operacao falhou! Saldo insuficiente.")
            return False
        if valor > self.LIMITE_SAQUE_VALOR:
            print(f"Operacao falhou! O limite maximo por saque e de R$ {self.LIMITE_SAQUE_VALOR:.2f}.")
            return False
        ok, msg = self._verificar_limite_horario_acumulado(valor, 'saque')
        if not ok:
            print(f"Operacao falhou! {msg}")
            return False
        if self.numero_saques_hoje >= self.LIMITE_SAQUES_DIA:
            print(f"Operacao falhou! Numero maximo de {self.LIMITE_SAQUES_DIA} saques diarios atingido.")
            return False
        self.saldo -= valor
        self.numero_saques_hoje += 1
        self.total_saques_periodo += valor
        self.extrato.append(f"Saque: -R$ {valor:.2f} - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
        return True

    def exibir_extrato(self):
        print("\n" + "=" * 40)
        print(f"EXTRATO - Conta {self.numero} | Agencia {self.AGENCIA}")
        print(f"Cliente: {self.cliente.nome} (CPF: {self.cliente.cpf})")
        print("=" * 40)
        if not self.extrato:
            print("Nenhuma movimentacao registrada.")
        else:
            for linha in self.extrato:
                print(linha)
        print(f"\nSaldo atual: R$ {self.saldo:.2f}")
        print(f"Periodo atual: {self.periodo_atual.upper()}")
        print(f"Total de saques no periodo: R$ {self.total_saques_periodo:.2f}")
        print(f"Total de depositos no periodo: R$ {self.total_depositos_periodo:.2f}")
        print("=" * 40)

# ====================== SISTEMA PRINCIPAL ======================
clientes = {}
contas = {}
proximo_numero_conta = 1
conta_atual = None

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_cpf(cpf: str) -> bool:
    """Valida se o CPF contém apenas números e tem 11 dígitos (opcional)."""
    if not cpf.isdigit():
        print("Erro: CPF deve conter apenas numeros.")
        return False
    if len(cpf) != 11:
        print("Erro: CPF deve ter exatamente 11 digitos.")
        return False
    return True

def validar_nome(nome: str) -> bool:
    """Valida se o nome contém apenas letras, espaços e, opcionalmente, acentos."""
    # Permite letras (incluindo acentuadas), espaços e hífen (para sobrenomes compostos)
    if re.match(r'^[A-Za-zÀ-ÿ\s\-]+$', nome):
        return True
    else:
        print("Erro: Nome deve conter apenas letras, espacos e hifens.")
        return False

def criar_usuario():
    print("\n--- CADASTRO DE NOVO USUARIO ---")
    cpf = input("Informe o CPF (somente numeros, 11 digitos): ").strip()
    if not validar_cpf(cpf):
        return False
    if cpf in clientes:
        print("CPF ja cadastrado!")
        return False

    nome = input("Informe o nome completo: ").strip().upper()
    if not validar_nome(nome):
        return False

    data_nasc = input("Informe a data de nascimento (dd-mm-aaaa): ").strip()
    try:
        datetime.strptime(data_nasc, "%d-%m-%Y")
    except ValueError:
        print("Data invalida! Use o formato dd-mm-aaaa.")
        return False

    endereco = input("Informe o endereco (logradouro, nro - bairro - cidade/sigla estado): ").strip()
    clientes[cpf] = Cliente(cpf, nome, data_nasc, endereco)
    print("Usuario criado com sucesso!")
    return True

def criar_conta():
    print("\n--- CRIACAO DE NOVA CONTA ---")
    cpf = input("Informe o CPF do titular: ").strip()
    if not validar_cpf(cpf):
        return False
    if cpf not in clientes:
        print("CPF nao encontrado! Cadastre o usuario primeiro (opcao 1 no menu inicial).")
        return False
    global proximo_numero_conta
    numero = proximo_numero_conta
    proximo_numero_conta += 1
    conta = Conta(numero, clientes[cpf])
    contas[numero] = conta
    print(f"Conta criada! Agencia: {Conta.AGENCIA} | Numero: {numero}")
    return True

def acessar_conta():
    """Solicita CPF e lista todas as contas do titular para escolha."""
    global conta_atual
    print("\n--- ACESSAR CONTA ---")
    cpf = input("Informe o CPF do titular: ").strip()
    if not validar_cpf(cpf):
        return False
    if cpf not in clientes:
        print("CPF nao encontrado!")
        return False

    contas_do_cpf = []
    for num, conta in contas.items():
        if conta.cliente.cpf == cpf:
            contas_do_cpf.append((num, conta))

    if not contas_do_cpf:
        print(f"O CPF {cpf} nao possui nenhuma conta cadastrada. Crie uma conta primeiro (opcao 2).")
        return False

    if len(contas_do_cpf) == 1:
        numero, conta = contas_do_cpf[0]
        print(f"Unica conta encontrada: {numero}. Acessando automaticamente...")
    else:
        print(f"\nContas encontradas para o CPF {cpf}:")
        for i, (num, conta) in enumerate(contas_do_cpf, 1):
            print(f"  {i} - Conta {num} | Saldo: R$ {conta.saldo:.2f}")
        print("  0 - Cancelar")
        try:
            escolha = int(input("Escolha o numero da conta desejada: "))
            if escolha == 0:
                print("Acesso cancelado.")
                return False
            if escolha < 1 or escolha > len(contas_do_cpf):
                print("Opcao invalida!")
                return False
            numero, conta = contas_do_cpf[escolha - 1]
        except ValueError:
            print("Valor invalido!")
            return False

    conta_atual = conta
    print(f"Acesso concedido. Bem-vindo, {conta_atual.cliente.nome}! (Conta {numero})")
    return True

def listar_contas():
    print("\n--- LISTAGEM DE CONTAS ---")
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for numero, conta in contas.items():
        print(f"Agencia: {Conta.AGENCIA} | Conta: {numero} | Titular: {conta.cliente.nome} (CPF: {conta.cliente.cpf}) | Saldo: R$ {conta.saldo:.2f}")

def menu_bancario():
    """Menu principal apos acessar uma conta."""
    global conta_atual
    while True:
        print("\n" + "=" * 30)
        print(f"   BANCO PYTHON - CONTA {conta_atual.numero}")
        print("=" * 30)
        print("[D] Depositar")
        print("[S] Sacar")
        print("[E] Extrato")
        print("[L] Limites (consultar/alterar)")
        print("[LC] Listar contas")
        print("[Q] Sair da conta")
        print("=" * 30)

        opcao = input("Escolha a opcao: ").strip().upper()

        if opcao == "D":
            try:
                valor = float(input("Informe o valor a depositar: R$ "))
                conta_atual.depositar(valor)
            except ValueError:
                print("Valor invalido!")
        elif opcao == "S":
            try:
                valor = float(input("Informe o valor a sacar: R$ "))
                conta_atual.sacar(valor)
            except ValueError:
                print("Valor invalido!")
        elif opcao == "E":
            conta_atual.exibir_extrato()
        elif opcao == "L":
            ConfiguracaoLimites.menu_configuracao()
        elif opcao == "LC":
            listar_contas()
        elif opcao == "Q":
            print(f"Saindo da conta {conta_atual.numero}. Volte sempre!")
            conta_atual = None
            break
        else:
            print("Opcao invalida! Tente novamente.")

        input("\nPressione Enter para continuar...")
        limpar_tela()

def menu_inicial():
    """Menu inicial com opcoes de cadastro e acesso."""
    while True:
        print("\n" + "=" * 30)
        print("        BANCO PYTHON")
        print("=" * 30)
        print("[1] Novo usuario")
        print("[2] Nova conta")
        if contas:
            print("[3] Acessar conta")
        print("[0] Encerrar sistema")
        print("=" * 30)

        opcao = input("Escolha a opcao: ").strip()

        if opcao == "1":
            criar_usuario()
        elif opcao == "2":
            criar_conta()
        elif opcao == "3" and contas:
            if acessar_conta():
                limpar_tela()
                menu_bancario()
        elif opcao == "0":
            print("Encerrando o sistema bancario. Obrigado por utilizar!")
            break
        else:
            print("Opcao invalida!")

        input("\nPressione Enter para continuar...")
        limpar_tela()

if __name__ == "__main__":
    menu_inicial()