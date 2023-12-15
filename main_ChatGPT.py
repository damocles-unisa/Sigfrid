from scene_interaction_graph import SceneInteractionGraph
from search_engine import Detector
from utils_ChatGPT import *
import pandas as pd

if __name__ == '__main__':

    qa_engine = QuestionAnswerChatGPT('api_key')

    df = pd.read_csv('path')

    # Author-Based Strategy
    creator_rules = df.loc[df['creatorName'] == 'xxx']

    rule_triggers = []
    rule_actions = []
    rule_trigger_services = []
    rule_action_services = []

    rule_graph = SceneInteractionGraph()

    total_trigger_system_elements = []
    total_action_system_elements = []


    for i in range(len(creator_rules)):
        
        trigger = creator_rules.iloc[i]['triggerDesc']
        
        trigger_system_elements = qa_engine.get_answer_system_elements(trigger, 'trigger')
        total_trigger_system_elements.append(trigger_system_elements)

        
        action = creator_rules.iloc[i]['actionDesc']
        
        action_system_elements = qa_engine.get_answer_system_elements(action, 'action')
        total_action_system_elements.append(action_system_elements)

        
        rule_graph.add_node(f"TR{i+1}", 'trigger', ','.join(trigger_system_elements))
        
        rule_graph.add_node(f"AR{i+1}", 'action', ','.join(action_system_elements))
       
        rule_graph.add_edge(f"TR{i+1}", f"AR{i+1}", 'trigger_action')

        
        rule_triggers.append(trigger)
        
        rule_actions.append(action)
        
        rule_trigger_services.append(creator_rules.iloc[i]['triggerService'])
        
        rule_action_services.append(creator_rules.iloc[i]['actionService'])

  
    for i in range(len(rule_triggers)):
        
        trigger_id = f"TR{i+1}"
        
        trigger_desc = rule_triggers[i]
        
        trigger_system_elements = total_trigger_system_elements[i]
        
        for j in range(len(rule_actions)):
            if i != j:
                
                action_id = f"AR{j+1}"
                
                action_desc = rule_actions[j]
                action_system_elements = total_action_system_elements[j]
                
                if rule_trigger_services[i].lower() == rule_action_services[j].lower():
                   
                    if qa_engine.get_answer_relation(action_desc, trigger_desc, 'RULE_CHAINING') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'rule_chaining')

                    elif qa_engine.get_answer_relation(action_desc, trigger_desc, 'TRIGGER_BLOCK') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'trigger_block')

                elif any(elem in trigger_system_elements for elem in action_system_elements):

                    if qa_engine.get_answer_relation(action_desc, trigger_desc, 'RULE_CHAINING') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'rule_chaining')
                    elif qa_engine.get_answer_relation(action_desc, trigger_desc, 'TRIGGER_BLOCK') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'trigger_block')

              
                elif 'temperature' in action_system_elements and 'humidity' in trigger_system_elements:
                    if qa_engine.get_answer_relation(action_desc, trigger_desc, 'RULE_CHAINING') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'rule_chaining')
                    elif qa_engine.get_answer_relation(action_desc, trigger_desc, 'TRIGGER_BLOCK') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'trigger_block')
                elif 'illumination' in action_system_elements and ('motion' in trigger_system_elements or 'temperature' in trigger_system_elements):
                    if qa_engine.get_answer_relation(action_desc, trigger_desc, 'RULE_CHAINING') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'rule_chaining')
                    elif qa_engine.get_answer_relation(action_desc, trigger_desc, 'TRIGGER_BLOCK') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'trigger_block')
                elif 'security' in action_system_elements and ('sound' in trigger_system_elements or 'motion' in trigger_system_elements):
                    if qa_engine.get_answer_relation(action_desc, trigger_desc, 'RULE_CHAINING') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'rule_chaining')
                    elif qa_engine.get_answer_relation(action_desc, trigger_desc, 'TRIGGER_BLOCK') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'trigger_block')
                elif 'water' in action_system_elements and ('humidity' in trigger_system_elements or 'temperature' in trigger_system_elements):
                    if qa_engine.get_answer_relation(action_desc, trigger_desc, 'RULE_CHAINING') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'rule_chaining')
                    elif qa_engine.get_answer_relation(action_desc, trigger_desc, 'TRIGGER_BLOCK') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'trigger_block')
                elif 'ventilation' in action_system_elements and ('temperature' in trigger_system_elements or 'humidity' in trigger_system_elements):
                    if qa_engine.get_answer_relation(action_desc, trigger_desc, 'RULE_CHAINING') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'rule_chaining')
                    elif qa_engine.get_answer_relation(action_desc, trigger_desc, 'TRIGGER_BLOCK') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'trigger_block')
                elif 'sound' in action_system_elements and 'motion' in trigger_system_elements:
                    if qa_engine.get_answer_relation(action_desc, trigger_desc, 'RULE_CHAINING') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'rule_chaining')
                    elif qa_engine.get_answer_relation(action_desc, trigger_desc, 'TRIGGER_BLOCK') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'trigger_block')
                elif 'gas' in action_system_elements and 'humidity' in trigger_system_elements:
                    if qa_engine.get_answer_relation(action_desc, trigger_desc, 'RULE_CHAINING') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'rule_chaining')
                    elif qa_engine.get_answer_relation(action_desc, trigger_desc, 'TRIGGER_BLOCK') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'trigger_block')
                elif 'network' in action_system_elements and ('security' in trigger_system_elements or 'motion' in trigger_system_elements):
                    if qa_engine.get_answer_relation(action_desc, trigger_desc, 'RULE_CHAINING') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'rule_chaining')
                    elif qa_engine.get_answer_relation(action_desc, trigger_desc, 'TRIGGER_BLOCK') == 'Yes':
                        rule_graph.add_edge(action_id, trigger_id, 'trigger_block')

        
        action_id = f"AR{i + 1}"
        
        action_desc = rule_actions[i]
        action_system_elements = total_action_system_elements[i]

        
        for x in range(len(rule_actions)):
            if i != x:
                
                action_id_2 = f"AR{x + 1}"
                
                if not rule_graph.has_edge(action_id, action_id_2) and not rule_graph.has_edge(action_id_2, action_id):
                    
                    action_desc_2 = rule_actions[x]
                    action_system_elements_2 = total_action_system_elements[x]

                    if rule_action_channels[i].lower() == rule_action_channels[x].lower():

                        answer_1 = qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_BLOCK')
                        answer_2 = qa_engine.get_answer_relation(action_desc_2, action_desc, 'ACTION_BLOCK')

                        if qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_DUPLICATE') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_duplicate')
                            rule_graph.add_edge(action_id_2, action_id, 'action_duplicate')
                        elif qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_CONFLICT') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_conflict')
                            rule_graph.add_edge(action_id_2, action_id, 'action_conflict')
                        elif answer_1 == 'Yes' and answer_2 == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_block')
                            rule_graph.add_edge(action_id_2, action_id, 'action_block')
                        elif answer_1 == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_block')
                        elif answer_2 == 'Yes':
                            rule_graph.add_edge(action_id_2, action_id, 'action_block')

                    elif any(elem in action_system_elements for elem in action_system_elements_2):

                        answer_1 = qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_BLOCK')
                        answer_2 = qa_engine.get_answer_relation(action_desc_2, action_desc, 'ACTION_BLOCK')

                        if qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_CONFLICT') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_conflict')
                            rule_graph.add_edge(action_id_2, action_id, 'action_conflict')
                        elif answer_1 == 'Yes' and answer_2 == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_block')
                            rule_graph.add_edge(action_id_2, action_id, 'action_block')
                        elif answer_1 == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_block')
                        elif answer_2 == 'Yes':
                            rule_graph.add_edge(action_id_2, action_id, 'action_block')

                    elif 'temperature' in action_system_elements and 'humidity' in action_system_elements_2:
                        if qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_CONFLICT') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_conflict')
                        elif qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_BLOCK') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_block')
                    elif 'illumination' in action_system_elements and (
                            'motion' in action_system_elements_2 or 'temperature' in action_system_elements_2):
                        if qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_CONFLICT') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_conflict')
                        elif qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_BLOCK') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_block')
                    elif 'security' in action_system_elements and ('sound' in action_system_elements_2 or 'motion' in action_system_elements_2):
                        if qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_CONFLICT') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_conflict')
                        elif qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_BLOCK') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_block')
                    elif 'water' in action_system_elements and (
                            'humidity' in action_system_elements_2 or 'temperature' in action_system_elements_2):
                        if qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_CONFLICT') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_conflict')
                        elif qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_BLOCK') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_block')
                    elif 'ventilation' in action_system_elements and (
                            'temperature' in action_system_elements_2 or 'humidity' in action_system_elements_2):
                        if qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_CONFLICT') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_conflict')
                        elif qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_BLOCK') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_block')
                    elif 'sound' in action_system_elements and 'motion' in action_system_elements_2:
                        if qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_CONFLICT') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_conflict')
                        elif qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_BLOCK') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_block')
                    elif 'gas' in action_system_elements and 'humidity' in action_system_elements_2:
                        if qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_CONFLICT') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_conflict')
                        elif qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_BLOCK') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_block')
                    elif 'network' in action_system_elements and ('security' in action_system_elements_2 or 'motion' in action_system_elements_2):
                        if qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_CONFLICT') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_conflict')
                        elif qa_engine.get_answer_relation(action_desc, action_desc_2, 'ACTION_BLOCK') == 'Yes':
                            rule_graph.add_edge(action_id, action_id_2, 'action_block')

    pattern_engine = Detector(rule_graph)

    action_block_interferences = pattern_engine.getSubgraphs_action_conflict_block_duplicate('action_block')
    action_conflict_interferences = pattern_engine.getSubgraphs_action_conflict_block_duplicate('action_conflict')
    action_duplicate_interferences = pattern_engine.getSubgraphs_action_conflict_block_duplicate('action_duplicate')
    chain_loop_interferences = pattern_engine.getSubgraphs_chain_loop()
    action_revert_interferences = pattern_engine.getSubgraphs_action_revert()
    rule_chaining_interferences = pattern_engine.getSubgraphs_trigger_block_and_rule_chaining('rule_chaining')
    trigger_block_interferences = pattern_engine.getSubgraphs_trigger_block_and_rule_chaining('trigger_block')
    multi_trigger_activation_interferences = pattern_engine.getSubgraphs_multi_trigger_activation()

    print('Action Block Interferences:', action_block_interferences, ', Count:', len(action_block_interferences))
    print('Action Conflict Interferences:', action_conflict_interferences, ', Count:',
          len(action_conflict_interferences))
    print('Action Duplicate Interferences:', action_duplicate_interferences, ', Count:',
          len(action_duplicate_interferences))
    print('Chain Loop Interferences:', chain_loop_interferences, ', Count:', len(chain_loop_interferences))
    print('Action Revert Interferences:', action_revert_interferences, ', Count:', len(action_revert_interferences))
    print('Rule Chaining Interferences:', rule_chaining_interferences, ', Count:', len(rule_chaining_interferences))
    print('Trigger Block Interferences:', trigger_block_interferences, ', Count:', len(trigger_block_interferences))
    print('Multi Trigger Activation Interferences:', multi_trigger_activation_interferences, ', Count:',
          len(multi_trigger_activation_interferences))

    rule_graph.draw_graph(700, 5.6)
