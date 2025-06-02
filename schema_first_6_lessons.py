from enum import Enum
# enum é uma classe que permite definir um conjunto de valores constantes
# é útil para definir qualquer tipo de valor que não muda, como os géneros das bandas
# dos quais o utilizador pode escolher
# isto reduz a carga sobre o servidor, pois o FastAPI não tem de verificar se o género é válido
from pydantic import BaseModel
# Pydantic é uma biblioteca que o FastAPI usa para validar os dados de entrada
# é diferente de emun, pois nao se preocupa com a validação de possibilidades que uma var pode ter,
# mas sim com a validação de tipos de dados e estruturas de dados
# podes combiná-los e usar Enum dentro de Pydantic para validar os dados de entrada
from datetime import date
from pydantic import validator


class GenreURLchoices(Enum):
    ROCK = 'rock'
    GRUNGE = 'grunge'
    METAL = 'metal'
    PROGRESSIVE_ROCK = 'progressive rock'
    PUNK = 'punk'
    
class Genrechoices(Enum):
    ROCK = 'Rock'
    GRUNGE = 'Grunge'
    METAL = 'Metal'
    PROGRESSIVE_ROCK = 'Progressive Rock'
    PUNK = 'Punk'

class Album(BaseModel):
    title : str
    release_date : date

"""class Band(BaseModel):
    #{'id': 1, 'name': 'The Beatles','genre': 'Rock'},
    id : int
    name : str
    # nao podes usar Enum aqui pq aqui Rock pode ser upper case,
    # terias de definir o Enum com todas as possibilidades de upper e lower case
    genre : str
    # por defeito é uma lista vazia, mas podes passar uma lista de álbuns
    albuns : list[Album] = []"""
    
# Vid 5: Para integrar post requests tens de mudar a class Band, isto pq o id é atribuído pelo servidor (normalmente pela base de dados)

class BandBase(BaseModel):
    name : str
    genre : Genrechoices
    albuns : list[Album] = []

class BandCreate(BandBase):
    # vamos adicionar um Validator para converter o genre 
    # para title case, antes das validações do Pydantic correrem
    # pre = True significa que este validator vai correr antes das validações do Pydantic
    @validator('genre', pre=True)
    def genre_to_title_case(cls, value):
        return value.title() # rock -> Rock

class BandWithID(BandBase):
    id : int
