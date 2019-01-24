import os
from etl.config import JOBS, YEARS, OUTPUT, AUX_MUN, FIXES, DATABASES
from etl.process.CandidatesProcess import CandidatesProcess
from etl.process.CoalitionsProcess import CoalitionsProcess
from etl.process.CrawlerTSEDataProcess import CrawlTSEDataProcess
from etl.process.FixProcess import FixProcess
from etl.process.PartitioningDimensionsProcess import PartitioningDimensionsProcess
from etl.process.PartitioningVotesProcess import PartitioningVotesProcess
from etl.process.VotesVotsecProcess import VotesVotsecProcess
from etl.process.items import SourceFileItem, TSEFileItem


def check(item):
    if isinstance(item, SourceFileItem):
        return item['year'] in YEARS and item['database'] in DATABASES
    else:
        return item['year'] in YEARS


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
    cand = CandidatesProcess(os.path.join(OUTPUT, 'joined/candidatos'))
    for f in output_files:
        item = SourceFileItem.create(f)
        if check(item) and cand.check(item) and not cand.done(item):
            print(item)
            try:
                cand.handle(item)
            except Exception as e:
                print(e.__class__.__name__, e)

    print("Generating Coalitions")
    leg = CoalitionsProcess(os.path.join(OUTPUT, 'joined/legendas'))
    for f in output_files:
        item = SourceFileItem.create(f)
        if check(item) and leg.check(item) and not leg.done(item):
            print(item)
            try:
                leg.handle(item)
            except Exception as e:
                print(e)

    print("Generating Votes - Votsec")
    votsec = VotesVotsecProcess(AUX_MUN, cand.output, leg.output, os.path.join(OUTPUT, 'joined/votos'))
    for f in output_files:
        item = SourceFileItem.create(f)
        if check(item) and votsec.check(item) and not votsec.done(item):
            print(item)
            try:
                votsec.handle(item)
            except Exception as e:
                print(e.__class__.__name__, e)

    print("Partitioning Files - Candidates")
    part_dim = PartitioningDimensionsProcess(JOBS, os.path.join(OUTPUT, 'final/candidatos'))
    for f in cand.output_files():
        item = TSEFileItem.create(f)
        if check(item) and part_dim.check(item) and not part_dim.done(item):
            print(item)
            try:
                part_dim.handle(item)
            except Exception as e:
                print(e.__class__.__name__, e)

    print("Partitioning Files - Legendas")
    part_dim = PartitioningDimensionsProcess(JOBS, os.path.join(OUTPUT, 'final/legendas'))
    for f in leg.output_files():
        item = TSEFileItem.create(f)
        if check(item) and part_dim.check(item) and not part_dim.done(item):
            print(item)
            try:
                part_dim.handle(item)
            except Exception as e:
                print(e.__class__.__name__, e)

    print("Partitioning Files - Votes")
    part = PartitioningVotesProcess(JOBS, os.path.join(OUTPUT, 'final/votos'))
    for f in votsec.output_files():
        item = TSEFileItem.create(f)
        if check(item) and part.check(item) and not part.done(item):
            print(item)
            try:
                part.handle(item)
            except Exception as e:
                print(e.__class__.__name__, e)


if __name__ == "__main__":
    run()
