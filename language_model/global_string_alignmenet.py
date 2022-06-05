from alignment.sequence import Sequence
from alignment.sequencealigner import SimpleScoring, GlobalSequenceAligner
from alignment.vocabulary import Vocabulary


def _get_alignment_sore_and_percent(seq1, seq2):
    a = Sequence(seq1)
    b = Sequence(seq2)

    v = Vocabulary()
    aEncoded = v.encodeSequence(a)
    bEncoded = v.encodeSequence(b)

    scoring = SimpleScoring(2, -1)
    aligner = GlobalSequenceAligner(scoring, -1)
    score = aligner.align(aEncoded, bEncoded, backtrace=False)

    return score


def get_normalized_score(seq1, seq2):
    score = _get_alignment_sore_and_percent(seq1, seq2)
    return score / (len(seq2) + len(seq1))


if __name__ == '__main__':
    string = "argrgsergserg"
    string2 = "arsrgssdfserg"
    print(get_normalized_score(string, string2))
