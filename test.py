from typing import Annotated, get_type_hints, get_origin, get_args
from functools import wraps

def check_value_range(func):
    @wraps(func)
    def wrapped(x):
        type_hints = get_type_hints(double, include_extras=True)
        # type_hints é um dicionário que contém os tipos de dados dos parâmetros e do retorno da função
        #print(type_hints)
        hint = type_hints['x']
        if get_origin(hint) is Annotated:
            hint_type, *hint_args = get_args(hint)
            low, high = hint_args[0]
            
            if not low <= x <= high:
                raise ValueError(f"x must be between {low} and {high}, got {x}")
            # se a validação passar, chama a função original
        return func(x)

    return wrapped

## víd 6
# usas annotations para incluir metadata sobre os typeHints
# neste exemplo estamos a definir que o valor de x deve ser um inteiro entre 0 e 100
# no entanto isto não é uma validação, é apenas uma anotação, não há nenhuma obrigação de seguir este padrão

# no início podes fazer assim, mas é bue código. A func deve preocupar-se apenas
# com a lógica de negócio, e não com a validação dos dados
# por isso vais passar toda a parte de validação para um decorator
"""def double(x : Annotated[int, (0,100)]) -> int:
    
    type_hints = get_type_hints(double, include_extras=True)
    # type_hints é um dicionário que contém os tipos de dados dos parâmetros e do retorno da função
    #print(type_hints)
    hint = type_hints['x']
    if get_origin(hint) is Annotated:
        hint_type, *hint_args = get_args(hint)
        low, high = hint_args[0]
        
        if not low <= x <= high:
            raise ValueError(f"x must be between {low} and {high}, got {x}")
    return x * 2    """

@check_value_range
def double(x: Annotated[int, (0,1000)]) -> int:
    
    return x*2

result = double(500)
print(result)