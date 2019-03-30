from etl.config import FIXES
from etl.process.TestProcess import TestProcess


def run():
    tester = TestProcess(FIXES)
    tester.handle()


if __name__ == "__main__":
    run()
