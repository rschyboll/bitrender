import os
import sys

import bpy
from bpy.types import (
    CompositorNodeMixRGB,
    CompositorNodeImage,
    Context,
    CompositorNodeOutputFile,
    NodeSocketFloat,
    NodeTree,
    NodeSocket,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from rendering_api.output import create_outputs
from rendering_api.utils import Args, setup_devices, MergeTask


def clear_tree(tree: NodeTree) -> None:
    nodes = tree.nodes
    for node in nodes:
        nodes.remove(node)


def create_output_node(tree: NodeTree, file_path: str) -> CompositorNodeOutputFile:
    nodes = tree.nodes
    node: CompositorNodeOutputFile = nodes.new("CompositorNodeOutputFile")
    node.file_slots.clear()
    node.format.file_format = "OPEN_EXR_MULTILAYER"
    node.base_path = file_path
    node.format.color_mode = "RGBA"
    return node


def join_files(context: Context, output_file: str, files: list[MergeTask]) -> None:
    context.scene.render.use_compositing = True
    context.scene.use_nodes = True
    tree = context.scene.node_tree
    print(tree)

    clear_tree(tree)
    nodes = []
    for file in files:
        print(file)
        node: CompositorNodeImage = tree.nodes.new(type="CompositorNodeImage")
        img = bpy.data.images.load(file["file"])
        node.image = bpy.data.images.load(file["file"])
        nodes.append((node, file["samples"]))
    node = nodes[0]
    output_node = create_output_node(tree, output_file)
    for socket_key in node[0].outputs.keys():
        join_sockets(tree, nodes, socket_key, output_node)


def join_sockets(
    tree: NodeTree,
    nodes: list[tuple[CompositorNodeImage, int]],
    socket: str,
    output_node: CompositorNodeOutputFile,
) -> None:
    nodes = nodes.copy()
    first_node = nodes.pop(0)
    second_node = nodes.pop(0)
    merge_node = merge(
        tree,
        first_node[0].outputs[socket],
        first_node[1],
        second_node[0].outputs[socket],
        second_node[1],
    )
    samples = first_node[1] + second_node[1]
    try:
        while True:
            node = nodes.pop(0)
            merge_node = merge(
                tree, node[0].outputs[socket], node[1], merge_node.outputs[0], samples
            )
            samples += node[1]
    except IndexError:
        pass
    output_socket = output_node.file_slots.new(name=socket)
    tree.links.new(merge_node.outputs[0], output_socket)


def merge(
    tree: NodeTree,
    socket_1: NodeSocket,
    samples_1: int,
    socket_2: NodeSocket,
    samples_2: int,
) -> CompositorNodeMixRGB:
    merge_node: CompositorNodeMixRGB = tree.nodes.new("CompositorNodeMixRGB")
    merge_node.blend_type = "MIX"
    inputs = get_mix_inputs(merge_node)
    tree.links.new(socket_1, inputs[0])
    tree.links.new(socket_2, inputs[1])
    socket: NodeSocketFloat = merge_node.inputs["Fac"]
    socket.default_value = samples_2 / (samples_1 + samples_2)
    return merge_node


def get_mix_inputs(node: CompositorNodeMixRGB) -> tuple[NodeSocket, NodeSocket]:
    inputs: list[NodeSocket] = []
    for input in node.inputs.items():
        if input[0] == "Image":
            inputs.append(input[1])
    return (inputs[0], inputs[1])


args = Args.from_sys_args()

if args.merge_files is None or len(args.merge_files) == 0:
    raise Exception()

context = bpy.context

files = []

for file in args.merge_files:
    files.append(
        {
            "samples": file["samples"],
            "file": os.path.join(args.files_dir, file["subtask_id"]),
        }
    )

join_files(context, args.output, files)

bpy.ops.render.render()
