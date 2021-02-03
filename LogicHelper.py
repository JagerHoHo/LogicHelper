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
    validity = "Invalid, the Venn diagram does not contain all the information of the conclusion."
    valid_set = [
        "AAA1", "EAE1", "AEE2", "EAE2", "AEE4", "AII1", "AII3", "IAI3",
        "IAI4", "EIO1", "AOO2", "EIO2", "EIO3", "OAO3", "EIO3"
    ]
    if standard_form in valid_set:
        validity = "Valid, the Venn diagram contains all the information of the conclusion."
    venn = find_venn(standard_form)
    print("standard_form: " + standard_form)
    for key, value in venn.items():
        if key < 8:
            print("Area " + str(key) + ":" + value, end=", ")
        else:
            print("Area " + str(key) + ":" + value)
    print("P = " + p)
    print("M = " + m)
    print("S = " + s)
    print(validity)


def b_part():
    aeio = input("Input your standard_form (e.g. AAA1/AIO2): ").upper()
    find_venn(aeio)


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
                for keys, values in square(existential_import, aeio, value).items():
                    print(keys, values)
    else:
        print("Invalid input")


def d_part():
    aeio = aeio_to_senc(
        input("Input your standard form(e.g. AAA1/AOI4): ").upper().strip())
    for index, sentence in enumerate(aeio):
        if index == 2:
            print("----------------")
        print(sentence)


def typefinder(argument, temp_counter):
    if "all" in argument[temp_counter]:
        return ['A', "is"] if "is" in argument[temp_counter] else ['A', "are"]
    if "no" in argument[temp_counter]:
        return ['E', "is"] if "is" in argument[temp_counter] else ['E', "are"]
    if "not" in argument[temp_counter]:
        return ['O', "not"]
    else:
        return ['I', "is"] if "is" in argument[temp_counter] else ['I', "are"]


def findterms(index, arg_type, argument):
    verb = arg_type[index][1]
    start_of_sec = argument[index].index(verb) + 1
    sec = " ".join(argument[index][start_of_sec:])
    end_of_first = argument[index].index(verb)
    if arg_type[index][0] == 'O':
        end_of_first -= 1
    first = " ".join(argument[index][1:end_of_first])
    return first, sec


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
            venn[5]
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


def aeio_to_senc(aeio):
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
    if not aeio[3].isdigit():
        invalid_input[1] = aeio[3] + " is not a digit which"
        return invalid_input
    for i in range(3):
        if aeio[i] == "A":
            logic_word1 = "All"
        elif aeio[i] == "E":
            logic_word1 = "No"
        else:
            logic_word1 = "Some"
        logic_word2 = "are" if aeio[i] != "O" else "are not"
        if i == 0:
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
        s.append(" ".join([logic_word1, term1, logic_word2, term2]))
    return s if not too_long else invalid_input


def square(not_empty, aeio, true):
    if not_empty:
        a = e = i = o = False
        if aeio == 'A':
            if true:
                a = i = True
            else:
                e = i = "logically undetermined"
                o = True
        elif aeio == 'E':
            if true:
                e = o = True
            else:
                a = o = "logically undetermined"
                i = True
        elif aeio == 'I':
            if true:
                i = True
                a = o = "logically undetermined"
            else:
                e = o = True
        else:
            if true:
                e = i = "logically undetermined"
            else:
                a = i = True
        corner = {"A": a, "E": e, "I": i, "O": o}
        return corner
    else:
        contradictory = {'A': 'O', 'E': 'I', 'I': 'E', 'O': 'A'}
        contradictory_corner = contradictory[aeio]
        for i in contradictory.keys():
            contradictory[i] = "logically undetermined" if i != contradictory_corner else not true
        return contradictory


exit = False
while not exit:
    print("\nWhich type of question you are answering?")
    print("A: Categorical Syllogism 定言三段論")
    print("B: The Venn Diagram Method 范氏圖解法")
    print("C: Square of Opposition 四角對當關係")
    print("D: AEIO to sentence 標準式轉句子")
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
    elif q_type == "EXIT":
        exit = True
    else:
        print("Invalid input.")
