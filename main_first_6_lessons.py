from fastapi import FastAPI, HTTPException, Path,Query
from schema_first_6_lessons import *
from typing import Annotated

#activar o ambiente virtual
# .\venv-fastapi\Scripts\activate
app = FastAPI()

Bands = [
    {'id': 1, 'name': 'The Beatles','genre': 'Rock'},
    {'id': 2, 'name': 'Nirvana', 'genre': 'Grunge'},
    {'id': 3, 'name': 'Queen', 'genre': 'Rock', 'albuns': [
        {'title': 'A Night at the Opera', 'release_date': '1975-11-21'},
        {'title': 'The Game', 'release_date': '1980-06-30'}
    ]},
    {'id': 4, 'name': 'Metallica', 'genre': 'Metal'},
    {'id': 5, 'name': 'Pink Floyd', 'genre': 'Progressive Rock'}
]

# isto é um route, ou se quiseres, um endpoint (get,put,post,delete)
#'/' é o caminho para o root path
@app.get('/')
#defines a função como index pq é a que vai ter ao caminho da root
# a maioria das vezes, o nome da função é irrelevante, mas é uma boa prática usar nomes descritivos
# as api packages usam type hints para definir o tipo de retorno da função, por isso é boa prática usar type hints (e.g. -> dict)
async def index() -> dict[str, str]:
    return {'message': 'Hello World'}


#uvicorn main:app --reload
# usas isto para criar um servidor assíncrono
# reload é útil para desenvolvimento, para que o servidor reinicie sempre que houver alterações no código
# mas reaload não é recomendado para produção, pois pode causar problemas de desempenho por usar demasiados recursos
# para produção, deves usar um servidor como o gunicorn ou o uvicorn com o --workers

@app.get('/about')
async def about() -> dict[str, str]:
    return {'message': 'This is a simple FastAPI application.'}


# se fores ao url da root e adicionares /docs, vais ver a documentação automática da API
# foi essa doc que o Fernando nos mostrou no vídeo


## Vid 2
"""@app.get('/all_bands')
async def get_all_bands() -> list[Band]:
    # para cada banda na tua base de dados vais passar 
    # cada k:v pair para o construtor da classe Band
    # o constructor vai verificar se os dados estão corretos
    # e se estiverem, vai criar um objeto Band com esses dados
    # se vires os docs já tens info sobre o que é que cada endpoint aceita e retorna
    return [
        Band(**b) for b in Bands
    ]"""

"""@app.get('/bands/{id}', status_code = 200)
async def get_band(id : int) -> Band:
    
    band_to_return = None
    for band in Bands:
        if band['id'] == int(id):
            band_to_return = Band(**band)
    
    # se não encontrar a banda, retorna um erro 404
    # 404 é o código de erro para "Not Found"
    # HTTPException é uma exceção que o FastAPI usa para retornar erros HTTP
    if band_to_return is None:
        raise HTTPException(status_code = 404, detail="Band not found")
    else:
        return band_to_return"""
    
 
# ao meteres que o genre é do tipo GenreURLchoices, o FastAPI vai validar automaticamente o género
# se o género não for válido, o FastAPI vai retornar um erro 422 e não chegará a chamar a função
# 422 é o código de erro para "Unprocessable Entity", ou seja, a entidade não pode ser processada
# isto reduz o número de chamadas à função e consequentemente a uma possível base de dados, melhorando a eficiência da API   
"""
@app.get('/bands/genre/{genre}')
async def bands_for_genre(genre : GenreURLchoices) -> list[dict[str,object]]:
    
    return [
        b for b in Bands if b['genre'].lower() == genre.value#.lower()
    ]
"""    
    
# vídeo 3
# Pydantic é uma biblioteca que o FastAPI usa para validar os dados de entrada
# é diferente de emun, pois nao se preocupa com a validação de possibilidades que uma var pode ter,
# mas sim com a validação de tipos de dados e estruturas de dados
# podes combiná-los e usar Enum dentro de Pydantic para validar os dados de entrada


