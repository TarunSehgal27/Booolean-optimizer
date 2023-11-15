"""def get_binary_representation(num, num_bits):
    binary = bin(num)[2:]
    return '0' * (num_bits - len(binary)) + binary

def count_ones(binary_str):
    return binary_str.count('1')

def combine_terms(term1, term2):
    result = ''
    diff_count = 0
    for bit1, bit2 in zip(term1, term2):
        if bit1 == bit2:
            result += bit1
        else:
            result += '-'
            diff_count += 1
    if diff_count == 1:
        return result
    return None

def quine_mccluskey(minterms, num_vars):
    prime_implicants = []

    # Step 1: Group minterms by the number of 1s
    groups = [[] for _ in range(num_vars + 1)]
    for minterm in minterms:
        num_ones = count_ones(get_binary_representation(minterm, num_vars))
        groups[num_ones].append(get_binary_representation(minterm, num_vars))

    # Step 2: Combine adjacent groups
    while True:
        new_groups = [[] for _ in range(num_vars)]
        for i in range(len(groups) - 1):
            for term1 in groups[i]:
                for term2 in groups[i + 1]:
                    combined = combine_terms(term1, term2)
                    if combined is not None and combined not in new_groups[i]:
                        new_groups[i].append(combined)

        # If no new terms are generated, break the loop
        if all(len(group) == 0 for group in new_groups):
            break

        groups = new_groups

    # Step 3: Select prime implicants
    for group in groups:
        for term in group:
            prime_implicants.append(term)

    # Step 4: Simplify the expression using essential prime implicants
    simplified_expression = []
    covered_minterms = set()
    for minterm in minterms:
        for implicant in prime_implicants:
            if get_binary_representation(minterm, num_vars) in implicant:
                simplified_expression.append(implicant)
                covered_minterms.add(minterm)
                break

    # Include any remaining minterms that are not covered by essential prime implicants
    for minterm in minterms:
        if minterm not in covered_minterms:
            simplified_expression.append(get_binary_representation(minterm, num_vars))

    # Combine terms into a final expression
    final_expression = ' + '.join(simplified_expression)

    return final_expression

# Example usage:
minterms = [0, 1, 3, 5, 7]
num_vars = 3
result = quine_mccluskey(minterms, num_vars)
print("Simplified Expression:", result)
"""
def mul(x, y):
    res = []
    for i in x:
        if i + "'" in y or (len(i) == 2 and i[0] in y):
            return []
        else:
            res.append(i)
    for i in y:
        if i not in res:
            res.append(i)
    return res

def multiply(x, y):
    res = []
    for i in x:
        for j in y:
            tmp = mul(i, j)
            res.append(tmp) if len(tmp) != 0 else None
    return res

def refine(my_list, dc_list):
    res = []
    for i in my_list:
        if int(i) not in dc_list:
            res.append(i)
    return res

def findEPI(x):
    res = []
    for i in x:
        if len(x[i]) == 1:
            res.append(x[i][0]) if x[i][0] not in res else None
    return res

def findVariables(x):
    var_list = []
    for i in range(len(x)):
        if x[i] == '0':
            var_list.append(chr(i + 65) + "'")
        elif x[i] == '1':
            var_list.append(chr(i + 65))
    return var_list

def flatten(x):
    flattened_items = []
    for i in x:
        flattened_items.extend(x[i])
    return flattened_items

def findminterms(a):
    gaps = a.count('-')
    
    if gaps == 0:
        return [str(int(a, 2))]
    x = [bin(i)[2:].zfill(gaps) for i in range(pow(2, gaps))]
    temp = []
    for i in range(pow(2, gaps)):
        temp2, ind = a[:], -1
        for j in x[0]:
            if ind != -1:
                ind = ind + temp2[ind + 1:].find('-') + 1
            else:
                ind = temp2[ind + 1:].find('-')
            temp2 = temp2[:ind] + j + temp2[ind + 1:]
        temp.append(str(int(temp2, 2)))
        x.pop(0)
    return temp

def compare(a, b):
    c = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            mismatch_index = i
            c += 1
            if c > 1:
                return (False, None)
    return (True, mismatch_index)

def removeTerms(_chart, terms):
    for i in terms:
        for j in findminterms(i):
            try:
                del _chart[j]
            except KeyError:
                pass

def quine_mccluskey_simplification(minterms, dc):
    mt = sorted(minterms)
    minterms = mt + dc
    minterms.sort()
    size = len(bin(minterms[-1])) - 2
    groups, all_pi = {}, set()

    for minterm in minterms:
        try:
            groups[bin(minterm).count('1')].append(bin(minterm)[2:].zfill(size))
        except KeyError:
            groups[bin(minterm).count('1')] = [bin(minterm)[2:].zfill(size)]

    while True:
        tmp = groups.copy()
        groups, m, marked, should_stop = {}, 0, set(), True
        l = sorted(list(tmp.keys()))
        
        for i in range(len(l) - 1):
            for j in tmp[l[i]]:
                for k in tmp[l[i + 1]]:
                    res = compare(j, k)
                    if res[0]:
                        try:
                            groups[m].append(j[:res[1]] + '-' + j[res[1] + 1:]) \
                                if j[:res[1]] + '-' + j[res[1] + 1:] not in groups[m] else None
                        except KeyError:
                            groups[m] = [j[:res[1]] + '-' + j[res[1] + 1:]]
                        should_stop = False
                        marked.add(j)
                        marked.add(k)
                m += 1

        local_unmarked = set(flatten(tmp)).difference(marked)
        all_pi = all_pi.union(local_unmarked)
        
        if should_stop:
            break

    sz = len(str(mt[-1]))
    chart = {}
    
    for i in all_pi:
        merged_minterms, y = findminterms(i), 0
        for j in refine(merged_minterms, dc):
            x = mt.index(int(j)) * (sz + 1)
            try:
                chart[j].append(i) if i not in chart[j] else None
            except KeyError:
                chart[j] = [i]

    EPI = findEPI(chart)
    removeTerms(chart, EPI)

    if len(chart) == 0:
        final_result = [findVariables(i) for i in EPI]
    else:
        P = [[findVariables(j) for j in chart[i]] for i in chart]
        while len(P) > 1:
            P[1] = multiply(P[0], P[1])
            P.pop(0)
        final_result = [min(P[0], key=len)]
        final_result.extend(findVariables(i) for i in EPI)

    return final_result

# Example usage:
#minterms_input = input("Enter the minterms: ")
#dc_input = input("Enter the don't cares (If any): ")

#minterms = [int(i) for i in minterms_input.strip().split()]
#dc = [int(i) for i in dc_input.strip().split()]

#result = quine_mccluskey_simplification(minterms, dc)
#print('\nSolution: F = ' + ' + '.join(''.join(i) for i in result))
