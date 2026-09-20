from pendulumLib import Pendulum

pendulumOne = Pendulum(pivot=(640, 360), mass=3, length=150, width=3, colour="Blue", starting_angle=190, damping=0.05, gravity=9.81)
pendulumOne.SHMSimulation()
