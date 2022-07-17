def a_part():
    print("\nDo not input the So in the conclusion. Words like all, no, some, not, is, are should be in lowercase.")
    print("If they appear more than one time, only the one with logical usefulness should be in lowercase.")
    print("Make the one without logical usefulness fully capital like all cat are things that ARE cute")
    print("No Punctuation should be inputted")
    print("不要輸入結論中的So。具有邏輯意義的的字(all, no, some, not, is, are)都應該用小寫。")
    print("如果出現多於一次，則只有具有邏輯意義的字小寫。")
    print("讓沒有邏輯的那個大寫(如:all cat are things that ARE cute)。")
    print("不要輸入標點符號。")
    argument = []
    arg_part = ["premise 1", "premise 2", "conclusion"]
    arg_type = []
    temp_counter = 0

    while len(argument) < 3:
        argument.append(
            input(f"Input your {arg_part[temp_counter]}: ").strip().split()
        )

        if argument[temp_counter][0] in ["all", "no", "some"] and ("is" in argument[temp_counter] or "are" in argument[temp_counter]):
            arg_type.append(typefinder(argument[temp_counter]))
            temp_counter += 1
        else:
            print(f"Invalid input found in your {arg_part[temp_counter]}")
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

    print(f"P = {p}", end=", ")
    print(f"M = {m}", end=", ")
    print(f"S = {s}")
    print(f"standard_form: {standard_form}")
    print("For the placement of the areas, please refer to Lecture 2 ppt P.29")
    for key, value in venn.items():
        if key < 8:
            print(f"Area {str(key)}:{value}", end=", ")
        else:
            print(f"Area {str(key)}:{value}")
    print(validity)


def b_part():
    aeio = input("Input your standard form(e.g. AAA1/AOI4): ").upper().strip()
    if check_aeio(aeio):
        sen = aeio_to_senc(aeio)
        venn = find_venn(aeio)
        for index, sentence in enumerate(sen):
            if index == 2:
                print("----------------")
            print(sentence)
        print("For the placement of the areas, please refer to Lecture 2 ppt P.29")
        for key, value in venn.items():
            if key < 8:
                print(f"Area {str(key)}:{value}", end=", ")
            else:
                print(f"Area {str(key)}:{value}")
        print(find_validity(aeio))


def c_part():
    existential_import = input("With Existential Import? (YES/NO): ").upper()
    if existential_import == "YES" or existential_import == "NO":
        existential_import = existential_import == "YES"
        aeio = input("Input your statement (AEIO): ").upper().strip()
        if aeio not in ["A", "E", "I", "O"] or len(aeio) > 1:
            print("Invalid input")
        else:
            value = input("True or False (T/F): ").upper().strip()
            if value not in ["T", "F"]:
                print("Invalid input")
            else:
                value = value == "T"
                form = input(
                    "In AEIO form or in sentence form?(AEIO/SEN): ").upper().strip()
                if form not in ["AEIO", "SEN"]:
                    print("Invalid input")
                else:
                    theSquare, relations = square(
                        existential_import, aeio, value)
                    if form == "AEIO":
                        for keys, values in theSquare.items():
                            print(keys, values, "because they are",
                                  relations[keys])
                    else:
                        sen = {"A": "\"All a are b\" is",
                               "E": "\"No a are b\" is",
                               "I": "\"Some a are b\" is",
                               "O": "\"Some a are not b\" is"}
                        for keys, values in theSquare.items():
                            print(sen[keys], values, "because they are",
                                  relations[keys])
    else:
        print("Invalid input")


def d_part():
    sen = input(
        "Input your sentence without \"it is not that case that\" : ").strip().split()
    if sen[0] in ["all", "no", "some"] and ("is" in sen or "are" in sen):
        reverse_sen(sen)
    else:
        print("Invalid input")


def check_aeio(aeio):
    for i, char in enumerate(aeio):
        if len(aeio) > 4:
            print("Invalid input")
        elif i != 3 and char not in ["A", "E", "I", "O"]:
            print(f"{char} is not a valid input")
            return False
        elif i == 3 and (not char.isdigit() or int(char) > 4):
            print(f"{char} is not a valid input")
            return False
    return True


def typefinder(argument):
    if "all" in argument:
        return ['A', "is"] if "is" in argument else ['A', "are"]
    if "no" in argument:
        return ['E', "is"] if "is" in argument else ['E', "are"]
    if "not" in argument:
        return ['O', "not"]
    else:
        return ['I', "is"] if "is" in argument else ['I', "are"]


def findterms(index, arg_type, argument):
    verb = arg_type[index][1]
    start_of_sec = argument[index].index(verb) + 1
    sec = " ".join(argument[index][start_of_sec:])
    end_of_first = argument[index].index(verb)
    if arg_type[index][0] == 'O':
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

    m_is_before_verb[p1_position] = p1_first == m
    m_is_before_verb[p2_position] = p2[0] == m

    Figure = {
        (True, True): 3,
        (False, False): 2,
        (True, False): 1,
        (False, True): 4
    }

    figure = str(Figure[tuple(m_is_before_verb)])

    return ''.join(arg_type[0][0] + arg_type[1][0] + arg_type[2][0] + figure)


