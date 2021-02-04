def a_part():
    print("\nDo not input the So in the conclusion. Words like all, no, some, not, is, are should be in lowercase.")
    print("If they appear more than one time, only the one with logical usefulness shuold be in lowercase.")
    print("Make the one without logical usefulness fully capital like all cat are things that ARE cute")
    print("No Punctuation should be inputted")
    argument = []
    arg_part = ["premise 1", "premise 2", "conclusion"]
    arg_type = []
    temp_counter = 0

    while len(argument) < 3:
        argument.append(
            input("Input your " + arg_part[temp_counter] + ": ").strip().split())
        if argument[temp_counter][0] in ["all", "no", "some"] and ("is" in argument[temp_counter] or "are" in argument[temp_counter]):
            arg_type.append(typefinder(argument, temp_counter))
            temp_counter += 1
        else:
            print("Invalid input found in your " + arg_part[temp_counter])
            argument.pop(temp_counter)

    s, p = findterms(2, arg_type, argument)
    p1_first, p1_sec = findterms(0, arg_type, argument)
    p2 = [*findterms(1, arg_type, argument)]

    try:
        m = {p1_first, p1_sec}.intersection(p2).pop()
    except:
        print("No M has been found.")
        return

    standard_form = find_stdform(p, argument, arg_type, p1_first, p2, m)
    validity = find_validity(standard_form)
    venn = find_venn(standard_form)

    print("P = " + p, end=", ")
    print("M = " + m, end=", ")
    print("S = " + s)
    print("standard_form: " + standard_form)
    print("For the placement of the areas, please refer to Lecture 2 ppt P.29")
    for key, value in venn.items():
        if key < 8:
            print("Area " + str(key) + ":" + value, end=", ")
        else:
            print("Area " + str(key) + ":" + value)
    print(validity)


def b_part():
    aeio = input("Input your standard form (e.g. AAA1/AIO2): ").upper()
    venn = find_venn(aeio)
    print("For the placement of the areas, please refer to Lecture 2 ppt P.29")
    for key, value in venn.items():
        if key < 8:
            print("Area " + str(key) + ":" + value, end=", ")
        else:
            print("Area " + str(key) + ":" + value)


def c_part():
    existential_import = input("With Existential Import? (YES/NO): ").upper()
    if existential_import in ["YES", "NO"]:
        existential_import = True if existential_import == "YES" else False
        aeio = input("Input your statement (AEIO): ").upper().strip()
        if aeio not in ["A", "E", "I", "O"] or len(aeio) > 1:
            print("Invalid input")
        else:
            value = input("True or False (T/F): ").upper().strip()
            if value not in ["T", "F"]:
                print("Invalid input")
            else:
                value = True if value == "T" else False
                theSquare, relations = square(existential_import, aeio, value)
                for keys, values in theSquare.items():
                    print(keys, values, "because they are", relations[keys])
    else:
        print("Invalid input")


def d_part():
    aeio = aeio_to_senc(
        input("Input your standard form(e.g. AAA1/AOI4): ").upper().strip())
    for index, sentence in enumerate(aeio):
        if index == 2:
            print("----------------")
        print(sentence)


def e_part():
    sen = input(
        "Input your sentence without \"it is not that case that\" : ").strip().split()
    if sen[0] in ["all", "no", "some"] and ("is" in sen or "are" in sen):
        reverse_sen(sen)
    else:
        print("Invalid input")


def typefinder(argument, temp_counter):
    if "all" in argument[temp_counter]:
        return ['A', "is"] if "is" in argument[temp_counter] else ['A', "are"]
    if "no" in argument[temp_counter]:
        return ['E', "is"] if "is" in argument[temp_counter] else ['E', "are"]
    if "not" in argument[temp_counter]:
        return ['O', "not"]
    else:
        return ['I', "is"] if "is" in argument[temp_counter] else ['I', "are"]


