from anytree import PostOrderIter, PreOrderIter
from colorama import Fore

import nndt
from nndt.space2 import AbstractBBoxNode
from nndt.space2.abstracts import node_method, AbstractTreeElement, DICT_NODETYPE_PRIORITY, NODE_METHOD_DICT, \
    IterAccessMixin


def _get_class_hierarchy(obj):
    class_hierarchy = [obj.__class__]
    while len(class_hierarchy[-1].__bases__) > 0:
        class_hierarchy = class_hierarchy + [class_hierarchy[-1].__bases__[0]]
    return class_hierarchy


def _add_explicit_methods_to_node(node: AbstractTreeElement):
    class_hierarchy = _get_class_hierarchy(node)
    class_hierarchy = list([str(class_.__name__) for class_ in class_hierarchy])
    from nndt.space2 import MethodNode
    for class_name in class_hierarchy:
        if class_name in NODE_METHOD_DICT:
            for fn_name, fn_docs in NODE_METHOD_DICT[class_name].items():
                if hasattr(node, fn_name) and (fn_name not in [x.name for x in node.children]):
                    MethodNode(fn_name, fn_docs, parent=node)


def _add_method_sets_to_node(node: AbstractTreeElement):
    from nndt.space2 import MethodSetNode
    from nndt.space2 import AbstractTransformation
    from nndt.space2 import MethodNode
    from nndt.space2 import ImpRepr
    elements = [child for child in node.children
                if isinstance(child, (AbstractTransformation, MethodSetNode, ImpRepr))]
    for elem in elements:
        for fn_name, fn_docs in NODE_METHOD_DICT[str(elem.__class__.__name__)].items():
            if not hasattr(node, fn_name) and (fn_name not in [x.name for x in node.children]):
                fun = getattr(elem, fn_name)
                setattr(node, fn_name, fun)
                MethodNode(fn_name, fn_docs, parent=node)


class Space(AbstractBBoxNode, IterAccessMixin):
    def __init__(self, name,
                 bbox=((0., 0., 0.), (0., 0., 0.)),
                 parent=None):
        super(Space, self).__init__(name, parent=parent, bbox=bbox, _print_color=Fore.RED, _nodetype='S')
        self.version = nndt.__version__

        self._is_init = False
        self._is_preload = False

    def __repr__(self):
        return self._print_color + f'{self._nodetype}:{self.name}' + Fore.WHITE + f' {self.version}' + Fore.RESET

    @node_method("save_space_to_file(filepath)")
    def save_space_to_file(self, filepath: str):
        """Writes Space in file

        Args:
            filepath (str): file name
        """
        from nndt.space2 import save_space_to_file
        return save_space_to_file(self, filepath)

    @node_method("to_json()")
    def to_json(self):
        """Converts Space to json format

        Returns:
            json: space in json format
        """
        from nndt.space2 import to_json
        return to_json(self)

    @node_method("init()")
    def init(self):
        """Makes initialization for Space
        """
        for node in PostOrderIter(self):
            if isinstance(node, AbstractTreeElement):
                _add_explicit_methods_to_node(node)

        for node in PostOrderIter(self):
            if isinstance(node, AbstractTreeElement):
                _add_method_sets_to_node(node)

        for node in PreOrderIter(self):
            node._NodeMixin__children_or_empty.sort(key=lambda d: (100 - DICT_NODETYPE_PRIORITY[d._nodetype], d.name),
                                                    reverse=False)

    @node_method("preload(identity|shift_and_scale|to_cube, scale, keep_in_memory=True)")
    def preload(self, mode="identity", scale=50, keep_in_memory=True):
        """Makes preload for Space if it was not done. Otherwise does nothing

        Args:
            mode (str, optional): Mode. Defaults to "identity".
            scale (int, optional): Scale. Defaults to 50.
            keep_in_memory (bool, optional): Keep in memory. Defaults to True.
        """
        if not self._is_preload:
            from nndt.space2.space_preloader import DefaultPreloader
            self.preloader = DefaultPreloader(mode=mode, scale=scale, keep_in_memory=keep_in_memory)
            self.preloader.preload(self)
