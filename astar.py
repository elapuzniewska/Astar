
class Node():
    def __init__(self, rodzic=None, punkt=None):
        self.rodzic = rodzic
        self.punkt = punkt

        # poczatkowo wszystkie wartosci na 0
        # bo przy towrzeniu wezla ustawiam ich wartosci
        self.g = 0
        self.h = 0
        self.f = 0

    # ten kod wywolywany gdy
    # if current_node == end_node:
    def __eq__(self, other):
        return self.punkt == other.punkt


class Astar():
    def __init__(self, plansza):
        self.plansza = plansza
        # inicjalizacja wartosci
        # poczatkowo wszystkie na 0
        self.start = 0
        self.koniec = 0

        self.znajdz_start()
        self.znajdz_koniec()

    # metoda do szukania startu
    # start na planszy jest oznaczony litera 'S'
    def znajdz_start(self):
        for x, linia in enumerate(self.plansza):
            for y, kolumna in enumerate(linia):
                if kolumna == 'S':
                    self.start = (x, y)

    # metoda do szukania mety
    # meta oznaczona jest litera 'K'
    def znajdz_koniec(self):
        for x, linia in enumerate(self.plansza):
            for y, kolumna in enumerate(linia):
                if kolumna == 'K':
                    self.koniec = (x, y)

    # metoda do szukania sasiadow
    # uwzglednia ruch gora, dol, prawo, lewo
    # sprawda czy punkt jest na zamknietej liscie
    # sprawdza czy punkt jest na otwartej liscie, jesli jest to modyfikuje g
    def znajdz_sasiadow(self, current_node, end_node, otwarta_lista, zamknieta_lista):
        sasiedzi = []
        plansza_len = len(self.plansza)

        # petla zeby uzyskac punkty gora, dol, lewo, prawo
        for new_punkt in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_punkt = (current_node.punkt[0] + new_punkt[0], current_node.punkt[1] + new_punkt[1])

            # sprawdz czy punkt jest na planszy
            if node_punkt[0] > (plansza_len - 1) or node_punkt[0] < 0 or node_punkt[1] > (
                    len(self.plansza[plansza_len - 1]) - 1) or node_punkt[1] < 0:
                # idz do nastepnej iteracji
                continue

            # sprawdz czy punkt jest N
            # jesli nie to idz do nastepnej iteracji
            if self.plansza[node_punkt[0]][node_punkt[1]] != 'N':
                if self.plansza[node_punkt[0]][node_punkt[1]] != 'S':
                    if self.plansza[node_punkt[0]][node_punkt[1]] != 'K':
                        # idz do nastepnej iteracji
                        continue

            # stworzy nowy Node
            new_node = Node(current_node, node_punkt)

            # zmienna sterujaca na potrzeby sprawdzenia czy punkt jest na liscie zamknietej
            closed = False
            # sprawdzenie czy punkt jest na zamknietej liscie
            for elem in zamknieta_lista:
                if new_node == elem:
                    closed = True
            if closed:
                continue

            # zmienna sterujaca na potrzeby sprawdzenia czy punkt jest na liscie otwartej
            open = False
            # spradzenie czy punkt jest na otwartej liscie
            for open_node in otwarta_lista:
                if new_node == open_node:
                    open_node.g += 1
                    open = True
            if open:
                continue

            # zalozenie ze do g zawsze dodaje sie jeden
            # g to droga przebyta od poczatku
            new_node.g = current_node.g + 1

            # wyliczenie H = wartosc bezwzgledna odleglosci od x + wartosc bezwzgledna odleglosci od y
            new_node.h = abs(end_node.punkt[0] - new_node.punkt[0]) + abs(end_node.punkt[1] - new_node.punkt[1])

            # wyliczenie kosztu
            new_node.f = new_node.g + new_node.h

            # dodaj Node do sasiadow
            sasiedzi.append(new_node)

        return sasiedzi

    # metoda do znalezienia najnizszego f
    def znajdz_najnizsze_f(self, otwarta_lista):
        # pierwszy element z listy
        punkt_index = 0
        # float("inf") to nieskonczonosc
        f = float("inf")
        punkt = 0

        for index, item in enumerate(otwarta_lista):
            if item.f < f:
                f = item.f
                punkt = item
                punkt_index = index

        return (punkt_index, punkt)

    # metoda do szukania drogi
    def znajdz_droge(self):
        if self.start == 0:
            print("Oznacz punkt start!")
            return None

        if self.koniec == 0:
            print("Oznacz punkt konca!")
            return None

        # stworz Node startowy
        start_node = Node(None, self.start)
        # stworz Node koncowy
        end_node = Node(None, self.koniec)

        # inicjuj otwarta i zamknieta liste
        otwarta_lista = []
        zamknieta_lista = []

        # dodaj do otwartej liscie Node startowy
        otwarta_lista.append(start_node)

        # wez pierwszy element z listy
        current_node = otwarta_lista[0]
        current_index = 0

        # petla dopoki cos jest w liscie otwartej
        while otwarta_lista:
            # w znajdz_najnizsze_f zwaracam dwie wartosci
            najnizsze_f = self.znajdz_najnizsze_f(otwarta_lista)
            current_index = najnizsze_f[0]
            current_node = najnizsze_f[1]

            # jesli znaleziono koniec
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.punkt)
                    current = current.rodzic
                return path[::-1]  # Return reversed path

            # usun z otwartej listy, usun z zamknietej listy
            otwarta_lista.pop(current_index)
            zamknieta_lista.append(current_node)

            # znajdz_sasiadow() znajdzie dostepne punkty planszy
            sasiedzi = self.znajdz_sasiadow(current_node, end_node, otwarta_lista, zamknieta_lista)
            for punkt in sasiedzi:
                # dodaj punkt do otwartej listy
                otwarta_lista.append(punkt)


