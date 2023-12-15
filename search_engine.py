import random

class Detector(object):

    def __init__(self, G):
        self.G = G

    def getSubgraphs_action_conflict_block_duplicate(self, relation_type):
        if relation_type in ['action_conflict', 'action_block', 'action_duplicate']:
            subgraphs = []

            labeled_edges = self.G.get_labeled_edges(relation_type)

            for edge in labeled_edges:
                subgraph = []
                
                first_node_name = edge[0]
                
                second_node_name = edge[1]
                edge_tuple = (first_node_name, second_node_name)
                subgraph.append(edge_tuple)

                first_node_in_labeled_edges_trac = self.G.get_node_in_labeled_edges(first_node_name, 'trigger_action')

                second_node_in_labeled_edges_trac = self.G.get_node_in_labeled_edges(second_node_name, 'trigger_action')

                first_node_in_labeled_edges_trandac = self.G.get_node_in_labeled_edges(first_node_name, 'andaction')
                
                second_node_in_labeled_edges_trandac = self.G.get_node_in_labeled_edges(second_node_name, 'andaction')

                if first_node_in_labeled_edges_trac:
                    subgraph.extend(first_node_in_labeled_edges_trac)
                else:
                    subgraph.extend(first_node_in_labeled_edges_trandac)
                    for edge in first_node_in_labeled_edges_trandac:
                        triggerand_node = edge[0]
                        triggerand_node_in_labeled_edges = self.G.get_node_in_labeled_edges(triggerand_node, 'triggerand')
                        subgraph.extend(triggerand_node_in_labeled_edges)

                if second_node_in_labeled_edges_trac:
                    subgraph.extend(second_node_in_labeled_edges_trac)
                else:
                    subgraph.extend(second_node_in_labeled_edges_trandac)
                    for edge in second_node_in_labeled_edges_trandac:
                        triggerand_node = edge[0]
                        triggerand_node_in_labeled_edges = self.G.get_node_in_labeled_edges(triggerand_node, 'triggerand')
                        subgraph.extend(triggerand_node_in_labeled_edges)

                subgraphs.append(subgraph)

            return subgraphs
        else:
            raise ValueError('Unrecognized relation')

    def getSubgraphs_chain_loop(self):
        rule_chaining_edges = self.G.get_labeled_edges('rule_chaining')
        trigger_nodes_in_action = [edge[1] for edge in rule_chaining_edges]
        cycles = []
        while trigger_nodes_in_action:
            selected_trigger = random.choice(trigger_nodes_in_action)
            
            subset_cycles, visited_trigger = self.__tap_dfs_loop(selected_trigger)
            cycles.extend(subset_cycles)

            trigger_nodes_in_action = [trigger for trigger in trigger_nodes_in_action if trigger not in visited_trigger]

        lists = {}

        final_list = []

        for single_list in cycles:
            list_tuple = tuple(single_list)
            if list_tuple not in lists:
                lists[list_tuple] = True
                final_list.append(single_list)

        return final_list

    def __tap_dfs_loop(self, start_node):
        stack = [(start_node, [])]  
        trigger_node_visited = set()
        cycles = []

        while stack:
            node, path = stack.pop()  
            path.append(node)  
            if self.G.get_node_information(node)['event'] == 'action':  
                edges = self.G.get_node_out_labeled_edges(node, 'rule_chaining')
                for edge in edges:
                    neighbor = edge[1]
                    if neighbor in path:
                        cycle = path[path.index(neighbor):]  
                        cycles.append(cycle)
                    else:
                        stack.append((neighbor, path[:]))
            else:  
                trigger_node_visited.add(node)
                
                edges = self.G.get_node_out_labeled_edges(node, 'trigger_action')
                for edge in edges:
                    stack.append((edge[1], path[:]))

        return cycles, trigger_node_visited

    def getSubgraphs_action_revert(self):
        action_conflict_edges = self.G.get_labeled_edges('action_conflict')
        trigger_node_visited = set()
        action_revert_interferences = []
        for edge in action_conflict_edges:
            trigger_first_action = self.G.get_node_in_labeled_edges(edge[0], 'trigger_action')
            trigger_second_action = self.G.get_node_in_labeled_edges(edge[1], 'trigger_action')
            if trigger_first_action and trigger_second_action:
                if trigger_first_action[0][0] not in trigger_node_visited:
                    action_revert_interferences.append(self.__tap_dfs_revert(trigger_first_action[0][0]))
                    trigger_node_visited.add(trigger_first_action[0][0])
                if trigger_second_action[0][0] not in trigger_node_visited:
                    action_revert_interferences.append(self.__tap_dfs_revert(trigger_second_action[0][0]))
                    trigger_node_visited.add(trigger_second_action[0][0])
            elif trigger_first_action:
                if trigger_first_action[0][0] not in trigger_node_visited:
                    action_revert_interferences.append(self.__tap_dfs_revert(trigger_first_action[0][0]))
                    trigger_node_visited.add(trigger_first_action[0][0])
            else:
                if trigger_second_action[0][0] not in trigger_node_visited:
                    action_revert_interferences.append(self.__tap_dfs_revert(trigger_second_action[0][0]))
                    trigger_node_visited.add(trigger_second_action[0][0])

        return [x for x in action_revert_interferences if x != []]

    def __tap_dfs_revert(self, start_node):
        stack = [(start_node, [])]
        action_node_visited = set()
        trigger_node_visited = set()

        while stack:
            node, path = stack.pop()  
            path.append(node)  
            if self.G.get_node_information(node)['event'] == 'action':  
                action_node_visited.add(node)
                action_conflict_edges = self.G.get_node_out_labeled_edges(node, 'action_conflict')
                for edge_revert in action_conflict_edges:                    
                    if edge_revert[1] in path:
                        return path
                rule_chaining_edges = self.G.get_node_out_labeled_edges(node, 'rule_chaining')
                for edge in rule_chaining_edges:
                    neighbor = edge[1]
                    if neighbor not in trigger_node_visited:
                        stack.append((neighbor, path[:]))
            else:  
                trigger_node_visited.add(node)
                edges = self.G.get_node_out_labeled_edges(node, 'trigger_action')
                for edge in edges:
                    stack.append((edge[1], path[:]))

        return []

    def getSubgraphs_trigger_block_and_rule_chaining(self, relation_type):
        if relation_type in ['rule_chaining', 'trigger_block']:
            subgraphs = []
            labeled_edges = self.G.get_labeled_edges(relation_type)

            for edge in labeled_edges:
                subgraph = []
               
                first_node_name = edge[0]
                
                second_node_name = edge[1]
                edge_tuple = (first_node_name, second_node_name)
                subgraph.append(edge_tuple)

                first_node_in_labeled_edges_trac = self.G.get_node_in_labeled_edges(first_node_name, 'trigger_action') 

                second_node_out_labeled_edges_trac = self.G.get_node_out_labeled_edges(second_node_name, 'trigger_action') 
                first_node_in_labeled_edges_trandac = self.G.get_node_in_labeled_edges(first_node_name, 'andaction')
                
                second_node_out_labeled_edges_trandac = self.G.get_node_out_labeled_edges(second_node_name, 'triggerand')

                if first_node_in_labeled_edges_trac:
                    subgraph.extend(first_node_in_labeled_edges_trac)
                else:
                    subgraph.extend(first_node_in_labeled_edges_trandac)
                    for edge in first_node_in_labeled_edges_trandac:
                        triggerand_node = edge[0]

                        triggerand_node_in_labeled_edges = self.G.get_node_in_labeled_edges(triggerand_node, 'triggerand')
                        subgraph.extend(triggerand_node_in_labeled_edges)

                if second_node_out_labeled_edges_trac:
                    subgraph.extend(second_node_out_labeled_edges_trac)
                else:
                    for edge in second_node_out_labeled_edges_trandac:
                        triggerand_node = edge[1]

                        triggerand_node_in_labeled_edges = self.G.get_node_in_labeled_edges(triggerand_node, 'triggerand')
                        
                        triggerand_node_out_labeled_edges = self.G.get_node_out_labeled_edges(triggerand_node, 'andaction')
                        subgraph.extend(triggerand_node_in_labeled_edges)
                        subgraph.extend(triggerand_node_out_labeled_edges)

                subgraphs.append(subgraph)

            return subgraphs
        else:
            raise ValueError('Unrecognized relation')

    def getSubgraphs_multi_trigger_activation(self):
        subgraphs = []

        triggerand_action_edges = self.G.get_labeled_edges('andaction')
        for edge in triggerand_action_edges:
            subgraph = []

            triggerand_node = edge[0]
            flag = True

            triggerand_node_in_labeled_edges = self.G.get_node_in_labeled_edges(triggerand_node, 'triggerand')
            for triggerand_edge in triggerand_node_in_labeled_edges:
                
                triggerand_node_iteration = triggerand_edge[0]
               
                rule_chaining_edges = self.G.get_node_in_labeled_edges(triggerand_node_iteration, 'rule_chaining')

                if not rule_chaining_edges:
                    flag = False
                    break

                sub_edge_tuple = (triggerand_edge[0], triggerand_edge[1])
                subgraph.append(sub_edge_tuple)
                subgraph.extend(rule_chaining_edges)

                for rule_chaining in rule_chaining_edges:
                    action_node = rule_chaining[0]
                    action_node_in_labeled_edges_trac = self.G.get_node_in_labeled_edges(action_node, 'trigger_action')
                    if action_node_in_labeled_edges_trac:
                        subgraph.extend(action_node_in_labeled_edges_trac)
                    else:
                        action_node_in_labeled_edges_trandac = self.G.get_node_in_labeled_edges(action_node, 'andaction')
                        subgraph.extend(action_node_in_labeled_edges_trandac)
                        for edge_and in action_node_in_labeled_edges_trandac:
                            triggerand_node = edge_and[0]
                            triggerand_node_in_labeled_edges = self.G.get_node_in_labeled_edges(triggerand_node, 'triggerand')
                            subgraph.extend(triggerand_node_in_labeled_edges)
           
            if flag:
                main_edge_tuple = (edge[0], edge[1])
                subgraph.append(main_edge_tuple)
                subgraphs.append(subgraph)

        return subgraphs
