ANALYSE_FORMAT = r"^A (.+)$"

def analyse_nick(nick):
    result = ""
    # about length
    if len(nick) == 24:
        result += "- maximum length of nickname\n"
    elif len(nick) == 1:
        result += "- minimum length of nickname\n"
    # something lover
    c_underline = (len([i for i in nick if i == "_"]), "underline", )
    c_bigchar = (len([i for i in nick if ord("A") < ord(i) < ord("Z")]), "uppercase", )
    c_smallchar = (len([i for i in nick if ord("a") < ord(i) < ord("b")]), "lowercase", )
    c_number = (len([i for i in nick if ord("0") < ord(i) < ord("9")]), "number", )
    if c_underline != c_bigchar != c_smallchar != c_number:
        result += "- a %s lover\n" % max(c_underline, c_bigchar, c_smallchar, c_number)[1]
    # same character
    same = True
    last = nick[0]
    for i in nick:
        if i != last:
            same = False
            break
        last = i
    if same:
        result += "- made of same character\n"
    # homo
    if re.findall(r"114.{0,3}514", nick) != []:
        result += "- homo\n"
    # xiaoheizi
    if re.findall(r"(jntm)|(jinitaimei)", nick, re.I) != []:
        result += "- xiaoheizi\n"
    # sad
    if re.findall(r"(pwq)|(qwq)|(pwp)", nick, re.I) != []:
        result += "- sad\n"
    if re.findall(r"QAQ", nick, re.I) != []:
        result += "- quite sad\n"
    # common
    if result == "":
        return "a common one\n"
    return result