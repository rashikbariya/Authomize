from graph import Graph, Node
import json


def load_gcp_resources(json_file_path: str) -> list:
    with open(json_file_path, 'r') as gcp_permissions_json_file:
        return json.load(gcp_permissions_json_file)


def add_parent_relationship(graph: Graph, resource: dict) -> None:
    ancestors = resource.get('ancestors', [])
    if len(ancestors) > 1:
        child_id = resource.get('name', '').split('.googleapis.com/')[-1]
        parent_id = ancestors[1]
        child_node = graph.get_or_insert_node(
            Node(id=child_id, type='resource', resource_type=resource.get('asset_type', '').split('/')[-1]))
        parent_node = graph.get_or_insert_node(
            Node(id=parent_id, type='resource'))
        graph.insert_edge(parent_node, child_node, 'is_parent_resource_of')


def add_permission_relationships(graph: Graph, resource: dict) -> None:
    resource_id = resource.get('name', '').split('.googleapis.com/')[-1]
    resource_type = resource.get('asset_type', '').split('/')[-1]
    resource_node = graph.get_or_insert_node(
        Node(id=resource_id, type='resource', resource_type=resource_type))
    bindings = resource.get('iam_policy', {}).get('bindings', [])
    for binding in bindings:
        role = binding.get('role', '')
        for identity in binding.get('members', []):
            identity_type = identity.split(':')[0]
            identity_node = graph.get_or_insert_node(
                Node(id=identity, type='identity', identity_type=identity_type))
            graph.insert_edge(identity_node, resource_node, f'is_{role}_of')


def build_gcp_permission_graph(json_file_path: str) -> Graph:
    graph = Graph()
    resources = load_gcp_resources(json_file_path)

    for resource in resources:
        add_parent_relationship(graph, resource)
        add_permission_relationships(graph, resource)
    return graph
