from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = 'sqlite:///db.sqlite'

# Vídeo 8
# Vamos usar Alembic para lidar com as mudanças (migrations) na base de dados
# começas por inicializar o Alembic com o comando:
# alembic init migrations
# para meteres os alembic a fazer revisoes sobre migraçoes corres :  alembic revision --autogenerate -m "initial migration"
# mas isto só faz alguma coisa se não tiveres a tabela criada
# ou se fizeres alterações ao modelo
# depois é correres o comando acima e ver quais as alterações que o Alembic detecta ao analisares o ficheiro que gerou e a função upgrade
#  depois corres : alembic upgrade head
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    # vai olhar para as classes de SQLMOdel que têm table = true para criar tais tabelas
    SQLModel.metadata.create_all(engine)
    
def get_session():
    # cria uma sessão para interagir com o banco de dados
    with Session(engine) as session:
        yield session
        
        # este yield é importante porque permite que a sessão seja fechada automaticamente
        # quando a aplicação terminar ou quando a sessão for fechada