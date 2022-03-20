def title(msg, border_length):
    msg_length = len(msg)
    line(border_length, '=')
    print(f'{msg:<{msg_length}}')
    line(border_length, '=')


def line(line_length, msg='-'):
    print(f'{msg}'*line_length)


def validated_input(msg, value_type=int, sep_line=False):
    value = 0
    while value == 0:
        try:
            value = value_type(input(msg))
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
