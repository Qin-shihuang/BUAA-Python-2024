import zlib

from utils.pyac.submission import Submission


# Performing NCD test
def ncdTest(a: Submission, b: Submission, max_len=90000) -> float:
    combined = a.content + b.content
    a_size = a.getCompSize()
    b_size = b.getCompSize()
    combined_size = len(zlib.compress(combined.encode()))
    m = min(a_size, b_size)
    M = a_size + b_size - m
    res = float((combined_size - m)) / M
    # correction for small files
    # see https://stackoverflow.com/questions/1085048/how-would-you-code-an-anti-plagiarism-site
    if combined_size < max_len:
        min_content = a.content if a_size < b_size else b.content
        aa_size = len(zlib.compress((min_content + min_content).encode()))
        ref = (aa_size - m) / m
        res = res - ref
    return res