def find_validity(standard_form):
    valid_set = [
        "AAA1", "EAE1", "AEE2", "EAE2", "AEE4", "AII1", "AII3", "IAI3",
        "IAI4", "EIO1", "AOO2", "EIO2", "EIO3", "OAO3", "EIO4"
    ]
    return (
        "Valid, the Venn diagram contains all the information of the conclusion."
        if standard_form in valid_set
        else "Invalid, the Venn diagram does not contain all the information of the conclusion."
    )


def find_major(aeio, venn, mood):
    if aeio == 'A':
        if mood in ["1", "3"]:
            venn[5] = venn[3] = "Shaded"
        else:
            venn[4] = venn[2] = "Shaded"
    elif aeio == 'E':
        venn[7] = venn[6] = "Shaded"
    elif aeio == 'I':
        if venn[6] != "Shaded":
            venn[6] = "X"
        if venn[7] != "Shaded":
            venn[7] = "X"
    elif mood in ["1", "3"]:
        if venn[5] != "Shaded":
            venn[5] = "X"
        if venn[3] != "Shaded":
            venn[3] = "X"
    else:
        if venn[4] != "Shaded":
            venn[4] = "X"
        if venn[2] != "Shaded":
            venn[2] = "X"


def find_minor(aeio, venn, mood):
    if aeio == 'A':
        if mood in ["3", "4"]:
            venn[6] = venn[3] = "Shaded"
        else:
            venn[1] = venn[4] = "Shaded"
    elif aeio == 'E':
        venn[5] = venn[7] = "Shaded"
    elif aeio == 'I':
        if venn[5] != "Shaded":
            venn[5] = "X"
        if venn[7] != "Shaded":
            venn[7] = "X"
    elif mood in ["3", "4"]:
        if venn[6] != "Shaded":
            venn[6] = "X"
        if venn[3] != "Shaded":
            venn[3] = "X"
    else:
        if venn[1] != "Shaded":
            venn[1] = "X"
        if venn[4] != "Shaded":
            venn[4] = "X"


def find_venn(aeio):
    venn = {x+1: "Non-shaded" for x in range(8)}
    find_major(aeio[0], venn, aeio[3])
    find_minor(aeio[1], venn, aeio[3])
    return(venn)


def aeio_to_sen(mood, index):
    if index == 0:
        return ("M", "P") if int(mood) in {1, 3} else ("P", "M")
    elif index == 1:
        return ("S", "M") if int(mood) in {1, 2} else ("M", "S")
    else:
        return ("S", "P")


def find_first_word(char):
    return "All" if char == 'A' else "No" if char == 'E' else "Some"


def aeio_to_senc(aeio, *args):
    s = []
    mood = aeio[3] if len(aeio) > 2 else 2
    for i, char in enumerate(aeio):
        if i != 3:
            logic_word1 = find_first_word(char)
            logic_word2 = "are" if aeio[i] != "O" else "are not"
            term1, term2 = (args[0], args[1]) if args else aeio_to_sen(mood, i)
            s.append(" ".join([logic_word1, term1, logic_word2, term2]))
    return s if len(s) != 1 else s[0]


def setRelations(relations, relation, a, e, i, o):
    relations["A"] = relation[a]
    relations["E"] = relation[e]
    relations["I"] = relation[i]
    relations["O"] = relation[o]


def square(not_empty, aeio, true):
    relations = {"A": "", "E": "", "I": "", "O": ""}
    if not_empty:
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
        for i in contradictory:
            contradictory[i] = (
                "logically undetermined"
                if i not in [contradictory_corner, aeio]
                else not true
                if i == contradictory_corner
                else true
            )

            relations[i] = (
                "logically undetermined"
                if i not in [contradictory_corner, aeio]
                else "contradictories"
                if i == contradictory_corner
                else "self"
            )

        return contradictory, relations


def reverse_sen(sen):
    type = typefinder(sen)
    print(f"The sentence is a type {type[0]} sentence")
    term1, term2 = findterms(0, [type], [sen])
    contradictory = {'A': 'O', 'E': 'I', 'I': 'E', 'O': 'A'}
    aeio = contradictory[type[0]]
    print("The reversed from of the sentence is: " +
          aeio_to_senc(aeio, term1, term2))


exit = False
while not exit:
    print("\nWhich type of question you are answering?")
    print("A: Categorical Syllogism (The Venn Diagram Method) 定言三段論(范氏圖解法)")
    print("B: The Venn Diagram and sentence of a specific standard form 特定標準式的范氏圖加句子")
    print("C: Square of Opposition 四角對當關係")
    print("D: Reverse the sentence (it is not that case that) 相反句子")
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
