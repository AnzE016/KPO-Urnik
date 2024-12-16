# fuzzy_podobnost.py
from thefuzz import fuzz

def fuzzy_podobnost(koledar,baza):
    return fuzz.ratio(koledar, baza)
#return fuzz.partial_ratio(koledar, baza)

def main():
    print('Podobnost ', fuzzy_podobnost('AAAABB','AAAAAACc'))

if __name__ == "__main__":
    main()

