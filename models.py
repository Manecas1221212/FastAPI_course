from datetime import date
from enum import Enum
from pydantic import BaseModel, validator
from sqlmodel import SQLModel, Field, Relationship

# Vídeo 7
# vamos usar SQL Model em vez de BaseModel

# Vídeo 8
# Vamos usar Alembic para lidar com as mudanças (migrations) na base de dados
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

class AlbumBase(SQLModel):
    title : str
    release_date : date
    band_id : int | None = Field(foreign_key='band.id')  

# Vais usar o Field para definir o tipo de dado que é a chave primária
# metes table = true para indicar que é uma tabela de sql
class Album(AlbumBase, table = True):
    
    id : int = Field(default = None, primary_key = True)
    # vamos adicionar uma relação com a tabela Band
    band : "Band" = Relationship(back_populates = "albums" )

class BandBase(SQLModel):
    name : str
    genre : Genrechoices
    

class AlbumCreate(SQLModel):
    title: str
    release_date: date

class BandCreate(BandBase):

    albums : list[AlbumCreate] | None = None
    @validator('genre', pre=True)
    def genre_to_title_case(cls, value):
        return value.title() # rock -> Rock

class Band(BandBase, table = True):
    id : int = Field(default=None, primary_key=True)
    albums : list[Album] = Relationship(back_populates="band")
    date_formed : date | None 
