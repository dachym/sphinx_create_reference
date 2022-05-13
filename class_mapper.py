from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.util.docutils import SphinxDirective


class class_directive(nodes.Admonition, nodes.Element):
    pass


class class_list_doc(nodes.General, nodes.Element):
    pass


def visit_class_node(self, node):
    self.visit_admonition(node)


def depart_class_node(self, node):
    self.depart_admonition(node)


class ClassListDirective(Directive):

    def run(self):
        return [class_list_doc('')]


class ClassDirective(SphinxDirective):

    # this enables content in the directive
    has_content = True

    def run(self):
        class_node = class_directive('\n'.join(self.content))
        self.state.nested_parse(self.content, self.content_offset, class_node)

        if not hasattr(self.env, 'class_all_classes'):
            self.env.class_all_classes = []

        self.env.class_all_classes.append({
            'docname': self.env.docname,
            'lineno': self.lineno,
            'class_directive': class_node.deepcopy(),
        })

        return [class_node]


def purge_classes(app, env, docname):
    if not hasattr(env, 'class_all_classes'):
        return

    env.class_all_classes = [c for c in env.class_all_classes
                             if c['docname'] != docname]


def merge_classes(app, env, docnames, other):
    if not hasattr(env, 'class_all_classes'):
        env.class_all_classes = []
    if hasattr(other, 'class_all_classes'):
        env.class_all_classes.extend(other.class_all_classes)


def process_class_nodes(app, doctree, fromdocname):
    if not app.config.class_include_classes:
        for node in doctree.traverse(class_directive):
            node.parent.remove(node)

    env = app.builder.env

    if not hasattr(env, 'class_all_classes'):
        env.class_all_classes = []

    for node in doctree.traverse(class_list_doc):
        if not app.config.class_include_classes:
            node.replace_self([])
            continue

        for class_info in env.class_all_classes:

            class_name = class_info["class_directive"].children[0].astext()
            para = nodes.paragraph()
            para += nodes.reference(internal=False, refid=f"{class_name}_documentation",
                                    text=f"{class_name} documentation")
            node.replace_self(para)
            

def setup(app):
    app.add_config_value('class_include_classes', True, 'html')

    app.add_node(class_list_doc)
    app.add_node(class_directive,
                 html=(visit_class_node, depart_class_node),
                 latex=(visit_class_node, depart_class_node),
                 text=(visit_class_node, depart_class_node))

    app.add_directive('class_directive', ClassDirective)
    app.add_directive('class_list_doc', ClassListDirective)
    app.connect('doctree-resolved', process_class_nodes)
    app.connect('env-purge-doc', purge_classes)
    app.connect('env-merge-info', merge_classes)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }