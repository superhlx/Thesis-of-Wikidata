import pgf

gr = pgf.readPGF("Foods.pgf")  
eng = gr.languages["FoodsEng"]  


def parseSentence(sentence):
    i = eng.parse(sentence)  
    _, expr = next(i)  
    return expr

def isSingular(expr):
    fun, children = expr.unpack()
    if fun == "Pred": 

        np_fun, _ = children[0].unpack() 

        return np_fun in ["This", "That"]
    
    return False

def toPlural(tree):
    fun, children = tree.unpack()

    if fun == "Pred":
        np_fun, np_children = children[0].unpack()


        if np_fun == "This":  
            new_np = pgf.Expr("These", np_children) 
            return pgf.Expr("Pred", [new_np, children[1]])

        elif np_fun == "That":  
            new_np = pgf.Expr("Those", np_children) 
            return pgf.Expr("Pred", [new_np, children[1]])

    return pgf.Expr(fun, [toPlural(child) for child in children])


def addVery(tree):
    fun, children = tree.unpack()

    if fun == "Pred":
        return pgf.Expr("Pred", [children[0], pgf.Expr("Very", [children[1]])]) 


def transformSentence(sentence):
    expr = parseSentence(sentence)  
    if isSingular(expr):
        new_expr = toPlural(expr) 
    else:
        new_expr = addVery(expr)  

    return eng.linearize(new_expr)  



# ---parse and unpack
# A pgf file is a compiled grammar file , which contains both abstract and concrete syntaxes of a GF grammar,
# parse() converts a natural language sentence into a pgf.Expr syntax tree.
# unpack() extracts the constructor name and child expressions from a pgf.Expr.

# # Load grammar
# gr = pgf.readPGF("MiniLang.pgf")
# eng = gr.languages["MiniLangEng"]

# # Parse sentence
# i = eng.parse("I see you")
# prob, expr = next(i)  # Get first parse result
# print("Parsed Expression:", expr)

# # Unpack expression
# fun_name, children = expr.unpack()
# print("Constructor:", fun_name)
# print("Children:", children)

# # Further unpack child expression
# sub_fun_name, sub_children = children[0].unpack()
# print("Sub Constructor:", sub_fun_name)
# print("Sub Children:", sub_children)

# Parsed Expression: UttS (UsePresCl PPos (PredVP (UsePron i_Pron) (ComplV2 see_V2 (UsePron youSg_Pron))))
# Constructor: UttS
# Children: [<pgf.Expr at 0x...>]
# Sub Constructor: UsePresCl
# Sub Children: [<pgf.Expr at 0x...>, <pgf.Expr at 0x...>]
