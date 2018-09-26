import os

from etl.config import JOBS, YEARS, OUTPUT, AUX_MUN, FIXES, DATABASES
from etl.process.CrawlerTSEDataProcess import CrawlTSEDataProcess
from etl.process.FixProcess import FixProcess
from etl.process.OrganizingProcess import OrganizingProcess
from etl.process.TSEAggregationsProcess import TSEAggregationsProcess
from etl.process.TSEDimensionsProcess import TSEDimensionsProcessor
from etl.process.TSEFactProcess import TSEFactProcess
from etl.process.items import SourceFileItem


def check(item):
    if isinstance(item, SourceFileItem):
        valid = item['year'] in YEARS and item['database'] in DATABASES
    else:
        valid = item['year'] in YEARS

    if valid:
        print(item)
        return True
    else:
        return False


def run():
    print("Crawling")
    crawl = CrawlTSEDataProcess(JOBS, YEARS, os.path.join(OUTPUT, 'source'), os.path.join(OUTPUT, 'processed'))
    # crawl.start()
    output_files = crawl.output_files()

    print("Fixing Files")
    fixer = FixProcess(FIXES, os.path.join(OUTPUT, 'fixes'))
    for f in output_files:
        item = SourceFileItem.create(f)
        if check(item):
            fixer.handle(item)
    output_files = fixer.output_files()

    print("Started Organizing Files")
    organizer = OrganizingProcess(JOBS, AUX_MUN, os.path.join(OUTPUT, 'final'))
    for f in fixer.output_files():
        item = SourceFileItem.create(f)
        if check(item):
            organizer.handle(item)
    print("Finished Organizing Files")

    print("TSE Dimensions Generation")
    dim = TSEDimensionsProcessor(AUX_MUN, os.path.join(OUTPUT, 'tse'))
    for f in output_files:
        item = SourceFileItem.create(f)
        if check(item):
            dim.handle(item)

    print("TSE Fact Generation")
    fact = TSEFactProcess(AUX_MUN, os.path.join(OUTPUT, 'tse'))
    for f in output_files:
        item = SourceFileItem.create(f)
        if check(item):
            fact.handle(item)
    output_files = fact.output_files()

    print("TSE Aggregations Generation")
    aggr = TSEAggregationsProcess(os.path.join(OUTPUT, 'tse'))
    for f in output_files:
        item = SourceFileItem.create(f)
        if check(item):
            aggr.handle(item)
    output_files = aggr.output_files()

    #
    # print("Import to MySQL")
    # mysql = ImportToMySQLProcess(MYSQL)
    # for f in output_files:
    #     item = TSEFileItem.create(f)
    #     if check(item):
    #         mysql.handle(item)


if __name__ == "__main__":
    run()
