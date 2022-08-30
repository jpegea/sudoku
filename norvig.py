def prod_cart(X, Y):
    """Producte cartesià de dos conjunts de strings."""
    return [x+y for x in X for y in Y]


# String amb els digits de l'1 al 9.
digits = '123456789'

# String amb les files i les columnes
files = "ABCDEFGHI"
columnes = digits

# Fem la quadrícula
caselles = prod_cart(files, columnes)

grups = ([prod_cart(files, c) for c in columnes] +
         [prod_cart(f, columnes) for f in files] +
         [prod_cart(f, c) for f in ('ABC', 'DEF', 'GHI')
          for c in ('123', '456', '789')])

grups_de = dict((c, [g for g in grups if c in g]) for c in caselles)

veins = dict((c, set(sum(grups_de[c], [])) - set([c]))
             for c in caselles)


# TEST PER A COMPROVAR QUE FUNCIONA CORRECTAMENT
def test():
    assert len(caselles) == 81
    assert len(grups) == 27
    assert all(len(grups_de[c]) == 3 for c in caselles)
    assert veins['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print("Oki")


def sudoku_valors(sudoku):
    """Converteix l'entrada del sudoku en un diccionari on la clau és
    la casella i el valor és el conjunt de valors possibles que pot
    prendre la casella.  Torna False si s'ha trobat alguna
    contradicció."""

    valors = dict((c, digits) for c in caselles)
    for c, v in llegir_sudoku(sudoku).items():
        if v in digits and not assignar(valors, c, v):
            return False

    return valors


def llegir_sudoku(sudoku):
    """Converteix l'entrada del sudoku en un diccionari on la clau és
    la casella i el valor és el seu valor (valga la redundància)."""

    asignats = [a for a in sudoku if a in digits or a in '0.']
    assert len(asignats) == 81
    return dict(zip(caselles, asignats))


def assignar(valors, c, v):
    """Asigna un valor a una casella i elimina tots els altres
    possibles valors i es propaga."""

    altres_valors = valors[c].replace(v, '')
    if all(eliminar(valors, c, v2) for v2 in altres_valors):
        return valors
    else:
        return False


def eliminar(valors, c, v):
    """Elimina v de valors[c] i fa la magia."""

    if v not in valors[c]:
        return valors  # Ja l'ha eliminat perquè directament no estava.

    valors[c] = valors[c].replace(v, '')

    if len(valors[c]) == 0:
        return False
    elif len(valors[c]) == 1:
        v2 = valors[c]
        if not all(eliminar(valors, c2, v2) for c2 in veins[c]):
            return False

    for g in grups_de[c]:
        llocs = [c for c in g if v in valors[c]]
        if len(llocs) == 0:
            return False
        elif len(llocs) == 1:
            if not assignar(valors, llocs[0], v):
                return False
    return valors


def mostrar(valors):
    "Display these values as a 2-D grid."
    width = 1 + max(len(valors[c]) for c in caselles)

    for f in files:
        if f == 'D' or f == 'G':
            print("-"*width*3 + "+-" +
                  "-"*width*3 + "+" +
                  "-"*width*3)
        for c in columnes:
            if c == '4' or c == '7':
                print("|", end=' ')
            print(valors[f+c].center(width), end='')

        print()


def solucionar(sudoku):
    return buscar(sudoku_valors(sudoku))


def buscar(valors):
    "Resolem per 'fuerza bruta'."
    if valors is False:
        return False
    if all(len(valors[c]) for c in caselles):
        return valors  # Solucionat!

    n, c = min((len(valors[c]), c) for c in caselles if len(valors[c]) > 1)

    return algun(buscar(assignar(valors.copy, c, v)) for v in valors[c])


def algun(possibles):
    "Retorna algun element de possibles que siga possible."
    for p in possibles:
        if p:
            return p
    return False


sudo = "0050102000007000000240009500073000056000000013000084000790006800009000\
00003040100"

mostrar(llegir_sudoku(sudo))
print("\n")
mostrar(sudoku_valors(sudo))
print("\n")
mostrar(solucionar(sudo))
