import os

from etl.config import JOBS, YEARS, OUTPUT, AUX_MUN, FIXES, DATABASES, UF
from etl.crawler.process import CrawlTSEDataProcess
from etl.process.CandidatesProcess import CandidatesProcess
from etl.process.CoalitionsProcess import CoalitionsProcess
from etl.process.FixProcess import FixProcess
from etl.process.PartitioningDimensionsProcess import PartitioningDimensionsProcess
from etl.process.PartitioningVotesProcess import PartitioningVotesProcess
from etl.process.VotesVotsecProcess import VotesVotsecProcess
from etl.process.PartitioningBemCandidatoProcess import PartitioningBemCandidatoProcess
from etl.process.DetalheVotSecProcess import DetalheVotSecProcess
from etl.process.PartitioningDetalheProcess import PartitioningDetalheProcess
from etl.process.BemCandidatoProcess import BemCandidatoProcess
from etl.process.items import SourceFileItem, TSEFileItem


def check(item):
    if isinstance(item, SourceFileItem):
        if item['database'] == 'votos' and len(UF) > 0 and item['uf'] not in UF:
            return False

        return item['year'] in YEARS and item['database'] in DATABASES
    else:
        if item['table'] == 'votos' and len(UF) > 0 and item['uf'] not in UF:
            return False

        return item['year'] in YEARS


def process(output_files, process_class, item_class, *args):
    p = process_class(*args)
    for f in output_files:
        item = item_class.create(f)
        if check(item) and p.check(item) and not p.done(item):
            print(item)
            try:
                p.handle(item)
            except Exception as e:
                print(e.__class__.__name__, e)

    return p


def run():
    print("Crawling")
    crawl = CrawlTSEDataProcess(JOBS, YEARS, os.path.join(OUTPUT, 'source'), os.path.join(OUTPUT, 'processed'))
    crawl.start()
    output_files = crawl.output_files()

    print("Fixing Files")
    fixer = FixProcess(FIXES, os.path.join(OUTPUT, 'fixes'))
    for f in output_files:
        item = SourceFileItem.create(f)
        if check(item):
            print(item)
            fixer.handle(item)
    output_files = fixer.output_files()

    print("Generating Candidates")
    cand = process(output_files, CandidatesProcess, SourceFileItem, os.path.join(OUTPUT, 'joined/candidatos'))

    print("Generating Coalitions")
    leg = process(output_files, CoalitionsProcess, SourceFileItem, os.path.join(OUTPUT, 'joined/legendas'))

    print("Generating Detalhe")
    detalhe = process(output_files, DetalheVotSecProcess, SourceFileItem, AUX_MUN,
                      os.path.join(OUTPUT, 'joined/detalhe'))

    print("Generating Bem Candidato")
    bem = process(output_files, BemCandidatoProcess, SourceFileItem, cand.output,
                  os.path.join(OUTPUT, 'joined/bem_candidato'))

    print("Generating Votes - Votsec")
    votsec = process(output_files, VotesVotsecProcess, SourceFileItem, AUX_MUN, cand.output, leg.output,
                     os.path.join(OUTPUT, 'joined/votos'))

    print("Partitionning Bem Candidato")
    process(bem.output_files(), PartitioningBemCandidatoProcess, SourceFileItem,
            os.path.join(OUTPUT, 'final/bem_candidato'))

    print("Partitioning Files - Candidates")
    process(cand.output_files(), PartitioningDimensionsProcess, TSEFileItem, JOBS,
            os.path.join(OUTPUT, 'final/candidatos'))

    print("Partitioning Files - Legendas")
    process(leg.output_files(), PartitioningDimensionsProcess, TSEFileItem, JOBS,
            os.path.join(OUTPUT, 'final/legendas'))

    print("Partitioning Files - Votes")
    process(votsec.output_files(), PartitioningVotesProcess, TSEFileItem, JOBS, os.path.join(OUTPUT, 'final/votos'))

    print("Partitioning Files - Detalhe")
    process(detalhe.output_files(), PartitioningDetalheProcess, TSEFileItem, JOBS,
            os.path.join(OUTPUT, 'final/detalhe'))


if __name__ == "__main__":
    run()