def main():
    # legenda:
    # S - start
    # B - bariera
    # K - koniec
    # N - nic
    plansza = [['S', 'B', 'N', 'N', 'B', 'N', 'N', 'N', 'N', 'N'],
               ['N', 'B', 'B', 'B', 'B', 'N', 'N', 'N', 'N', 'N'],
               ['N', 'N', 'N', 'N', 'B', 'N', 'N', 'N', 'N', 'N'],
               ['N', 'N', 'B', 'N', 'B', 'N', 'N', 'N', 'N', 'N'],
               ['B', 'B', 'B', 'N', 'B', 'N', 'N', 'N', 'N', 'N'],
               ['N', 'N', 'N', 'N', 'B', 'N', 'N', 'N', 'N', 'N'],
               ['N', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'N', 'N'],
               ['N', 'N', 'N', 'N', 'B', 'B', 'N', 'N', 'N', 'N'],
               ['B', 'B', 'B', 'N', 'B', 'B', 'N', 'N', 'B', 'N'],
               ['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'B', 'K']]

    astar = Astar(plansza)
    droga = astar.znajdz_droge()

    if droga:
        # przypisanie do planszy punktow drogi jako X
        for x, linia in enumerate(plansza):
            for y, _ in enumerate(linia):
                for element in droga:
                    if element[0] == x and element[1] == y:
                        if plansza[x][y] != 'S' and plansza[x][y] != 'K':
                            # oznacz element drogi w liscie plansza jako X
                            plansza[x][y] = 'X'

        # rozrysowanie drogi
        for linia in plansza:
            wiersz = ""
            for kolumna in linia:
                if kolumna == 'X':
                    # kolor zielony
                    wiersz += "\033[92m[" + kolumna + "]\033[0m"
                elif kolumna == 'S' or kolumna == 'K':
                    # bold
                    wiersz += "\033[1m[" + kolumna + "]\033[0m"
                elif kolumna == 'B':
                    # kolor czerwony
                    wiersz += "\033[91m[" + kolumna + "]\033[0m"
                else:
                    wiersz += "[" + kolumna + "]"
            print(wiersz)
    else:
        print('Nie znaleziono drogi')


if __name__ == '__main__':
    main()
