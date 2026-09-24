def judge(question, expects, answer, results) -> bool:
    """Criterion 1: does any retrieved chunk contain the expected phrase?"""
    return any(expects.lower() in r.text.lower() for r in results)