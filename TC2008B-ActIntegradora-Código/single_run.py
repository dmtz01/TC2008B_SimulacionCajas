from model import OrderingBoxes

# Ejecución individual del modelo sin representación visual

width = 20 # Largo del grid
height = 20 # Alto del grid
K = 50 # Cantidad de cajas a ordenar
max_time = 500 # Tiempo máximo de ejecución

# Asignación de parámetros al modelo
model = OrderingBoxes(width, height, K, max_time)

# Ejecución del modelo
for i in range(max_time):
  model.step()