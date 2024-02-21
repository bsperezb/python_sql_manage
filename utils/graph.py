import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import t

def plot_histogram_and_std(array):
    # Crear un DataFrame de Pandas con los datos
    df = pd.DataFrame(array, columns=['Datos'])

    # Calcular la desviación estándar
    std_deviation = np.std(array)

    # Imprimir la desviación estándar
    print(f"La desviación estándar es: {std_deviation}")

    # Crear un histograma
    plt.hist(array, bins=50, color='blue', edgecolor='black')

    # Añadir etiquetas y título
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de Frecuencias')

    # Establecer el paso en el eje x (cada 2 unidades)
    plt.xticks(np.arange(min(array), max(array)+1, step=2))

    # Mostrar la gráfica
    plt.show()

def calcular_intervalo_confianza(datos, confianza=0.95):
    # Calcular la media y la desviación estándar de los datos
    media = np.mean(datos)
    desviacion_estandar = np.std(datos, ddof=1)  # ddof=1 para usar la desviación estándar muestral

    # Calcular el tamaño de la muestra
    n = len(datos)

    # Calcular el error estándar de la media
    error_estandar = desviacion_estandar / np.sqrt(n)

    # Calcular el valor crítico de t para el intervalo de confianza
    valor_critico_t = t.ppf((1 + confianza) / 2, df=n - 1)

    # Calcular los límites del intervalo de confianza
    margen_error = valor_critico_t * error_estandar
    print('margen_error', margen_error)
    limite_inferior = media - margen_error
    limite_superior = media + margen_error
    print('Limite superir: ',limite_superior )
    print('Limite inferior: ',limite_inferior)

    return limite_inferior, limite_superior

def bootstrap_ci(data, n_iterations=1000, alpha=0.05):
    # Inicializar un array para almacenar los resultados del bootstrap
    bootstrap_samples = np.empty(n_iterations)

    # Realizar el bootstrap
    for i in range(n_iterations):
        bootstrap_sample = np.random.choice(data, size=len(data), replace=True)
        bootstrap_samples[i] = np.mean(bootstrap_sample)

    # Calcular los límites del intervalo de confianza
    lower_bound = np.percentile(bootstrap_samples, alpha / 2 * 100)
    upper_bound = np.percentile(bootstrap_samples, (1 - alpha / 2) * 100)

    print('Limite superir: ',upper_bound )
    print('Limite inferior: ',lower_bound)

    return lower_bound, upper_bound
