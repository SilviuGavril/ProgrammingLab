def sum_csv(file_name):
# Inizializzo una lista vuota per salvare i valori
    sum=0
    # Apro e leggo il file, linea per linea
    my_file = open(file_name, 'r')
    #print("numero righe:",number_of_lines)
    if len(my_file.readlines())<2:
        return None
    my_file.seek(0)
    for line in my_file:
        # Faccio lo split di ogni riga sulla virgola
        elements = line.split(',')
        # Se NON sto processando l’intestazione...
        if elements[0] != 'Date' and len(elements)>1 and is_float(elements[1]) is True:
            value = float(elements[1])
            sum+=value
    return sum
def is_float(string):
    try:
        # float() is a built-in function
        float(string)
        return True
    except ValueError:
        return False
print(sum_csv('shampoo_sales.csv'))