# vídeo 4
# Vamos ver Query Parameters, que são parâmetros que podes passar na URL
# query parameters aparecem depois do ? na URL, podes ter vários separados por &
# no código são parâmeytros que não aparecem no @app...., mas apenas na função
#http://127.0.0.1:8000/all_bands?genre=rock
#http://127.0.0.1:8000/all_bands?genre=rock&has_albuns=true

# mesmo quando tens None, tens de meter None = None como default
"""@app.get('/all_bands')
async def get_all_bands(genre : GenreURLchoices | None = None) -> list[Band]:
    if genre :
        return [
            Band(**b) for b in Bands if b['genre'].lower() == genre.value
        ]
        
    else:
        return [
            Band(**b) for b in Bands
        ]"""
        


"""@app.get('/all_bands')
async def get_all_bands(genre : GenreURLchoices | None = None,
                        has_albuns : bool | None = None,
                        ) -> list[Band]:
    
    band_list = [Band(**b) for b in Bands]
    
    if genre :
        band_list = [
            # usas b.genre pq b é agora um objecto, e nao um dict
            b for b in band_list if b.genre.lower() == genre.value
        ]
        
    if has_albuns:
        band_list = [
            b for b in band_list if len(b.albuns) > 0
        ]
    
    return band_list
"""
# Vídeo 5
# Fiquei no minuto 9
# vamos usar endpoints de post requests e integrar os dados que provêem 
# do body da request com o Pydantic
# Request body is the data sent by the client to the server. Usually done in Post, Put or Patch
# Response Body is the data sent by the server to the client. Usually done in Get or Post


# Vídeo 6
# Vamos usar annotations e Query para adicionar Metadata aos parâmetros da função e aplicar extra datavalidation, respectivamente
@app.get('/all_bands')
async def get_all_bands(genre : Genrechoices | None = None,
                        has_albuns : bool | None = None,
                        q: Annotated[str | None, Query(max_length = 20)] = None
                        ) -> list[BandWithID]:
    
    band_list = [BandWithID(**b) for b in Bands]
    
    if genre :
        band_list = [
            # usas b.genre pq b é agora um objecto, e nao um dict
            #b for b in band_list if b.genre.lower() == genre.value
            # se o genre usar Genrechoices, tens de usar b.genre.value
            b for b in band_list if b.genre.value.lower() == genre.value
        ]
        
    if has_albuns:
        band_list = [
            b for b in band_list if len(b.albuns) > 0
        ]
        
    if q:
        band_list = [
            b for b in band_list if q.lower() in b.name.lower()   
        ]
    
    return band_list

@app.get('/bands/{id}', status_code = 200)
# id é um path parameter, ou seja, é um parâmetro que aparece na URL
# Por isso tens de usar Path para adicionar metadata ao parâmetro
async def get_band(id :Annotated[int, Path(title = "The band ID")]) -> BandWithID:
    
    band_to_return = None
    for band in Bands:
        if band['id'] == int(id):
            band_to_return = BandWithID(**band)
    
    # se não encontrar a banda, retorna um erro 404
    # 404 é o código de erro para "Not Found"
    # HTTPException é uma exceção que o FastAPI usa para retornar erros HTTP
    if band_to_return is None:
        raise HTTPException(status_code = 404, detail="Band not found")
    else:
        return band_to_return
    
    

# devolves o BandWithID pq vais devolver algo com um auto generated ID
@app.post('/all_bands', status_code = 201)
async def create_band(band_data : BandCreate) -> BandWithID:
    id = Bands[-1]['id'] + 1
    # passas o id e os dados da banda oferecidos pelo utilizador (estes passam pelo Pydantic BandCreate)
    band = BandWithID(id=id, **band_data.model_dump()).model_dump() # model dump passa para um dict
    Bands.append(band)
    # devolves banda para validar com o schema
    return band