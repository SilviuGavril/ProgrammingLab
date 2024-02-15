class ExamException(Exception):
    pass

#verifica la validità di ogni elemento della lista
def validate_data(data):
    if data is None:
        raise ExamException('Data is None')
    if not isinstance(data, list):
        raise ExamException('Data in time_series is not a list')
    if len(data) == 0:
        raise ExamException('Data is empty')
    if None in data:
        raise ExamException('There is at least a None value in data')
    if data[0] is None or data[1] is None:
        raise ExamException('There is at least a None value in Time Series')
    if not isinstance(data[0], str):
        raise ExamException('Data[0] is not a string')
    if not isinstance(data[1], int):
        raise ExamException('Data[1] is not an int')
    
def compute_increments(time_series, first_year, last_year):
    #verifico che time_series sia valida
    if time_series is None:
        raise ExamException('Time Series is None')
    if not isinstance(time_series, list):
        raise ExamException('Time Series is not a list')
    if len(time_series) == 0:
        raise ExamException('Time Series is empty')
    if None in time_series:
        raise ExamException('There is at least a None value in Time Series')
    #verifico validità anni passati
    if first_year is None or last_year is None:
        raise ExamException('One of the year is None')
    if not isinstance(first_year, str) or not isinstance(last_year, str):
        raise ExamException('Years are not strings')
    #converto gli anni da string a interi, se non ci riesco alzo un'eccezione
    try:
        first_year = int(first_year)
        last_year = int(last_year)
    except:
        raise ExamException('Cannot convert years strings into integers')
    if last_year <= first_year:
        raise ExamException('First year cannot be greater or equal to Last year')
    if first_year not in range(1949, 1960) or last_year not in range(1949, 1960):
        raise ExamException('Years out of accepted range 1949-1960')

    # Creo un dizionario per memorizzare i dati annuali
    yearly_data = {}
    
    for data in time_series:
        #verifico che questa lista contenga i dati aspettati
        validate_data(data)
        
        #prendo solo la parte prima del car '-' del primo elemento della lista "data" e la trasformo in int
        year = int(data[0].split('-')[0])
        
        #prendo in considerazione solo gli anni nel range passato come argomenti
        if first_year <= year <= last_year:
            #verifico se l'anno è già presente nel dizionario, altrimenti lo aggiungo
            if year not in yearly_data:
                yearly_data[year] = []
            #aggiungo il nr di passeggeri per l'anno in esame
            yearly_data[year].append(data[1])

    # Media: per ogni anno calcolo la somma e divido per il nr di elementi presenti
    #Loop through both keys and values, by using the items() method:
    #yearly_averages = {year: sum(values) / len(values) for year, values in yearly_data.items()}
    yearly_averages={}
    for year, values in yearly_data.items():
        yearly_averages[year] = (sum(values) / len(values))

    #verifico che gli anni estremi passati come argomenti sono presenti nel dizionario
    if first_year not in yearly_averages or last_year not in yearly_averages:
        raise ExamException('At least one year passed as argument is not in the data')
        
    # Calcolo gli incrementi e li salvo in un dizionario
    increments = {}
    #last_year +1 non incluso da "range"
    for year in range(first_year + 1, last_year + 1):
        if (year - 1) in yearly_averages:
            #cerco il prossimo anno presente nel dizionario
            for next_year in range(year, last_year + 1):
                if next_year in yearly_averages:
                    #salvo il dato e fermo il loop appena trovato un anno con dati
                    increments[f"{year-1}-{next_year}"] = yearly_averages[
                        next_year] - yearly_averages[year - 1]
                    break
    return increments

class CSVTimeSeriesFile:

    def __init__(self, name):
        if isinstance(name, str) is False:
            raise ExamException('Name "{}" not a string'.format(name))
        else:
            self.name = name

    def get_data(self):
        try:
            #questa funziona mi garantisce anche la chiusura del file
            with open(self.name, 'r') as file:
                lines = file.readlines()
        except:
            raise ExamException('Impossible to open the file')
        time_series = []
        last_date = None
        for line in lines:

            #mi salvo i valori divisi per virgola e tolgo eventuali spazi
            fields = line.strip().split(',')

            #verifico di avere almeno 2 elementi nella riga
            if len(fields) < 2:
                continue

            #mi salvo solo i primi 2 elementi della riga
            date, passengers = fields[:2]

            #verifica di non processare la prima riga, un pò paranoico questo try
            try:
                if date == "date":
                    continue
            except:
                continue

            #verifico che il timestamp sia maggiore del precedente
            if last_date is not None and date <= last_date:
                raise Exception("Timestamp not ordered or duplicated")

            try:
                #estraggo e trasformo in int l'anno
                year = int(date.split('-')[0])
                #verifico che l'anno sia all'interno del range atteso altrimenti ignoro
                if year not in range(1949, 1960):
                    continue
            except:
                continue
            try:
                #verifico che i passengeri siano maggiori di zero
                passengers = int(passengers)
                if passengers < 1:
                    continue
            except ValueError:
                continue

            time_series.append([date, passengers])
            last_date = date

        return time_series