# Programa Pré-definições do circuito NBR 5410

# IMPORTAÇÕES
from time import sleep
from functions import title, line, validated_input
from tabelas import metodo

# DECLARAÇÕES
fca = fcc = fct = f = k = h = corrente = cccfc = resistencia = 0
condutores = [
    {'Bitola': '1.5 mm', 'Cap. Condução': 17.5},
    {'Bitola': '2.5 mm', 'Cap. Condução': 24},
    {'Bitola': '4 mm', 'Cap. Condução': 32},
    {'Bitola': '6 mm', 'Cap. Condução': 41},
    {'Bitola': '10 mm', 'Cap. Condução': 57},
    {'Bitola': '16 mm', 'Cap. Condução': 76}
]

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

    k = validated_input('Digite aqui: ')

    '''
    DIMENSIONAMENTO DO CABO
    
    Nessa sessão é dimensionado o código a partir de cálculos utilizando
    tabelas presentes na nbr 5410, incluindo correções de capacidade de
    condução de corrente pelos condutores.
    '''

    if k == 1:
        title(" Dimensionamento do condutor ", 102)

        # sessão onde é informado se é um circuito de luz ou força
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

        tipo_circuito = int(input('Digite aqui: '))
        line(102)

        # Recebe o valor da corrente do circuito
        corrente = float(input('Corrente do Circuito, se não tiver, digite 0: '))
        line(102)

        # Calcula a corrente caso ela não seja informada pelo usuário
        if corrente == 0:
            potencia = float(input('Informe a potência do(s) aparelho(s): '))
            tensao = float(input('Informe a tensão do(s) aparelho(s): '))
            print(f'A corrente do circuito é de {potencia / tensao:.2f}A.')
            corrente = potencia / tensao
            line(102)

        # Menu Referência do método de condicionamento do circuito conforme tabela 33
        print('''Indique o método de referência conforme tabela 33:

\33[33m7 - Condutores isolados ou cabos unipolares em eletroduto de
seção circular embutido em alvenaria - B1\33[m
''')

        metodo_de_referencia = int(input('Digite aqui: '))
        line(102)

        if metodo_de_referencia == 7:
            temp = int(input('Informe a temperatura ambiente em °C (padrão 35°C): '))

            if temp == 35:
                line(102)
                material = str(
                    input('Informe qual o material usado no revestimento dos condutores [PVC/EPR ou XLPE]: ')
                )

                if material == 'P'.strip().upper()[0]:
                    fct = 0.94

            # Sessão onde o usuário informa o número de circuitos instalados no conduíte em questão

            line(102)
            qnt_circuitos = int(input('Informe a quantidade de circuitos presente no conduite : '))

            if qnt_circuitos > 5:  # Alteração do número de circuitos do conduíte
                print('Recomenda-se utilizar no máximo 5 circuitos por conduíte')
                opcao = str(input('Deseja alterar a quantidade? ')).strip()[0]

                if opcao in 'Ss':  # Condição de alteração do número de circuitos no conduíte
                    qnt_circuitos = int(input('Informe uma nova quantidade de circuitos presentes no conduite: '))

            # Menu Métodos de Agrupamento / Tabela 42
            print('-' * 102, '''\nForma de agrupamento dos condutores segundo a tabela 42 da nbr 5410:

\33[33m1 - Em feixe: ao ar livre ou sobre superfície; embutido; em conduto fechado
\33[36m2 - Camada única sobre parede, piso, ou em bandeja não perfurada ou prateleira
\33[33m3 - Camada única no teto
\33[36m4 - Camada única em bandeja perfurada
\33[33m5 - Camada única sobre leito, suporte etc\33[m
''')

            ref = int(input('Digite aqui: '))

            cr_factor = (1, 0.8, 0.7, 0.65, 0.6)
            fca = cr_factor[ref - 1]
            fcc = fct * fca  # Operação que obtém o fator de correção do circuito

            line(102)

            # DIMENSIONAMENTO DE CIRCUITO DE LUZ

            if circuito == 'L':

                if tipo_circuito == 1 or 2 or 3:
                    # ccc significa capacidade de condução do condutor em empares, no caso um condutor de 1,5 mm
                    ccc = 17.5
                    cccfc = ccc * fcc
                    print(
                        'A capacidade de condução de corrente do circuito de 1,5 mm^2'
                        f' com o fator de correção é de {cccfc:.2f}A'
                    )

                    if corrente <= cccfc:
                        print('O cabo de 1.5 mm^2 é capaz de alimentar este circuito')
                        f = 1

                    else:
                        print('o cabo de 1.5 mm^2 não capaz de alimentar este circuito')
                        f = 0

                        # Sessão para determinar o condutor caso o mínimo não seja o suficiente

                        while f == 0:
                            # Menu Condutores
                            print('-' * 102, '''\nIndique uma sessão maior :

a - 2,5 mm^2
b - 4 mm^2
c - 6 mm^2
d - 10 mm^2
                            ''')

                            s = str(input('Digite aqui : ')).strip().lower()[0]
                            line(102)

                            if s == 'a':
                                cccfc = 24 * fcc
                                print(
                                    'A capacidade de condução de corrente do circuito de 2,5 mm^2'
                                    f' com o fator de correção é de {cccfc:.2f}A'
                                )

                            elif s == 'b':
                                cccfc = 32 * fcc
                                print('A capacidade de condução de corrente do circuito de '
                                      f'4 mm^2 com o fator de correção é de {cccfc:.2f}A')

                            elif s == 'c':
                                cccfc = 41 * fcc
                                print('A capacidade de condução de corrente do circuito de '
                                      f'6 mm^2 com o fator de correção é de {cccfc:.2f}A')

                            elif s == 'd':
                                cccfc = 57 * fcc
                                print('A capacidade de condução de corrente do circuito de '
                                      f'10 mm^2 com o fator de correção é de {cccfc:.2f}A')

                            if cccfc < corrente:
                                print('Este cabo não é capaz de suportar a corrente do circuito.')
                                line(102)
                                f = 0

                            else:
                                f = 1
                        print('Este cabo é capaz de suportar a corrente.')
                        line(102)

            # Sessão para determinar a dimensão do condutor caso o circuito seja de força

            if circuito == 'F':
                if tipo_circuito == 1 or 2 or 3:
                    ccc = 24
                    cccfc = ccc * fcc
                    print(
                        'A capacidade de condução de corrente do condutor de 2,5 mm^2'
                        f' com o fator de correção é de {cccfc:.2f}A'
                    )

                    if corrente <= cccfc:
                        print('O cabo de 2,5 mm^2 é capaz de alimentar este circuito')
                        f = 1

                    else:
                        print('o cabo de 2,5 mm^2 não capaz de alimentar este circuito')
                        line(102)
                        f = 0

                        while f == 0:
                            # Menu Condutores
                            print('''Indique uma sessão maior :

A - 4 mm^2
B - 6 mm^2
C - 10 mm^2
D - 16 mm^2
                            ''')

                            s = str(input('Digite aqui : ')).strip().lower()[0]
                            line(102)

                            if s == 'a':
                                cccfc = fcc * 32
                                print(
                                    'A capacidade de condução de corrente do circuito de 4 mm^2'
                                    f'com o fator de correção é de {cccfc:.2f}A.')

                            if s == 'b':
                                cccfc = fcc * 41
                                print(
                                    'A capacidade de condução de corrente do circuito de 6 mm^2'
                                    f' com o fator de correção é de {cccfc:.2f}A')

                            if s == 'c':
                                cccfc = fcc * 57
                                print(
                                    'A capacidade de condução de corrente do circuito de 10 mm^2'
                                    f'com o fator de correção é de {cccfc:.2f}A.')

                            if s == 'd':
                                cccfc = fcc * 76
                                print(
                                    'A capacidade de condução de corrente do circuito de 16 mm^2'
                                    f' com o fator de correção é de {cccfc:.2f}A.')

                            if s not in 'abcd':
                                print('Comando inválido. tente novamente.')
                                f = 0

                            if cccfc < corrente:
                                print('Este cabo não é capaz de suportar a corrente do circuito.')
                                print('-' * 102)
                                f = 0

                            else:
                                f = 1

                        print('Este cabo é capaz de suportar a corrente')
                        line(102)

    '''
    CALCULO SESSÃO TRANSVERSAL MÍNIMA DO CONDUTOR
    
    Calcula a sessão transversal mínima de um condutor para circuito
    com o uso de referência de tabelas da nbr 5410 e fórmulas
    matemáticas apresentadas em vídeos tutoriais.
    '''

    if k == 2:
        title(" I  Sessão transversal do condutor para quedas de tensão  I ", 102)

        if corrente != 0 and cccfc != 0:

            while h == 0:
                h = str(input('Deseja utilizar as corrente dos cálculos anteriores? ')).strip().upper()[0]
                line(102)

                if h == 'S':
                    print('Com base nas correntes informada nos cálculos anteriores,')
                    line(102)

                # Calcula a corrente caso o usuário não a tenha
                elif h == 'N':
                    corrente = float(input('Informe a nova corrente do circuito : '))
                    line(102)
                    cccfc = float(input(
                        'Informe a nova capacidade de condução de corrente dos condutores com fator de correção : '))
                    line(102)

                else:
                    print('Comando inválido, tente novamente.')
                    line(102)
                    h = 0

        if corrente == 0:
            corrente = float(input('Informe a corrente do circuito : '))
            line(102)

        distancia = float(input('Informe o comprimento do circuito em metros.'
                                'Em caso de circuito ramificado, leve em conta a ramificação mais longa : '))
        line(102)

        material_condutor = str(input('Informe o material do condutor [ Cobre / Alumínio / Ouro ] : ')).strip().upper()[
            0]
        line(102)

        tensao = float(input('Informe o valor da tensão do circuito : '))
        line(102)

        if material_condutor == 'C':
            resistencia = 0.0172

        elif material_condutor == 'A':
            resistencia = 0.0282

        elif material_condutor == 'O':
            resistencia = 0.0244

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

    if k == 3:
        title(" I  Determinação do disjuntor / Linha Easy9 Schneider I ", 102)

        if corrente != 0 and cccfc != 0:

            while True:
                h = str(input('Deseja utilizar as corrente dos cálculos anteriores? ')).strip().upper()[0]
                line(102)

                if h == 'S':
                    print('Com base na corrente informada nos cálculos anteriores,', end='')
                    break

                elif h == 'N':
                    corrente = float(input('Informe a nova corrente do circuito : '))
                    line(102)
                    cccfc = float(input(
                        'Informe a nova capacidade de condução de corrente dos condutores com fator de correção : '))
                    line(102)
                    break

                else:
                    print('Comando inválido, tente novamente.')
                    line(102)
            h = 0

        elif corrente == 0 and cccfc == 0:
            corrente = float(input('Informe a corrente do circuito : '))
            line(102)
            cccfc = float(input('Informe a capacidade de condução de corrente dos condutores com fator de correção : '))
            line(102)

        if corrente <= 2 <= cccfc:
            print('O disjuntor de 2A é o ideal para este circuito.')

        elif corrente <= 4 <= cccfc:
            print('O disjuntor de 4A é o ideal para este circuito.')

        elif corrente <= 6 <= cccfc:
            print('O disjuntor de 6A é o ideal para este circuito.')

        elif corrente <= 10 <= cccfc:
            print('O disjuntor de 10A é o ideal para este circuito.')

        elif corrente <= 16 <= cccfc:
            print('O disjuntor de 16A é o ideal para este circuito.')

        elif corrente <= 20 <= cccfc:
            print('O disjuntor de 20A é o ideal para este circuito.')

        elif corrente <= 25 <= cccfc:
            print('O disjuntor de 25A é o ideal para este circuito.')

        elif corrente <= 32 <= cccfc:
            print('O disjuntor de 32A é o ideal para este circuito.')

        elif corrente <= 40 <= cccfc:
            print('O disjuntor de 40A é o ideal para este circuito.')

        elif corrente <= 50 <= cccfc:
            print('O disjuntor de 50A é o ideal para este circuito.')

        elif corrente > cccfc:
            print('Este condutor não é capaz de alimentar o circuito ')

        line(102)

    # Encerra o programa
    elif k == 4:
        break

    else:
        print('Comando inválido. tente novamente.')

print('Finalizando o programa...'), sleep(1)
print('Programa Finalizado.')
