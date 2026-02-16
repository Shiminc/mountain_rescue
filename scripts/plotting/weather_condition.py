from scripts.utils.utils import set_up_altair, convert_to_numeric, handling_problematic_data, read_json_to_df, format_time_columns,calculating_other_agencies, determine_next_day
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from d3blocks import D3Blocks    

PATH = "../../data/all_incidents.json"

def create_weather_pair(weather_series):
    all_node_tuple_list = []

    for incident_weather_list in weather_series:
        if isinstance(incident_weather_list, list):
            for i,item in enumerate(incident_weather_list):
                if i+1 < len(incident_weather_list):
                    node_set = tuple(sorted([item,incident_weather_list[i+1]])) 
                    all_node_tuple_list.append(node_set)
    
    return all_node_tuple_list

def calculate_node_count(weather_series):
    node_count_dict= {}
    for incident_weather_list in weather_series:
        if isinstance(incident_weather_list, list):
            for weather in incident_weather_list:
                if weather not in node_count_dict:
                    node_count_dict.update({weather:1})
                else: 
                    node_count_dict[weather] = node_count_dict[weather] +1

    for weather in node_count_dict:
        size = node_count_dict[weather]*10
        node_count_dict[weather] = {'size': size}


    return node_count_dict


def count_weather_pair(all_node_tuple_list):
    weather_dictionary = {}
    for node_tuple in all_node_tuple_list:
        if node_tuple not in weather_dictionary:
            weather_dictionary.update({node_tuple:1})
        else:
            weather_dictionary[node_tuple] = weather_dictionary[node_tuple] + 1
    
    return weather_dictionary

def create_network_graph_without_weight(list_of_nodes):
    graph = nx.Graph()
    graph.add_edges_from(list_of_nodes)
    pos = nx.circular_layout(graph)
    nx.draw_networkx(graph, pos)
    return graph


def adjust_weight_for_edge(edge_list, multiplier = 0.2):
    modified_edge_list = []
    for edge in edge_list:
        temp_list = list(edge)
        temp_list[2] = temp_list[2]*multiplier 
        modified_edge_list.append(tuple(temp_list))
    return modified_edge_list

def create_network_graph_with_weight(edge_list, node_list):

    graph = nx.Graph()
    graph.add_weighted_edges_from(edge_list)

    # pos = nx.spring_layout(graph, seed = 7) 
    pos = nx.circular_layout(graph)
    # pos = nx.bfs_layout(graph,start = 'Cold')
    pos = nx.kamada_kawai_layout(graph)
    pos = nx.shell_layout(graph)
    pos = nx.arf_layout(graph)
    nx.set_node_attributes(graph,node_list)
    node_size = nx.get_node_attributes(graph,'size')
    edge_weight = nx.get_edge_attributes(graph,'weight')
    nx.draw_networkx_nodes(graph, pos, node_size=list(node_size.values()))  
    nx.draw_networkx(graph, pos, width = list(edge_weight.values()),  
                     alpha = 0.6)
    return graph

def create_edge_tuple(weather_dictionary):
    edge_list = []
    for edge in weather_dictionary:
        temp_list = list(edge)
        temp_list.append(weather_dictionary[edge])
        edge_list.append((tuple(temp_list)))
        
    return edge_list
def create_chord_chart(df):
    d3 = D3Blocks(frame=False)
    d3.chord(df, color='source', opacity='source', cmap='Set2') 
    d3.show()
    return d3
def main():
    data = read_json_to_df(PATH)
    data = format_time_columns(data)
    data = convert_to_numeric(data)
    data = handling_problematic_data(data)
    data = calculating_other_agencies(data)
    data = determine_next_day(data)

    pair_list = create_weather_pair(data['Weather'])
    pair_count = count_weather_pair(pair_list)
    edge_list = create_edge_tuple(pair_count)


    node_count = calculate_node_count(data['Weather'])
    # pair_count_df = pd.DataFrame.from_dict(pair_count, orient='index').reset_index()
    # pair_count_df.columns = ['pair','weight']
    # create_network_graph_without_weight(pair_list)
    chord_df = pd.DataFrame(edge_list)
    chord_df.columns = ['source','target','weight']
    create_chord_chart(chord_df)

    modified_edge_list = adjust_weight_for_edge(edge_list)
    create_network_graph_with_weight(modified_edge_list, node_count)
    plt.show()
    print('finish')
main()