def findterms(index, arg_type, argument, *args):
    verb = arg_type[index][1]
    start_of_sec = argument[index].index(verb) + 1
    sec = " ".join(argument[index][start_of_sec:])
    end_of_first = argument[index].index(verb)
    if arg_type[index][0] == 'O' and not args:
        end_of_first -= 1
    first = " ".join(argument[index][1:end_of_first])
    return first, sec


def find_stdform(p, argument, arg_type, p1_first, p2, m):
    m_is_before_verb = [True, True]

    if p in argument[0]:
        p1_position, p2_position = 0, 1
    else:
        p1_position, p2_position = 1, 0
        arg_type[0], arg_type[1] = arg_type[1], arg_type[0]

    m_is_before_verb[p1_position] = True if p1_first == m else False
    m_is_before_verb[p2_position] = True if p2[0] == m else False

    Figure = {
        (True, True): 3,
        (False, False): 2,
        (True, False): 1,
        (False, True): 4
    }

    figure = str(Figure[tuple(m_is_before_verb)])

    standard_form = ''.join(
        arg_type[0][0] + arg_type[1][0] + arg_type[2][0] + figure)
    return standard_form


def find_validity(standard_form):
    validity = "Invalid, the Venn diagram does not contain all the information of the conclusion."
    valid_set = [
        "AAA1", "EAE1", "AEE2", "EAE2", "AEE4", "AII1", "AII3", "IAI3",
        "IAI4", "EIO1", "AOO2", "EIO2", "EIO3", "OAO3", "EIO3"
    ]
    if standard_form in valid_set:
        validity = "Valid, the Venn diagram contains all the information of the conclusion."
    return validity


def find_venn(aeio):
    venn = {x+1: "Non-shaded" for x in range(8)}
    if aeio[0] == 'A':
        if aeio[3] in ["1", "3"]:
            venn[5] = venn[3] = "Shaded"
        else:
            venn[4] = venn[2] = "Shaded"
    elif aeio[0] == 'E':
        venn[7] = venn[6] = "Shaded"
    elif aeio[0] == 'I':
        if venn[6] != "Shaded":
            venn[6] = "X"
        if venn[7] != "Shaded":
            venn[7] = "X"
    else:
        if aeio[3] in ["1", "3"]:
            if venn[5] != "Shaded":
                venn[5] = "X"
            if venn[3] != "Shaded":
                venn[3] = "X"
        else:
            if venn[4] != "Shaded":
                venn[4] = "X"
            if venn[2] != "Shaded":
                venn[2] = "X"

    if aeio[1] == 'A':
        if aeio[3] in ["3", "4"]:
            venn[6] = venn[3] = "Shaded"
        else:
            venn[1] = venn[4] = "Shaded"
    elif aeio[1] == 'E':
        venn[5] = venn[7] = "Shaded"
    elif aeio[1] == 'I':
        if venn[5] != "Shaded":
            venn[5] = "X"
        if venn[7] != "Shaded":
            venn[7] = "X"
    else:
        if aeio[3] in ["3", "4"]:
            if venn[6] != "Shaded":
                venn[6] = "X"
            if venn[3] != "Shaded":
                venn[3] = "X"
        else:
            if venn[1] != "Shaded":
                venn[1] = "X"
            if venn[4] != "Shaded":
                venn[4] = "X"
    return(venn)


