import pydot
import json

def draw(parent_name, child_name, graph):
    edge = pydot.Edge(str(parent_name), str(child_name))
    graph.add_edge(edge)

def get_name(id, value):
    return "("+str(id)+") "+str(value)

def get_name_org(id, value, number_table):
    return "("+str(id)+") "+str(number_table[value] + ":"+str(value))

def get_leaf_name(id, value):
    return "("+str(id)+") "+str(value)

def visit_forest_org(h_tree, graph, number_table, parent = "*"):
    id = 0
    for key in h_tree:
        h_node = h_tree[key]
        name = get_name_org(id, key, number_table)
        draw("*", name, graph)
        id += 1
        id = visit_h_node_org(h_node, name, graph, id, number_table)

def visit_forest(h_tree, graph, parent = "*"):
    id = 0
    for key in h_tree:
        h_node = h_tree[key]
        name = get_name(id, key)
        draw("*", name, graph)
        id += 1
        id = visit_h_node(h_node, name, graph, id)

def visit_h_node_org(h_node, parent, graph, id, number_table):
    name = get_name(id, h_node["item"], number_table)
    id += 1
    
    draw(parent, name, graph)
    for child in h_node["children"]:
        id = visit_h_node_org(child, name, graph, id, number_table)
    
    if h_node["leaf"] != None:
        draw(name, get_leaf_name(id, json.dumps(h_node["leaf"], indent=2)), graph)
        id += 1
    return id

def visit_h_node(h_node, parent, graph, id):
    name = get_name(id, h_node["item"])
    id += 1
    
    draw(parent, name, graph)
    for child in h_node["children"]:
        id = visit_h_node(child, name, graph, id)
    
    if h_node["leaf"] != None:
        draw(name, get_leaf_name(id, json.dumps(h_node["leaf"], indent=2)), graph)
        id += 1
    return id


def generate_forest_image_org(h_tree, filename, number_table):
    graph = pydot.Dot(graph_type='graph')
    visit_forest_org(h_tree, graph, number_table)
    graph.write(path=filename, format="png")

def generate_forest_image(h_tree, filepath):
    graph = pydot.Dot(graph_type='graph')
    visit_forest(h_tree, graph)
    graph.write(path=filepath, format="png")