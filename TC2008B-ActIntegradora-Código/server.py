import mesa
from model import OrderingBoxes
from agents import Robot, Box, Shelf

# Definición de la representación del modelo
def OrderingBoxesPortrayal(agent):
  if agent is None:
    return

  portrayal = {}

  if type(agent) is Robot:
    if agent.charging == 0:
      portrayal["Color"] = ["#0000AA", "#0000AA", "#0000AA"]
    elif agent.charging == 1:
      portrayal["Color"] = ["#AA00AA", "#AA00AA", "#AA00AA"]
    portrayal["Shape"] = "circle"
    portrayal["Filled"] = "true"
    portrayal["Layer"] = 0
    portrayal["r"] = 1

    return portrayal

  elif type(agent) is Box:
    portrayal["Color"] = ["#9B673C", "#9B673C", "#9B673C"]
    portrayal["Shape"] = "rect"
    portrayal["Filled"] = "true"
    portrayal["Layer"] = 0
    portrayal["w"] = 0.5
    portrayal["h"] = 0.5

    return portrayal

  elif type(agent) is Shelf:
    if agent.boxes == 0:
      portrayal["Color"] = ["#C5C6D0", "#C5C6D0", "#C5C6D0"]
    elif agent.boxes == 1:
      portrayal["Color"] = ["#ADADC9", "#ADADC9", "#ADADC9"]
    elif agent.boxes == 2:
      portrayal["Color"] = ["#696880", "#696880", "#696880"]
    elif agent.boxes == 3:
      portrayal["Color"] = ["#3E3D53", "#3E3D53", "#3E3D53"]
    elif agent.boxes == 4:
      portrayal["Color"] = ["#41424C", "#41424C", "#41424C"]
    elif agent.boxes == 5:
      portrayal["Color"] = ["#000000", "#000000", "#000000"]
    portrayal["Shape"] = "rect"
    portrayal["Filled"] = "true"
    portrayal["Layer"] = 0
    portrayal["w"] = 1
    portrayal["h"] = 1

    return portrayal

canvas_element = mesa.visualization.CanvasGrid(OrderingBoxesPortrayal, 20, 20, 500, 500)

server = mesa.visualization.ModularServer(OrderingBoxes, [canvas_element], "Ordering Boxes")

server.port = 8521