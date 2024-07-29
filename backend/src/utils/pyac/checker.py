from utils.pyac.ncd import ncdTest
from utils.pyac.submission import Submission

def test_two_lists(list1, list2, t0=0.2):
    if list1 == [] or list2 == []:
        return [], list1, list2
    distances = []
    for r1 in list1:
        row = []
        for r2 in list2:
            sub1 = Submission(r1[1])
            sub2 = Submission(r2[1])
            distance = ncdTest(sub1, sub2)
            row.append(distance)
        distances.append(row)

    t0_match = []
    list1_matched = []
    list2_matched = []

    # best matching
    while True:
        min_val = 1
        min_i = 0
        min_j = 0
        for i in range(len(distances)):
            for j in range(len(distances[i])):
                if distances[i][j] < min_val:
                    min_val = distances[i][j]
                    min_i = i
                    min_j = j
        if min_val < t0:
            l1_i = (list1[min_i][0], list1[min_i][1].rstrip() + '\n')
            l2_j = (list2[min_j][0], list2[min_j][1].rstrip() + '\n')
            t0_match.append((min_val, l1_i, l2_j))
            list1_matched.append(min_i)
            list2_matched.append(min_j)
            for i in range(len(distances)):
                distances[i][min_j] = 1
            for j in range(len(distances[min_i])):
                distances[min_i][j] = 1
        else:
            break
    # no-match snippets
    list1_no_match = [list1[i] for i in range(len(list1)) if i not in list1_matched]
    list2_no_match = [list2[i] for i in range(len(list2)) if i not in list2_matched]
    return t0_match, list1_no_match, list2_no_match

