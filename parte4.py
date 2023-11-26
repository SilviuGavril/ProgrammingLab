def is_float(string):
    try:
        # float() is a built-in function
        float(string)
        return True
    except ValueError:
        return False
        
class CSVFile():
    def __init__(self,name):
        self.name = name
    def get_data (self):
        lista_riga = []
        lista_completa = []
        my_file = open(self.name, 'r')
        if len(my_file.readlines())<1:
            return None
        my_file.seek(0)
        for line in my_file:
            # Faccio lo split di ogni riga sulla virgola
            elements = line.split(',')
            # Se NON sto processando l’intestazione...
            if elements[0] != 'Date' and len(elements)>1: #and is_float(elements[1]) is True:
                lista_riga.append((elements[0:2]))
                lista_completa.extend(lista_riga)
                lista_riga.clear()
        return lista_completa
        
file = CSVFile('shampoo_sales.csv')
print(file.get_data())