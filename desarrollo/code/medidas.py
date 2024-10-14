import pandas as pd

#Cragar Data
path_concen = "/Users/mauga/Desktop/desarrollo/intermediates/data_combined.csv"
data_concen = pd.read_csv(path_concen)
print("Tamaño del dataset:", data_concen.shape)
gasto_vars = ['alimentos', 'vivienda', 'salud', 'educacion', 'transporte', 'tot_integ', 'ing_cor', 'erogac_tot', 'ubica_geo_mod']
data_combined = data_concen[gasto_vars + ['folioviv']].copy()

# Crear variables de gasto per cápita 
data_combined['gasto_alimentos_pc'] = data_combined['alimentos'] / data_combined['tot_integ']
data_combined['gasto_vivienda_pc'] = data_combined['vivienda'] / data_combined['tot_integ']
data_combined['gasto_salud_pc'] = data_combined['salud'] / data_combined['tot_integ']
data_combined['gasto_educacion_pc'] = data_combined['educacion'] / data_combined['tot_integ']
data_combined['gasto_transporte_pc'] = data_combined['transporte'] / data_combined['tot_integ']


data_combined['gasto_total_basico_pc'] = (data_combined['gasto_alimentos_pc'] +
                                          data_combined['gasto_vivienda_pc'] +
                                          data_combined['gasto_salud_pc'] +
                                          data_combined['gasto_educacion_pc'] +
                                          data_combined['gasto_transporte_pc'])

# Crear una variable que indica vulnerabilidad financiera 
data_combined['vulnerabilidad_financiera'] = data_combined['erogac_tot'] > data_combined['ing_cor']

# Penalización para los hogares en vulnerabilidad financiera 
penalizacion_vulnerabilidad = 0.90
data_combined['gasto_ajustado_pc'] = data_combined['gasto_total_basico_pc']
data_combined.loc[data_combined['vulnerabilidad_financiera'], 'gasto_ajustado_pc'] *= penalizacion_vulnerabilidad

# Calcula la mediana 
linea_pobreza_ajustada = data_combined['gasto_total_basico_pc'].median()
print("Línea de pobreza ajustada:", linea_pobreza_ajustada)
data_combined['es_pobre_ajustado'] = data_combined['gasto_ajustado_pc'] < linea_pobreza_ajustada
porcentaje_pobres = data_combined['es_pobre_ajustado'].mean()
print("Porcentaje de hogares pobres:", porcentaje_pobres * 100, "%")

# Cálculo de las medidas FGT
# FGT0 
fgt0 = data_combined['es_pobre_ajustado'].mean()

# FGT1 
brechas = data_combined.loc[data_combined['es_pobre_ajustado'], 'gasto_ajustado_pc']
fgt1 = (linea_pobreza_ajustada - brechas).sum() / (linea_pobreza_ajustada * len(data_combined))

# FGT2 
fgt2 = ((linea_pobreza_ajustada - brechas) ** 2).sum() / (linea_pobreza_ajustada ** 2 * len(data_combined))

print("FGT0 (Proporción de pobreza):", fgt0 * 100, "%")
print("FGT1 (Brecha de pobreza):", fgt1 * 100, "%")
print("FGT2 (Severidad de pobreza):", fgt2 * 100, "%")


# POR ESTADOS
# Calcular FGT1 por cada 'ubica_geo_mod'
def calcular_fgt1_por_ubicacion(grupo):
    # Seleccionar los hogares pobres
    brechas = grupo.loc[grupo['es_pobre_ajustado'], 'gasto_total_basico_pc']
    # Calcular FGT1 como la brecha promedio de pobreza
    fgt1 = (linea_pobreza_ajustada - brechas).sum() / (linea_pobreza_ajustada * len(grupo))
    return fgt1

# Calcular FGT1 
fgt1_por_ubicacion_actualizada = data_combined.groupby('ubica_geo_mod').apply(calcular_fgt1_por_ubicacion)
print(fgt1_por_ubicacion_actualizada)
#fgt1_por_ubicacion_actualizada.to_csv('/Users/mauga/Desktop/desarrollo/intermediates/fgt1_por_ubicacion_actualizada.csv')
#Por temas de acentos y simplicidad, el archivo fgt1_por_ubicacion_actualizada fue modificado a mano y convertido a xlsx. (To be done in this script...)
