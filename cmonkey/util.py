"""util.py - cMonkey utility module

This file is part of cMonkey Python. Please see README and LICENSE for
more information and licensing details.
"""
from BeautifulSoup import BeautifulSoup
from operator import attrgetter
from scipy.stats import scoreatpercentile


def next_non_comment_index(lines, comment, line_index):
    """utility method that takes a list of strings and returns the next
    line index of a non-comment line. it also skips empty lines
    """
    if comment:
        num_lines = len(lines)
        line = lines[line_index].lstrip()
        while line_index < num_lines and (len(line) == 0 or
                                          line.startswith(comment)):
            line_index += 1
            line = lines[line_index].lstrip()
    return line_index


def remove_quotes(astring, quote):
    """removes the quote character from the input string if given"""
    if quote:
        return astring.replace(quote, "")
    else:
        return astring


class DelimitedFile:  # pylint: disable-msg=R0913
    """A file class to read text files that are delimited with certain
    separators. This class offers some flexibility over regular csv
    reading mechanisms by allowing for comments and storing optional
    headers.
    Create a DelimitedFile instance by calling DelimitedFile.read()."""
    def __init__(self, lines, header):
        self.lines = lines
        self.header = header

    @classmethod
    def read(cls, filepath, sep='\t', has_header=False, comment=None,
             quote=None):
        """Creates the reader object"""
        file_header = None
        file_lines = []
        lines = None
        with open(filepath) as inputfile:
            lines = inputfile.readlines()

        line_index = next_non_comment_index(lines, comment, 0)
        if has_header:
            file_header = lines[line_index].rstrip().split(sep)
            file_header = [remove_quotes(elem, quote) for elem in file_header]
            line_index += 1

        num_lines = len(lines)
        while line_index < num_lines:
            line_index = next_non_comment_index(lines, comment, line_index)
            if line_index < num_lines:
                line = lines[line_index].rstrip().split(sep)
                line = [remove_quotes(elem, quote) for elem in line]
                file_lines.append(line)
                line_index += 1

        return DelimitedFile(file_lines, file_header)

    def get_lines(self):
        """returns the lines in the file"""
        return self.lines

    def get_header(self):
        """returns the header in the file"""
        return self.header


def levenshtein_distance(str1, str2):
    """computes the Levenshtein distance. This is used in order
    to make approximate string comparisons"""
    strlen1 = len(str1)
    strlen2 = len(str2)

    dist = [[0 for _ in range(strlen2 + 1)] for _ in range(strlen1 + 1)]
    for row in range(strlen1 + 1):
        dist[row][0] = row
    for col in range(strlen2 + 1):
        dist[0][col] = col

    for col in range(strlen2):
        for row in range(strlen1):
            if str1[row] == str2[col]:
                dist[row + 1][col + 1] = dist[row][col]
            else:
                dist[row + 1][col + 1] = min(dist[row][col + 1] + 1,
                                             dist[row + 1][col] + 1,
                                             dist[row][col] + 1)
    return dist[strlen1][strlen2]


class RankedAnchor:  # pylint: disable-msg=R0903
    """A hyperlink with a Levenshtein score"""
    def __init__(self, score, anchor):
        """Creates a GenomeListEntry with a given Levenshtein distance
        and a BeautifulSoup anchor tag"""
        self.score = score
        self.anchor = anchor

    def __str__(self):
        return "(score: %d, %s)" % (self.score, str(self.anchor))

    def __repr__(self):
        return str(self)


def best_matching_links(search_string, html_file_path):
    """given a search string and an HTML file, extract the
    best matching href"""
    with open(html_file_path) as inputfile:
        html = inputfile.read()
    soup = BeautifulSoup(html)
    links = []
    for anchor in soup.findAll('a'):
        score = levenshtein_distance(search_string, anchor['href'])
        links.append(RankedAnchor(score, anchor))
    result = sorted(links, key=attrgetter('score'))
    num_results = len(result)
    if num_results > 0:
        best_score = result[0].score
        num_best = 1
        while num_best < num_results and result[num_best].score == best_score:
            num_best += 1
    return [entry.anchor['href'] for entry in result[0:num_best]]


def quantile(values, probability):
    """does the same as R's quantile function.
    values a list of numeric values
    probability a value in the range between 0 and 1
    """
    return round(scoreatpercentile(values, probability * 100), 6)


def make_matrix(row_names, num_columns, init_value=0):
    """creates a two-dimensional matrix with len(row_names) rows and
    num_cols columns, where all fields are initialized with
    init_value. The rows are accessed by row name"""
    result = {}
    for name in row_names:
        result[name] = [init_value for _ in range(num_columns)]
    return result


__all__ = ['DelimitedFile', 'best_matching_links', 'quantile', 'make_matrix']