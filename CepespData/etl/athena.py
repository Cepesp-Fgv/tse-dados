from etl.process.CreateAthenaTables import CreateAthenaTables, LoadAthenaPartitions

APP_ENV = 'master'
ATHENA_DATABASE = 'cepesp_' + APP_ENV
ATHENA_BUCKET = 'cepesp-athena'
ATHENA_BUCKET_FOLDER = 'source-' + APP_ENV
YEARS = [1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018]
JOBS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13]


def create():
    print("Create tables - Athena")
    tables = CreateAthenaTables(ATHENA_DATABASE, ATHENA_BUCKET_FOLDER, ATHENA_BUCKET)
    tables.create()


def partitions():
    print("Loading partitions - Athena")
    partitions_builder = LoadAthenaPartitions(ATHENA_DATABASE, ATHENA_BUCKET_FOLDER, ATHENA_BUCKET, YEARS, JOBS)
    partitions_builder.create()


if __name__ == "__main__":
    create()
    partitions()
