import pandas as pd

# Cargar Data
path_concen = "/Users/mauga/Desktop/desarrollo/data/concentradohogar.csv"
data_concen = pd.read_csv(path_concen)

# Convertir 'ubica_geo' a cadena para realizar las operaciones
data_concen['ubica_geo'] = data_concen['ubica_geo'].astype(str)

# Aplicar la lógica para modificar 'ubica_geo'
def modificar_ubica_geo(valor):
    if len(valor) == 4 and valor[0] in '123456789':
        return valor[0]  # Tomar solo el primer número
    else:
        return valor[:2]  # Tomar los primeros dos números

# Aplicar la función a la columna 'ubica_geo'
data_concen['ubica_geo_mod'] = data_concen['ubica_geo'].apply(modificar_ubica_geo)


data_concen.to_csv('/Users/mauga/Desktop/desarrollo/intermediates/data_combined.csv', index=False)
