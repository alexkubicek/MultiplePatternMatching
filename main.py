import sys


def add_indices_last(raw):
    last_indices = []
    a = c = t = g = 0
    for char in raw:
        if char == 'A':
            new_char = (char, a)
            a += 1
        elif char == 'C':
            new_char = (char, c)
            c += 1
        elif char == 'T':
            new_char = (char, t)
            t += 1
        elif char == 'G':
            new_char = (char, g)
            g += 1
        else:
            new_char = ('$', 0)
        last_indices.append(new_char)
    return last_indices


def get_counts(lastcol):
    count_dict = dict()
    count_dict['A'] = [0]
    count_dict['C'] = [0]
    count_dict['G'] = [0]
    count_dict['T'] = [0]
    count_dict['$'] = [0]
    for tup in lastcol:
        count_dict['A'].append(count_dict['A'][-1])
        count_dict['C'].append(count_dict['C'][-1])
        count_dict['G'].append(count_dict['G'][-1])
        count_dict['T'].append(count_dict['T'][-1])
        count_dict['$'].append(count_dict['$'][-1])
        count_dict[tup[0]][-1] += 1
    return count_dict


def get_matches(last_col, first_o, string, starting_index):
    top = 0
    bottom = len(last_col)-1
    counts = get_counts(last_col)
    while top <= bottom:
        # print("top: " + str(top) + " bottom: " + str(bottom))
        if len(string) > 0:
            symbol = string[len(string)-1]
            # print(symbol)
            string = string[:len(string)-1]
            if counts[symbol][bottom+1] - counts[symbol][top] > 0:
                top = first_o[symbol] + counts[symbol][top]
                bottom = first_o[symbol] + counts[symbol][bottom+1] - 1
            else:
                return
        # print(str(top) + " " + str(bottom))
        else:
            return starting_index[top:bottom+1]
    return


def get_first_occurrences(column):
    first_occurrences = {}
    tuples_to_find = [('$', 0), ("A", 0), ('C', 0), ('T', 0), ('G', 0)]
    for tup in tuples_to_find:
        if tup in column:
            first_occurrences[tup[0]] = column.index(tup)
    return first_occurrences


def better_bwt_matching(bwt, patterns, start):
    last_column = add_indices_last(bwt)
    first_occurrences = get_first_occurrences(sorted(last_column))
    pattern_matches = {}
    for string in patterns:
        if string not in pattern_matches.keys():
            pattern_matches[string] = list()
        found_at = get_matches(last_column, first_occurrences, string, start)
        if found_at:
            found_at.sort()
            pattern_matches[string].extend(found_at)
    return pattern_matches


def bwt_matrix(genome):
    matrix = []
    for i1 in range(len(genome)):
        matrix.append(genome[i1:] + genome[:i1])
    return matrix


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    filePath = input()
    inFile = open(filePath)
    text = inFile.readline()
    while text.endswith("\n"):
        text = text[:len(text)-1]
    if not text.endswith("$"):
        text = text + "$"
    index_to_print = len(text)-1
    m = bwt_matrix(text)
    starting_spot_dict = dict()
    sorted_matrix = sorted(m)
    i = 0
    for line in m:
        starting_spot_dict[line] = i
        i += 1
    starting_positions = []
    for line in sorted_matrix:
        starting_positions.append(starting_spot_dict[line])
    bwtransform = []
    for line in sorted_matrix:
        bwtransform.append(line[index_to_print])

    to_match = []
    for line in inFile:
        to_match.extend(line.split(" "))
        while to_match[-1].endswith("\n"):
            to_match[-1] = to_match[-1][:-1]
    inFile.close()
    # print(file_input)
    # print(to_match)
    answer = better_bwt_matching(bwtransform, to_match, starting_positions)
    f = open("output.txt", "w")
    sys.stdout = f
    for key in answer.keys():
        print(key, end=": ")
        for num in answer[key]:
            print(num, end=" ")
        print()
    f.close()