def aeio_to_senc(aeio, *args):
    s = []
    term1 = term2 = logic_word1 = logic_word2 = ""
    invalid_input = ["The character", "", "is not accepted"]
    too_long = False
    if len(aeio) > 4:
        too_long = True
        invalid_input[0] = "String longer that 4 characters"
    for i in aeio[:-2]:
        if i not in ["A", "E", "I", "O"]:
            invalid_input[1] = i
            return invalid_input
    if not args and not aeio[3].isdigit():
        invalid_input[1] = aeio[3] + " is not a digit which"
        return invalid_input
    times = 3 if not args else 1
    for i in range(times):
        if aeio[i] == "A":
            logic_word1 = "All"
        elif aeio[i] == "E":
            logic_word1 = "No"
        else:
            logic_word1 = "Some"
        if not args:
            logic_word2 = "are" if aeio[i] != "O" else "are not"
        else:
            logic_word2 = args[2] if aeio[i] not in ["O", "A"] else args[2] + \
                " not" if aeio[i] != "A" else ""
        if not args and i == 0:
            if int(aeio[3]) in [1, 3]:
                term1 = "M"
                term2 = "P"
            else:
                term1 = "P"
                term2 = "M"
        elif i == 1:
            if int(aeio[3]) in [1, 2]:
                term1 = "S"
                term2 = "M"
            else:
                term1 = "M"
                term2 = "S"
        else:
            term1 = "S"
            term2 = "P"
        if args:
            term1, term2 = args[0], args[1]
        s.append(" ".join([logic_word1, term1, logic_word2, term2]))
    return s if not too_long else invalid_input


def setRelations(relations, relation, a, e, i, o):
    relations["A"] = relation[a]
    relations["E"] = relation[e]
    relations["I"] = relation[i]
    relations["O"] = relation[o]


def square(not_empty, aeio, true):
    if not_empty:
        relations = {"A": "", "E": "", "I": "", "O": ""}
        relation = ["self",
                    "contradictories",
                    "contraries",
                    "subcontraries",
                    "subalternates"]
        a = e = i = o = False
        if aeio == 'A':
            if true:
                a = i = True
            else:
                e = i = "logically undetermined"
                o = True
            setRelations(relations, relation, 0, 2, 4, 1)
        elif aeio == 'E':
            if true:
                e = o = True
            else:
                a = o = "logically undetermined"
                i = True
            setRelations(relations, relation, 2, 0, 1, 4)
        elif aeio == 'I':
            if true:
                i = True
                a = o = "logically undetermined"
            else:
                e = o = True
            setRelations(relations, relation, 4, 1, 0, 3)
        else:
            if true:
                o = True
                e = i = "logically undetermined"
            else:
                a = i = True
            setRelations(relations, relation, 1, 4, 3, 0)
        corner = {"A": a, "E": e, "I": i, "O": o}
        return corner, relations
    else:
        contradictory = {'A': 'O', 'E': 'I', 'I': 'E', 'O': 'A'}
        contradictory_corner = contradictory[aeio]
        for i in contradictory.keys():
            contradictory[i] = "logically undetermined" if i != contradictory_corner and i != aeio else not true if i == contradictory_corner else true
        return contradictory


def reverse_sen(sen):
    type = typefinder([sen], 0)
    contradictory = {'A': 'O', 'E': 'I', 'I': 'E', 'O': 'A'}
    term1, term2 = findterms(0, [type], [sen], True)
    aeio = contradictory[type[0]]
    sen = " ".join(aeio_to_senc(aeio, term1, term2, type[1]))
    print(" ".join(sen.split()))


exit = False
while not exit:
    print("\nWhich type of question you are answering?")
    print("A: Categorical Syllogism (The Venn Diagram Method) 定言三段論(范氏圖解法)")
    print("B: The Venn Diagram a specific standard form 特定標準式的范氏圖")
    print("C: Square of Opposition 四角對當關係")
    print("D: Standard form (AEIO) to sentence 標準式轉句子")
    print("E: Reverse the sentence (it is not that case that) 相反句子")
    print("Input EXIT to 離開")

    q_type = input("I am answering: ").upper().strip()

    if q_type == "A":
        a_part()
    elif q_type == "B":
        b_part()
    elif q_type == "C":
        c_part()
    elif q_type == "D":
        d_part()
    elif q_type == "E":
        e_part()
    elif q_type == "EXIT":
        exit = True
    else:
        print("Invalid input.")
