from typing import List

import bpy
from bpy.types import (
    CompositorNodeOutputFile,
    CompositorNodeRLayers,
    Context,
    NodeTree,
    bpy_prop_collection,
)

node_types = {
    "render_layers": "CompositorNodeRLayers",
    "output_file": "CompositorNodeOutputFile",
}


def get_layers(context: Context) -> List[str]:
    view_layers = context.scene.view_layers
    if isinstance(view_layers, bpy_prop_collection):
        layers: List[str] = []

        for view_layer in view_layers.values():
            layers.append(view_layer.name)

        return layers
    raise Exception()


def create_output_node(tree: NodeTree, file_path: str) -> CompositorNodeOutputFile:
    nodes = tree.nodes
    node: CompositorNodeOutputFile = nodes.new(node_types["output_file"])
    node.file_slots.clear()
    node.format.file_format = "OPEN_EXR_MULTILAYER"
    node.base_path = file_path
    node.format.color_mode = "RGBA"
    return node


def create_render_layers_node(tree: NodeTree, layer: str) -> CompositorNodeRLayers:
    nodes = tree.nodes
    node: CompositorNodeRLayers = nodes.new(node_types["render_layers"])
    node.layer = layer
    return node


def connect_input_output(
    tree: NodeTree,
    input_node: CompositorNodeRLayers,
    layer: str,
    output_node: CompositorNodeOutputFile,
) -> None:
    links = tree.links
    for output_socket in input_node.outputs:
        if output_socket.enabled:
            input_name = layer + "/" + output_socket.name
            output_node.file_slots.new(name=input_name)
            links.new(output_socket, output_node.inputs[-1])


def clear_tree(tree: NodeTree) -> None:
    nodes = tree.nodes
    for node in nodes:
        nodes.remove(node)


def create_outputs(context: Context, file_path: str) -> None:
    context.scene.render.use_compositing = True
    context.scene.use_nodes = True
    layers = get_layers(context)
    tree = context.scene.node_tree
    clear_tree(tree)
    output_node = create_output_node(tree, file_path)
    for layer in layers:
        input_node = create_render_layers_node(tree, layer)
        connect_input_output(tree, input_node, layer, output_node)