def test_two_files(sub1, sub2, snippet_test=True):
    distance = ncdTest(sub1, sub2)
    distance = min(1, max(0, distance))

    if not snippet_test or distance > 0.6:
        return distance, []
    
    content1 = sub1.content.replace('\t', '    ').replace('\r', '')
    content2 = sub2.content.replace('\t', '    ').replace('\r', '')

    c1_lines = [s for s in content1.split('\n')]
    c2_lines = [s for s in content2.split('\n')]

    # round1 : classes, outer functions and if statements
    i = 0
    r1_seg1 = []
    r2_seg1 = []
    while i < len(c1_lines):
        snippet = ''
        if c1_lines[i].startswith('class') or c1_lines[i].startswith('def'):
            start = i
            snippet += c1_lines[i] + '\n'
            i += 1
            # while indentation is same
            while i < len(c1_lines) and (c1_lines[i].startswith('    ') or c1_lines[i].strip() == ''):
                snippet += c1_lines[i] + '\n'
                i += 1
            r1_seg1.append((start, snippet))
        elif c1_lines[i].startswith('try'):
            start = i
            snippet += c1_lines[i] + '\n'
            i += 1
            while i < len(c1_lines) and (c1_lines[i].startswith('    ') or c1_lines[i].strip() == '' or c1_lines[i].startswith('except') or c1_lines[i].startswith('finally')):
                snippet += c1_lines[i] + '\n'
                i += 1
            r1_seg1.append((start, snippet))
        elif c1_lines[i].startswith('if') or c1_lines[i].startswith('while') or c1_lines[i].startswith('for'):
            start = i
            snippet += c1_lines[i] + '\n'
            i += 1
            while i < len(c1_lines) and (c1_lines[i].startswith('    ') or c1_lines[i].strip() == '' or c1_lines[i].startswith('elif') or c1_lines[i].startswith('else')):
                snippet += c1_lines[i] + '\n'
                i += 1
            r1_seg1.append((start, snippet))
        else:
            i += 1

    i = 0
    r1_seg2 = []
    r2_seg2 = []
    while i < len(c2_lines):
        snippet = ''
        if c2_lines[i].startswith('class') or c2_lines[i].startswith('def'):
            start = i
            snippet += c2_lines[i] + '\n'
            i += 1
            # while indentation is same
            while i < len(c2_lines) and (c2_lines[i].startswith('    ') or c2_lines[i].strip() == ''):
                snippet += c2_lines[i] + '\n'
                i += 1
            
            r1_seg2.append((start, snippet))
        elif c2_lines[i].startswith('try'):
            start = i
            snippet += c2_lines[i] + '\n'
            i += 1
            while i < len(c2_lines) and (c2_lines[i].startswith('    ') or c2_lines[i].strip() == '' or c2_lines[i].startswith('except') or c2_lines[i].startswith('finally')):
                snippet += c2_lines[i] + '\n'
                i += 1
            r1_seg2.append((start, snippet))
        elif c2_lines[i].startswith('if') or c2_lines[i].startswith('while') or c2_lines[i].startswith('for'):
            start = i
            snippet += c2_lines[i] + '\n'
            i += 1
            while i < len(c2_lines) and (c2_lines[i].startswith('    ') or c2_lines[i].strip() == '' or c2_lines[i].startswith('elif') or c2_lines[i].startswith('else')):
                snippet += c2_lines[i] + '\n'
                i += 1
            r1_seg2.append((start, snippet))
        else:
            i += 1
    r1_match, r1_seg1_unmatched, r1_seg2_unmatched = test_two_lists(r1_seg1, r1_seg2)

    # rouond 2: non-matched classes
    for i in range(len(r1_seg1_unmatched)):
        if r1_seg1_unmatched[i][1].startswith('class') or r1_seg1_unmatched[i][1].startswith('try'):
            lines = r1_seg1_unmatched[i][1].split('\n')
            j = 0
            while j < len(lines):
                snippet = ''
                if lines[j].startswith('    def') or lines[j].startswith('    while') or lines[j].startswith('    for') or lines[j].startswith('    if'):
                    start = j + r1_seg1_unmatched[i][0]
                    snippet += lines[j][4:] + '\n'
                    j += 1
                    while j < len(lines) and (lines[j].startswith('        ') or lines[j].strip() == ''):
                        if lines[j].strip() != '':
                            snippet += lines[j][4:] + '\n'
                    r2_seg1.append((start, snippet))
                else:
                    j += 1
        elif r1_seg1_unmatched[i][1].startswith('def'):
            r2_seg1.append(r1_seg1_unmatched[i])
    for i in range(len(r1_seg2_unmatched)):
        if r1_seg2_unmatched[i][1].startswith('class') or r1_seg2_unmatched[i][1].startswith('try'):
            lines = r1_seg2_unmatched[i][1].split('\n')
            j = 0
            while j < len(lines):
                snippet = ''
                if lines[j].startswith('    def') or lines[j].startswith('    while') or lines[j].startswith('    for') or lines[j].startswith('    if'):
                    start = j + r1_seg2_unmatched[i][0]
                    snippet += lines[j][4:] + '\n'
                    j += 1
                    while j < len(lines) and (lines[j].startswith('        ') or lines[j].strip() == ''):
                        if lines[j].strip() != '':
                            snippet += lines[j][4:] + '\n'
                        j += 1
                    r2_seg2.append((start, snippet))
                else:
                    j += 1
        elif r1_seg2_unmatched[i][1].startswith('def'):
            r2_seg2.append(r1_seg2_unmatched[i])
    r2_match, _, _ = test_two_lists(r2_seg1, r2_seg2)
    # round 3: top level statements
    r3_seg1 = []
    i = 0
    while i < len(c1_lines):
        if c1_lines[i].startswith('class') or c1_lines[i].startswith('def'):
            i += 1
            while i < len(c1_lines) and (c1_lines[i].startswith('    ') or c1_lines[i].strip() == ''):
                i += 1
        elif c1_lines[i].startswith('try'):
            start = i
            i += 1
            while i < len(c1_lines) and (c1_lines[i].startswith('    ') or c1_lines[i].strip() == '' or c1_lines[i].startswith('except') or c1_lines[i].startswith('finally')):
                i += 1
        elif c1_lines[i].startswith('if') or c1_lines[i].startswith('while') or c1_lines[i].startswith('for'):
            start = i
            i += 1
            while i < len(c1_lines) and (c1_lines[i].startswith('    ') or c1_lines[i].strip() == '' or c1_lines[i].startswith('elif') or c1_lines[i].startswith('else')):
                i += 1
        else:
            if c1_lines[i].strip() != '':
                r3_seg1.append((i, c1_lines[i]))
            i += 1
    r3_seg2 = []
    i = 0
    while i < len(c2_lines):
        if c2_lines[i].startswith('class') or c2_lines[i].startswith('def'):
            i += 1
            while i < len(c2_lines) and (c2_lines[i].startswith('    ') or c2_lines[i].strip() == ''):
                i += 1
        elif c2_lines[i].startswith('try'):
            start = i
            i += 1
            while i < len(c2_lines) and (c2_lines[i].startswith('    ') or c2_lines[i].strip() == '' or c2_lines[i].startswith('except') or c2_lines[i].startswith('finally')):
                i += 1
        elif c2_lines[i].startswith('if') or c2_lines[i].startswith('while') or c2_lines[i].startswith('for'):
            start = i
            i += 1
            while i < len(c2_lines) and (c2_lines[i].startswith('    ') or c2_lines[i].strip() == '' or c2_lines[i].startswith('elif') or c2_lines[i].startswith('else')):
                i += 1
        else:
            if c2_lines[i].strip() != '':
                r3_seg2.append((i, c2_lines[i]))
            i += 1
    r3_seg1 = [s for s in r3_seg1 if len(s[1]) > 15]
    r3_seg2 = [s for s in r3_seg2 if len(s[1]) > 15]
    r3_match, _, _ = test_two_lists(r3_seg1, r3_seg2)

    match = r1_match + r2_match + r3_match
    match.sort(key=lambda x: x[1][0])

    match_lines = []
    for m in match:
        s1_line_start = m[1][0] + 1
        s2_line_start = m[2][0] + 1
        s1_line_count = m[1][1].count('\n')
        s2_line_count = m[2][1].count('\n')
        match_lines.append((s1_line_start, s1_line_start + s1_line_count, s2_line_start, s2_line_start + s2_line_count))

    return distance, match_lines