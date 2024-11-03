import pandas as pd
import os
import random
import string

def gerar_senha(tamanho=12, usar_maiusculas=True, usar_numeros=True, usar_simbolos=True):
    caracteres = string.ascii_lowercase
    if usar_maiusculas:
        caracteres += string.ascii_uppercase
    if usar_numeros:
        caracteres += string.digits
    if usar_simbolos:
        caracteres += string.punctuation
    senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return senha

def salvar_senhas(df, arquivo='senhas.csv'):
    df.to_csv(arquivo, index=False)

def carregar_senhas(arquivo='senhas.csv'):
    if os.path.exists(arquivo):
        df = pd.read_csv(arquivo)
        df['Senha'] = df['Senha'].astype(str)  # Garantir que a coluna de senhas é tratada como string
        return df
    return pd.DataFrame(columns=['Nome', 'Senha'])

def adicionar_senha(df):
    nome = input("Nome da conta: ")
    tamanho = int(input("Digite o tamanho da senha: "))
    usar_maiusculas = input("Incluir letras maiúsculas? (s/n): ").lower() == 's'
    usar_numeros = input("Incluir números? (s/n): ").lower() == 's'
    usar_simbolos = input("Incluir símbolos? (s/n): ").lower() == 's'
    senha = gerar_senha(tamanho, usar_maiusculas, usar_numeros, usar_simbolos)
    nova_linha = pd.DataFrame({'Nome': [nome], 'Senha': [senha]})
    df = pd.concat([df, nova_linha], ignore_index=True)
    print(f"Senha para {nome} gerada e salva com sucesso.")
    return df

def visualizar_senhas(df):
    if df.empty:
        print("Nenhuma senha armazenada.")
    else:
        print(df[['Nome', 'Senha']])

def editar_senha(df):
    nome = input("Nome da conta para editar a senha: ")
    if nome in df['Nome'].values:
        tamanho = int(input("Digite o tamanho da nova senha: "))
        usar_maiusculas = input("Incluir letras maiúsculas? (s/n): ").lower() == 's'
        usar_numeros = input("Incluir números? (s/n): ").lower() == 's'
        usar_simbolos = input("Incluir símbolos? (s/n): ").lower() == 's'
        nova_senha = gerar_senha(tamanho, usar_maiusculas, usar_numeros, usar_simbolos)
        df.loc[df['Nome'] == nome, 'Senha'] = nova_senha
        print(f"Senha para {nome} atualizada com sucesso.")
    else:
        print("Conta não encontrada.")
    return df

def excluir_senha(df):
    nome = input("Nome da conta para excluir a senha: ")
    if nome in df['Nome'].values:
        df = df[df['Nome'] != nome]
        print(f"Senha para {nome} excluída com sucesso.")
    else:
        print("Conta não encontrada.")
    return df

def avaliar_forca_senha(senha):
    senha = str(senha)  # Garantir que a senha seja tratada como string
    comprimento = len(senha)
    tem_maiusculas = any(c.isupper() for c in senha)
    tem_minusculas = any(c.islower() for c in senha)
    tem_numeros = any(c.isdigit() for c in senha)
    tem_simbolos = any(c in string.punctuation for c in senha)
    
    pontuacao = 0
    if comprimento >= 8:
        pontuacao += 1
    if tem_maiusculas:
        pontuacao += 1
    if tem_minusculas:
        pontuacao += 1
    if tem_numeros:
        pontuacao += 1
    if tem_simbolos:
        pontuacao += 1
    
    return pontuacao / 5  # Retorna a pontuação em forma de porcentagem

def relatorio_seguranca(df):
    if df.empty:
        print("Nenhuma senha armazenada para gerar um relatório de segurança.")
        return
    
    df['Seguranca'] = df['Senha'].apply(avaliar_forca_senha)
    df['Classificacao'] = df['Seguranca'].apply(lambda x: 'Fraca' if x <= 0.3 else 'Média' if x <= 0.6 else 'Forte')

    print("\nRelatório de Segurança das Senhas:")
    for index, row in df.iterrows():
        nome = row['Nome']
        senha = row['Senha']
        classificacao = row['Classificacao']
        seguranca = row['Seguranca'] * 100  # Transformar em porcentagem
        print(f"Conta: {nome} | Senha: {senha} | Força: {classificacao} ({seguranca:.1f}%)")

    print("\nRecomendações:")
    print(" - Senhas fortes têm pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e símbolos.")
    print(" - Considere atualizar as senhas classificadas como 'Fraca' ou 'Média'.")

def menu():
    df = carregar_senhas()
    while True:
        print("\nMenu:")
        print("1. Adicionar senha")
        print("2. Visualizar senhas")
        print("3. Editar senha")
        print("4. Excluir senha")
        print("5. Relatório de Segurança")
        print("6. Sair")
        escolha = input("Escolha uma opção (1-6): ")
        if escolha == '1':
            df = adicionar_senha(df)
        elif escolha == '2':
            visualizar_senhas(df)
        elif escolha == '3':
            df = editar_senha(df)
        elif escolha == '4':
            df = excluir_senha(df)
        elif escolha == '5':
            relatorio_seguranca(df)
        elif escolha == '6':
            salvar_senhas(df)
            print("Saindo e salvando senhas.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()






