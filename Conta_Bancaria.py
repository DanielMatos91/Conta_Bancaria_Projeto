from datetime import datetime

menu = """
[c] Cadastrar Novo Usuário
[l] Listar Usuários
[d] Depositar
[s] Sacar
[e] Extrato
[a] Criar Conta Corrente
[b] Listar Contas
[q] Sair

=> """

# Variáveis globais
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
usuarios = []
contas = []
numero_conta_sequencial = 1
AGENCIA = "0001"

def criar_usuario():
    """Cadastra um novo usuário no sistema"""
    print("\n--- Cadastro de Novo Usuário ---")
    
    nome = input("Nome completo: ").strip()
    
    while True:
        data_nasc = input("Data de nascimento (DD/MM/AAAA): ").strip()
        try:
            datetime.strptime(data_nasc, '%d/%m/%Y')
            break
        except ValueError:
            print("Formato inválido! Use DD/MM/AAAA")
    
    while True:
        cpf = input("CPF (apenas números): ").strip()
        if not cpf.isdigit():
            print("CPF deve conter apenas números!")
            continue
            
        if any(usuario['cpf'] == cpf for usuario in usuarios):
            print("Erro: CPF já cadastrado!")
        else:
            break
    
    print("\n--- Endereço ---")
    logradouro = input("Logradouro (Rua/Av.): ").strip()
    numero = input("Número: ").strip()
    cidade = input("Cidade: ").strip()
    uf = input("UF (Sigla): ").strip().upper()
    
    endereco = f"{logradouro}, {numero} - {cidade}/{uf}"
    
    usuario = {
        'nome': nome,
        'data_nascimento': data_nasc,
        'cpf': cpf,
        'endereco': endereco
    }
    
    usuarios.append(usuario)
    print("\nUsuário cadastrado com sucesso!")
    return usuario

def listar_usuarios():
    """Lista todos os usuários cadastrados"""
    print("\n--- Lista de Usuários Cadastrados ---")
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    
    for i, usuario in enumerate(usuarios, 1):
        print(f"\nUsuário {i}:")
        print(f"Nome: {usuario['nome']}")
        print(f"Data de Nascimento: {usuario['data_nascimento']}")
        print(f"CPF: {usuario['cpf']}")
        print(f"Endereço: {usuario['endereco']}")

def criar_conta_corrente(usuario):
    """Cria uma nova conta corrente para o usuário especificado"""
    global numero_conta_sequencial, contas
    
    if not usuario or not isinstance(usuario, dict) or 'cpf' not in usuario:
        print("Erro: Usuário inválido para criação de conta")
        return None
    
    nova_conta = {
        'agencia': AGENCIA,
        'numero_conta': numero_conta_sequencial,
        'usuario': usuario
    }
    
    numero_conta_sequencial += 1
    contas.append(nova_conta)
    
    print(f"\nConta criada com sucesso! Número: {nova_conta['numero_conta']}")
    return nova_conta

def listar_contas():
    """Lista todas as contas correntes cadastradas"""
    print("\n=== Lista de Contas Correntes ===")
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    
    for conta in contas:
        print(f"\nAgência: {conta['agencia']}")
        print(f"Número: {conta['numero_conta']}")
        print(f"Titular: {conta['usuario']['nome']}")
        print(f"CPF: {conta['usuario']['cpf']}")

def depositar(saldo, valor, extrato):
    """Realiza um depósito na conta"""
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\nDepósito realizado com sucesso!")
    else:
        print("\nOperação falhou! O valor informado é inválido.")
    
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    """Realiza um saque da conta"""
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("\nOperação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("\nOperação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("\nOperação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\nSaque realizado com sucesso!")
    else:
        print("\nOperação falhou! O valor informado é inválido.")
    
    return saldo, extrato, numero_saques

def mostrar_extrato(saldo, extrato):
    """Exibe o extrato bancário"""
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

# Sistema principal
while True:
    opcao = input(menu).strip().lower()

    if opcao == "c":
        criar_usuario()

    elif opcao == "l":
        listar_usuarios()

    elif opcao == "a":
        if not usuarios:
            print("\nErro: É necessário cadastrar um usuário primeiro!")
        else:
            # Usa o último usuário cadastrado por padrão
            criar_conta_corrente(usuarios[-1])

    elif opcao == "b":
        listar_contas()

    elif opcao == "d":
        try:
            valor = float(input("\nInforme o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
        except ValueError:
            print("\nErro: Valor inválido! Digite um número.")

    elif opcao == "s":
        try:
            valor = float(input("\nInforme o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                LIMITE_SAQUES=LIMITE_SAQUES
            )
        except ValueError:
            print("\nErro: Valor inválido! Digite um número.")

    elif opcao == "e":
        mostrar_extrato(saldo, extrato)

    elif opcao == "q":
        print("\nSaindo do sistema...")
        break

    else:
        print("\nOperação inválida! Por favor, selecione novamente a operação desejada.")