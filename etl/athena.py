from etl.process.CreateAthenaTables import CreateAthenaTables, LoadAthenaPartitions

APP_ENV = 'master'
ATHENA_DATABASE = 'cepesp_' + APP_ENV
ATHENA_BUCKET = 'cepesp-athena'
ATHENA_BUCKET_FOLDER = 'source-' + APP_ENV
YEARS = [1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018]
JOBS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13]


def create(*tables):
    print("Create tables - Athena")
    creator = CreateAthenaTables(ATHENA_DATABASE, ATHENA_BUCKET_FOLDER, ATHENA_BUCKET)

    if "candidatos" in tables or len(tables) == 0:
        creator.create_candidatos()

    if "legendas" in tables or len(tables) == 0:
        creator.create_legendas()

    if "detalhe" in tables or len(tables) == 0:
        creator.create_detalhe()

    if "bem_candidato" in tables or len(tables) == 0:
        creator.create_bem_candidato()

    if "votos" in tables or len(tables) == 0:
        creator.create_votos()


def partitions(*tables):
    print("Loading partitions - Athena")
    loader = LoadAthenaPartitions(ATHENA_DATABASE, ATHENA_BUCKET_FOLDER, ATHENA_BUCKET, YEARS, JOBS)

    if "candidatos" in tables or len(tables) == 0:
        loader.load_candidatos()

    if "legendas" in tables or len(tables) == 0:
        loader.load_legendas()

    if "bem_candidato" in tables  or len(tables) == 0:
        loader.load_bem_candidato()

    if "votos" in tables or len(tables) == 0:
        loader.load_votos()

    if "detalhe" in tables or len(tables) == 0:
        loader.load_detalhe()


if __name__ == "__main__":
    create()
    partitions()
