import logging
import time
from datetime import datetime, timedelta

# Configurar el sistema de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('berkeley_logs.log'), logging.StreamHandler()])

# Nodo principal
class MainNode:
    def __init__(self):
        self.node_id = "Principal"
        self.nodes = []
        self.current_time = None
    
    def add_node(self, node):
        self.nodes.append(node)
    
    def synchronize_clocks(self):
        # Obtiene la hora actual del nodo principal
        self.current_time = datetime.now()
        logging.info(f"Nodo {self.node_id}: Hora actual - {self.current_time}")
        
        # Envía la hora actual a cada nodo y recibe los ajustes de tiempo
        time_adjustments = {}
        for node in self.nodes:
            adjustment = node.receive_time(self.current_time)
            time_adjustments[node] = adjustment
            logging.info(f"Nodo {self.node_id}: Ajuste recibido de Nodo {node.node_id} - {adjustment}")
        
        # Calcula el promedio de los ajustes de tiempo
        sum_adjustments = sum(time_adjustments.values(), timedelta())
        average_adjustment = sum_adjustments / len(time_adjustments)
        logging.info(f"Nodo {self.node_id}: Ajuste promedio calculado - {average_adjustment}")
        
        # Envía el ajuste promedio a cada nodo
        for node in self.nodes:
            node.adjust_time(average_adjustment)

# Nodo
class Node:
    def __init__(self, node_id, main_node):
        self.node_id = node_id
        self.main_node = main_node
        self.time_adjustment = timedelta()
    
    def start_clock_synchronization(self, interval):
        while True:
            self.main_node.synchronize_clocks()
            time.sleep(interval)
    
    def receive_time(self, current_time):
        # Calcula el ajuste de tiempo basado en la diferencia entre la hora actual y la recibida
        received_time = datetime.now()
        adjustment = current_time - received_time
        self.time_adjustment = adjustment
        return self.time_adjustment
    
    def adjust_time(self, average_adjustment):
        # Ajusta el reloj sumando el valor del ajuste promedio
        adjusted_time = datetime.now() + average_adjustment
        logging.info(f"Nodo {self.node_id}: Hora ajustada - {adjusted_time}")
    
    def get_current_time(self):
        # Obtiene la hora actual ajustada
        current_time = datetime.now() + self.time_adjustment
        logging.info(f"Nodo {self.node_id}: Hora actual - {current_time}")

# Ejemplo de uso
if __name__ == "__main__":
    # Crea el nodo principal
    main_node = MainNode()
    
    # Crea los nodos
    node1 = Node(1, main_node)
    node2 = Node(2, main_node)
    node3 = Node(3, main_node)
    
    # Agrega los nodos al nodo principal
    main_node.add_node(node1)
    main_node.add_node(node2)
    main_node.add_node(node3)
    
    # Inicia la sincronización periódica de los nodos con el nodo principal (intervalo de 5 segundo)
    node1.start_clock_synchronization(5)
    node2.start_clock_synchronization(5)
    node3.start_clock_synchronization(5) 