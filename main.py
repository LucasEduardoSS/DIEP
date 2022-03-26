# Programa Pré-definições do circuito NBR 5410

# IMPORTAÇÕES
from time import sleep
from functions import title, line, validated_input, calculate_current
from tabelas import tabela_36, tabela_42, disjuntores, materiais

# DECLARAÇÕES
fcc = is_enough = user_choice = is_to_continue = cond_crg = corrente = cccfc = resistencia = 0
cond_min_index = 0


def var_status():
    print('\n<VARIABLES STATUS>')
    print(f'fator de correção de condução: {fcc:.2f}')


# CÓDIGO PRINCIPAL
title(" Programa pré-definições do circuito ", 102)

while True:
    # Menu Principal
    print('''Selecione uma das opções:

\33[33m1 - Dimensionar o Condutor
\33[36m2 - Cálculo da STMC Contra Quedas de Tensão
\33[33m3 - Determinação do Disjuntor
\33[36m4 - Finalizar Programa\33[m
''')

    user_choice = validated_input('Digite aqui: ')

    '''
    DIMENSIONAMENTO DO CABO
    
    Nessa sessão é dimensionado o código a partir de cálculos utilizando
    tabelas presentes na nbr 5410, incluindo correções de capacidade de
    condução de corrente pelos condutores.
    '''

    if user_choice == 1:
        title(" Dimensionamento do condutor ", 102)

        # Decide se o circuito é de força ou de luz
        circuito = str(input('Luz ou Força? ')).strip().upper()[0]

        # Menu Tipo de Circuito
        print('-' * 102, '''\nInforme o tipo de circuito:

\33[33m1 - Monofásico a dois condutores
\33[36m2 - Monofásico a três condutores
\33[33m3 - Bifásico sem neutro
\33[36m4 - Bifásico com neutro
\33[33m5 - Trifásico sem neutro
\33[36m6 - Trifásico com neutro\33[m
''')

        tipo_circ = int(input('Digite aqui: '))
        line(102)

        if tipo_circ in [1, 2, 3]:
            cond_crg = 2

        elif tipo_circ in [4, 5, 6]:
            cond_crg = 3

        # Recebe o valor da corrente do circuito
        corrente = float(input('Corrente do Circuito, se não tiver, digite 0: '))
        line(102)

        # Calcula a corrente caso ela não seja informada pelo usuário
        if corrente == 0:
            corrente = calculate_current()

        # Menu Referência do método de condicionamento do circuito conforme tabela 33
        print('''Indique o método de referência conforme tabela 33:

\33[33m7 - Condutores isolados ou cabos unipolares em eletroduto de
seção circular embutido em alvenaria - B1\33[m
''')

        metodo_de_referencia = int(input('Digite aqui: '))
        line(102)

        if metodo_de_referencia == 7:
            red_met_index = 2

        # Recebe o número de circuitos instalados no conduíte em questão
        qnt_circuitos = int(input('Quantidade de circuitos presente no conduite: '))

        # Menu Métodos de Agrupamento / Tabela 42
        print('-' * 102, '''\nForma de agrupamento dos condutores segundo a tabela 42 da nbr 5410:

\33[33m1 - Em feixe: ao ar livre ou sobre superfície; embutido; em conduto fechado
\33[36m2 - Camada única sobre parede, piso, ou em bandeja não perfurada ou prateleira
\33[33m3 - Camada única no teto
\33[36m4 - Camada única em bandeja perfurada
\33[33m5 - Camada única sobre leito, suporte etc\33[m
''')

        ref_agrupamento = int(input('Digite aqui: '))

        fcc = tabela_42[ref_agrupamento - 1][qnt_circuitos - 1]

        var_status()

        line(102)

        if circuito == 'L':
            cond_min_index = 3
        elif circuito == 'F':
            cond_min_index = 4

        # Dimensiona o condutor
        for pos, condutor in enumerate(tabela_36[f'CCC{cond_crg}'][cond_min_index:]):
            cccfc = condutor * fcc
            if corrente <= cccfc:
                print(f'O condutor de {tabela_36["Cond"][pos + cond_min_index]} mm^2 ', end='')
                print(f'é capaz de alimentar este circuito.')
                print(f'Sua capacidade de condução corrigida é de {cccfc:.2f}A.')
                line(102)
                break

    '''
    CALCULO SESSÃO TRANSVERSAL MÍNIMA DO CONDUTOR
    
    Calcula a sessão transversal mínima de um condutor para circuito
    com o uso de referência de tabelas da nbr 5410 e fórmulas
    matemáticas apresentadas em vídeos tutoriais.
    '''

    if user_choice == 2:
        title(" I  Sessão transversal do condutor para quedas de tensão  I ", 102)
        print(
            '''
        ATENÇÃO
        
        Recomenda-se o uso desta função para dimensionar circuitos de alta tensão,
        como aqueles utilizados em oficinas, grandes edificações, centros de pesquisa, etc.
        '''
        )

        # Escolhe se será usada a corrente calculada
        if cccfc != 0:
            is_to_continue = validated_input('Deseja utilizar as corrente dos cálculos anteriores? ', str, True)

            if is_to_continue == 'N':
                corrente = validated_input('Informe a nova corrente do circuito : ', float, True)
                cccfc = validated_input('Informe a nova capacidade de condução corrigida: ', float, True)

            elif is_to_continue == 'S':
                print('Com base na corrente informada nos cálculos anteriores,\n', end='')

        # Recebe a corrente do circuito
        if corrente == 0:
            corrente = float(input('Informe a corrente do circuito: '))
            line(102)

        print('''Informe o comprimento do circuito em metros. Em caso de circuito ramificado
leve em conta aquele com maior valor.
''')

        # Recebe o valor do comprimento, material condutor e tensão do circuito
        distancia = validated_input('Comprimento: ', float, True)
        material_condutor = validated_input('Material do condutor [ Cobre / Alumínio / Ouro ]: ', str, True)
        tensao = validated_input('Informe o valor da tensão do circuito: ', int, True)

        for pos, material in enumerate(materiais['Nome']):
            if material_condutor == material:
                resistencia = materiais['Resistências'][pos]

        s = ((resistencia * distancia * corrente * 2) / (4 * tensao)) * 100

        print('A sessão transversal mínima para este cabo é de {:.3f} mm^2'.format(s))
        line(102)

    '''
    DIMENSIONADOR DE DISJUNTOR
    
    Dimensiona a corrente do disjuntor necessário para proteção do
    circuito trabalhado, sendo que este deve ter uma corrente maior
    que a capacidade de condução de corrente do circuito com fator de
    correção.
    '''

    if user_choice == 3:
        title(" Determinação do disjuntor / Linha Easy9 Schneider ", 102)

        # Escolhe se será usada a corrente calculada
        if cccfc != 0:
            is_to_continue = validated_input('Deseja utilizar as corrente dos cálculos anteriores? ', str, True)

            if is_to_continue == 'N':
                corrente = validated_input('Nova corrente do circuito: ', float, True)
                cccfc = validated_input('Nova capacidade de condução corrigida: ', float)

            elif is_to_continue == 'S':
                print('Com base na corrente informada nos cálculos anteriores,\n', end='')

        # Dimensiona o disjuntor
        for disjuntor in disjuntores:
            if corrente <= disjuntor <= cccfc:
                print(f'O disjuntor de {disjuntor}A é o ideal para este circuito.')

            else:
                print('Não há disjuntor disponível para este circuito.')

    # Encerra o programa
    elif user_choice == 4:
        break

    elif user_choice not in [1, 2, 3, 4]:
        print('Comando inválido. tente novamente.')

print('Finalizando o programa...'), sleep(1)
print('Programa Finalizado.')
