def title(msg, border_length):
    msg_length = len(msg)
    line(border_length, '=')
    print(f'{msg:<{msg_length}}')
    line(border_length, '=')


def line(line_length, msg='-'):
    print(f'{msg}'*line_length)


def validated_input(msg, value_type=int, sep_line=False):
    """
    Valida um input corrigindo possíveis erros. Pode receber todos os tipos de valores.
    :param msg: mensagem apresentada ao usuário.
    :param value_type: tipo de valor a ser validado.
    :param sep_line: escreve uma linha de separação.
    :return: retorna o valor do usuário para a variável.
    """

    value = 0
    while value == 0:
        try:
            value = value_type(input(msg))
            if value_type == str:
                value = str(value).strip().upper()[0]
        except ValueError:
            print('\33[31mValor incorreto! tente novamente.\33[m')
        except TypeError:
            print('\33[31mTipo de valor incorreto! tente novamente.\33[m')
    if sep_line:
        line(102)
    return value


def value_limit(min_limit, max_limit, value, msg):
    while max_limit < value < min_limit:
        validated_input(msg)


def calculate_current():
    potencia = float(validated_input('Informe a potência do(s) aparelho(s): '))
    tensao = float(validated_input('Tensão do circuito: '))
    print(f'A corrente do circuito é de {potencia / tensao:.2f}A.')
    corrente = potencia / tensao
    line(102)
    return corrente


def get_current():
    corrente = validated_input('Corrente do circuito')
