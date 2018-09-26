from web.tests.responses import test_repeated_macro, test_duplicated_votes, test_response_ok


def test():
    test_repeated_macro.test()
    test_duplicated_votes.test()
    test_response_ok.test()

if __name__ == "__main__":
    test()
