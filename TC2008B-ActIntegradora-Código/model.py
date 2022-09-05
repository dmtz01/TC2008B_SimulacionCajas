import mesa
import numpy as np
from agents import Robot, Box, Shelf

# Modelo OrderingBoxes
class OrderingBoxes(mesa.Model):
  def __init__(self, width=20, height=20, K=50, max_time=1000):
    super().__init__()
    self.width = width # Miembro width: Largo del grid (20 por defecto)
    self.height = height # Miembro height: Alto del grid (20 por defecto)
    self.K = K # Miembro K: Cantidad inicial de cajas a ordenar (50 por defecto)
    self.max_time = max_time # Miembro max_time: Tiempo máximo de ejecución (1000 por defecto)
    self.steps_to_finish = 0 # Miembro steps_to_finish: Número de pasos para acomodar las cajas 
    self.steps = 0 # Miembro steps: Cantidad de pasos actual

    self.schedule = mesa.time.SimultaneousActivation(self)
    self.grid = mesa.space.SingleGrid(self.width, self.height, torus=False)
    self.datacollector = mesa.DataCollector()

    # Creación y colocación aleatoria de los 5 Robots
    num_of_robots = 0
    while (num_of_robots < 5):
      x = self.random.randrange(self.width)
      y = self.random.randrange(1, self.height)
      if self.grid.is_cell_empty([x, y]) == True:
        num_of_robots += 1
        robot = Robot(self.next_id(), (x, y), self, self.height, self.width)
        self.grid.place_agent(robot, (x, y))
        self.schedule.add(robot)
    
    # Creación y colocación de los estantes
    for i in range(0, self.width, 1):
      x = i
      y = 0
      shelf = Shelf(self.next_id(), (x, y), self)
      self.grid.place_agent(shelf, (x, y))
      self.schedule.add(shelf)
    
    # Creación y colocación aleatoria de las cajas
    num_of_boxes = 0
    while (num_of_boxes < self.K):
      x = self.random.randrange(self.width)
      y = self.random.randrange(2, self.height)
      if self.grid.is_cell_empty([x, y]) == True:
        num_of_boxes += 1
        box = Box(self.next_id(), (x, y), self)
        self.grid.place_agent(box, (x, y))
        self.schedule.add(box)

    self.running = True
    self.datacollector.collect(self)

  def step(self):
    self.steps += 1

    # Si la cantidad actual de pasos supera el tiempo máximo, se detiene la ejecución
    if self.steps > self.max_time:
      return

    # Eliminación de las cajas ya cargadas por los Robots
    self.kill_agents = []
    self.schedule.step()
    for x in self.kill_agents:
      self.grid.remove_agent(x)
      self.schedule.remove(x)
      self.kill_agents.remove(x)
    self.datacollector.collect(self)

    # Reporte del estado de las cajas, estantes y Robots
    status = self.get_grid(self.steps)

    self.K = status[3] 

    # Si aún hay cajas desordenadas, el conteo de pasos continúa
    if status[0] >= 0 and status[1] < self.K:
      self.steps_to_finish += 1

    # Se ya no hay cajas por ordenar, se detiene la ejecución y se muestran
    # los resultados de la ejecución 
    elif status[0] == 0 and status[1] == self.K:
      print("All boxes ordered\nTotal steps: " + str(self.steps_to_finish))
      for cell in self.grid.coord_iter():
        agent, x, y = cell
        if isinstance(agent, Robot):
          print("Robot ID: " + str(agent.unique_id) + ", movements: " + str(agent.movements))
      self.steps = self.max_time + 1
      return

    # Si se ha alcanzado el límite de tiempo, se detiene la ejecución y se muestran
    # los resultados de la ejecución
    if self.steps == self.max_time:
      print("Maximum time reached")
      print("Remaining boxes: " + str(status[0]) + "\nOrdered boxes: " + str(status[1]) + "\nRobots carrying boxes: " + str(status[2]))
      for cell in self.grid.coord_iter():
        agent, x, y = cell
        if isinstance(agent, Robot):
          print("Robot ID: " + str(agent.unique_id) + ", movements: " + str(agent.movements))
      return

  # Función get_grid: Crea un grid para asignar valores que identifiquen a los estantes,
  # cajas y Robots con sus estados actuales
  def get_grid(model, steps):
    remaining_boxes = 0
    ordered_boxes = 0
    robots_carrying_boxes = 0
    total_boxes = 0
    
    grid = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
      agent, x, y = cell
      if isinstance(agent, Robot):
        if agent.charging == 0:
          grid[x][y] = 10
        elif agent.charging == 1:
          grid[x][y] = 11
          robots_carrying_boxes += 1
      elif isinstance(agent, Box):
        grid[x][y] = 1
        remaining_boxes += 1
      elif isinstance(agent, Shelf):
        if agent.boxes == 0:
          grid[x][y] = 100
        elif agent.boxes == 1:
          grid[x][y] = 101
          ordered_boxes += 1
        elif agent.boxes == 2:
          grid[x][y] = 102
          ordered_boxes += 2
        elif agent.boxes == 3:
          grid[x][y] = 103
          ordered_boxes += 3
        elif agent.boxes == 4:
          grid[x][y] = 104
          ordered_boxes += 4
        elif agent.boxes == 5:
          grid[x][y] = 105
          ordered_boxes += 5
      else:
        grid[x][y] = 0

    total_boxes = remaining_boxes + ordered_boxes + robots_carrying_boxes
    status = [remaining_boxes, ordered_boxes, robots_carrying_boxes, total_boxes]      
    return status
      
      