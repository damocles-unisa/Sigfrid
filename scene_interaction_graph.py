import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class SceneInteractionGraph(object):

    def __init__(self, node_labels = set(), edge_labels = set()):
        self.G = nx.DiGraph()
        self.node_labels = node_labels
        self.edge_labels = edge_labels
        self.action_conflict_edges = []  # Conflict
        self.action_block_edges = []  # Blocking
        self.trigger_block_edges = []  # Blocking
        self.action_duplicate_edges = []  # Duplication
        self.rule_chaining_edges = [] # Chaining
        self.and_action_edges = [] # AND-Action
        self.trigger_and_edges = [] # Trigger-AND
        self.trigger_action_edges = [] # Trigger-Action

    def __str__(self):
        return 'Nodes: ' + str(list(self.G.nodes)) + ' - Edges: ' + str(list(self.G.edges)) + ' - Node labels: ' + str(self.node_labels) + ' - Edge labels: ' + str(self.edge_labels)

    def get_node_information(self, node_name):
        return self.G.nodes[node_name]

    def get_edge_information(self, first_node_name, second_node_name):
        return self.G.edges[first_node_name, second_node_name]

    def get_node_in_labeled_edges(self, node_name, relation_type):
        edges = list(self.G.in_edges(node_name))
        labeled_edges = []
        for edge in edges:
            if self.get_edge_information(edge[0], edge[1])['relation'] == relation_type:
                labeled_edges.append(edge)

        return labeled_edges

    def get_node_out_labeled_edges(self, node_name, relation_type):
        edges = list(self.G.out_edges(node_name))
        labeled_edges = []
        for edge in edges:
            if self.get_edge_information(edge[0], edge[1])['relation'] == relation_type:
                labeled_edges.append(edge)
        return labeled_edges

    def add_node(self, node_name, node_type, system_element):
        self.G.add_node(node_name, event=node_type, environment=system_element)
        self.node_labels.add(node_type)
        system_element_list = system_element.split(',')
        for element in system_element_list:
            self.node_labels.add(element)

    def has_edge(self, first_node_name, second_node_name):
        return self.G.has_edge(first_node_name, second_node_name)

    def draw_graph(self, node_size, font_size):
        color_map = {'trigger_action': 'black', 'triggerand': 'orange', 'andaction': 'orange',
                     'action_duplicate': 'blue', 'action_block': 'silver', 'action_conflict': 'green', 'rule_chaining': 'red',
                     'trigger_block': 'violet'}
        labels = nx.get_edge_attributes(self.G, 'relation')
        patches = [mpatches.Patch(color=color, label=label) for label, color in color_map.items()]
        nx.draw(self.G, with_labels=True, font_size = font_size, edge_color=[color_map[label] for label in labels.values()], node_color='lightblue', font_weight='bold', node_size=node_size)
        plt.legend(handles=patches)
        plt.show()

    def get_labeled_edges(self, relation_type):
        match relation_type:
            case 'action_duplicate':
                return self.action_duplicate_edges
            case 'action_conflict':
                return self.action_conflict_edges
            case 'action_block':
                return self.action_block_edges
            case 'trigger_block':
                return self.trigger_block_edges
            case 'rule_chaining':
                return self.cause_effect_edges
            case 'andaction':
                return self.and_action_edges
            case 'triggerand':
                return self.trigger_and_edges
            case 'trigger_action':
                return self.trigger_action_edges
            case _:
                raise ValueError('Unrecognized relation')

    def add_edge(self, first_node_name, second_node_name, relation_type):
        self.G.add_edge(first_node_name, second_node_name, relation=relation_type)
        self.edge_labels.add(relation_type)
        match relation_type:
            case 'trigger_action':
                self.trigger_action_edges.append(([first_node_name, second_node_name]))
            case 'triggerand':
                self.trigger_and_edges.append(([first_node_name, second_node_name]))
            case 'andaction':
                self.and_action_edges.append(([first_node_name, second_node_name]))
            case 'action_duplicate':
                self.action_duplicate_edges.append([first_node_name, second_node_name])
            case 'action_conflict':
                self.action_conflict_edges.append([first_node_name, second_node_name])
            case 'action_block':
                self.action_block_edges.append([first_node_name, second_node_name])
            case 'trigger_block':
                self.trigger_block_edges.append(([first_node_name, second_node_name]))
            case 'rule_chaining':
                self.rule_chaining_edges.append(([first_node_name, second_node_name]))
            case _:
                raise ValueError('Unrecognized relation')
