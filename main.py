from fastapi import FastAPI, HTTPException, Path,Query, Depends
from models import GenreURLchoices, Genrechoices, BandCreate, Band, Album
from typing import Annotated
from db import init_db,get_session
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

#activar o ambiente virtual
# .\venv-fastapi\Scripts\activate
# correr a app ; uvicorn main:app 

#" Vídeo 7"

# vamos criar um Lifespan event; estes servem para definir lógica que deve acontecer antes, ou depois, da aplicação iniciar
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # inicializa o banco de dados
    yield  # aqui é onde a aplicação está a correr

app = FastAPI(lifespan=lifespan)

@app.get('/all_bands')
async def get_all_bands(genre : Genrechoices | None = None,
                        has_albums : bool | None = None,
                        q: Annotated[str | None, Query(max_length = 20)] = None,
                        session: Session = Depends(get_session)
                        ) -> list[Band]:
    
    
    band_list = session.exec(select(Band)).all()
    
    if genre :
        band_list = [
            # usas b.genre pq b é agora um objecto, e nao um dict
            #b for b in band_list if b.genre.lower() == genre.value
            # se o genre usar Genrechoices, tens de usar b.genre.value
            b for b in band_list if b.genre.value.lower() == genre.value
        ]
        
    if has_albums:
        band_list = [
            b for b in band_list if len(b.albums) > 0
        ]
        
    if q:
        band_list = [
            b for b in band_list if q.lower() in b.name.lower()   
        ]
    
    return band_list

@app.get('/bands/{id}', status_code = 200)
# id é um path parameter, ou seja, é um parâmetro que aparece na URL
# Por isso tens de usar Path para adicionar metadata ao parâmetro
async def get_band(id :Annotated[int, Path(title = "The band ID")],
                   session : Session = Depends(get_session)) -> Band:
    
    # o problema
    statement = select(Band).where(Band.id == id).options(selectinload(Band.albums))
    band_to_return = session.exec(statement).first()  # Use .first() to get the object or None
    
    if band_to_return is None:
        raise HTTPException(status_code = 404, detail="Band with the given id not found")
   
    return band_to_return
    
    

# devolves o BandWithID pq vais devolver algo com um auto generated ID
@app.post('/all_bands', status_code = 201)
async def create_band(band_data : BandCreate,
                      session : Session = Depends(get_session)) -> Band:
    
    band = Band(name = band_data.name, genre = band_data.genre )
    # vais usar a sessão aberta de SQL para injectares os dados do POST request na base de dados
    # sessao depende da função que cria a função (e que está no db.py)
    
    session.add(band)
    
    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album(title = album.title, 
                              release_date = album.release_date,
                              band = band)
            session.add(album_obj)  
    
    # a primary key é gerada automaticamente pelo SQLModel depois do commit
    session.commit()    
    
    session.refresh(band)
    
    return band
