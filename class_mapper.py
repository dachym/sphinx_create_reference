from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx import addnodes
from sphinx.util.docutils import SphinxDirective
from sphinx.transforms.post_transforms import SphinxPostTransform


class ClassListPending(nodes.General, nodes.Element):
    pass


def class_name_to_target(class_name: str) -> str:
    """Needs to be globally unique, so prefix"""
    return f"class-mapper-target--{class_name.lower()}"


class ClassListDirective(Directive):
    @staticmethod
    def run():
        return [ClassListPending("")]


class ClassDirective(SphinxDirective):
    # this enables content in the directive
    has_content = True

    def run(self):
        class_name = "".join(self.content).strip()
        self.env.class_names_list.append(class_name)  # NoQA

        # Create a new target node
        target = nodes.target(
            '', '',
            ids=[class_name_to_target(class_name)],
            names=[class_name_to_target(class_name)]
        )

        # Update the document with the new target (imperative note)
        self.state.document.note_explicit_target(target)

        # Add the target to the top of the document tree
        self.state.document.insert(0, target)
        return []

class ClassDirectiveDoc(SphinxDirective):
    # this enables content in the directive
    has_content = True

    def run(self):
        class_name = "".join(self.content).strip()
        self.env.class_doc_names_list.append((class_name, self.state.document))  # NoQA

        # Create a new target node
        target = nodes.target(
            '', '',
            ids=[class_name_to_target(class_name)],
            names=[class_name_to_target(class_name)]
        )

        # Update the document with the new target (imperative note)
        self.state.document.note_explicit_target(target)

        # Add the target to the top of the document tree
        self.state.document.insert(0, target)
        
        self.state.document.insert(0, nodes.warning(
                "",
                nodes.Text("Warning node !"),
            ))

        return []


def initialise_class_all_classes(app):
    app.env.class_names_list = []
    app.env.class_doc_names_list = []


class ClassListTransform(SphinxPostTransform):
    default_priority = 5

    def run(self, **kwargs) -> None:
        for node in self.document.findall(ClassListPending):
            ref_nodes = []
            for class_name, class_doc_name in zip(self.app.builder.env.class_names_list, self.app.builder.env.class_doc_names_list):
                class_doc_name[1].insert(0, nodes.warning(
                                "",
                                nodes.Text(
                                    "Warning node !"
                                ),
                            ))
                ref_to = f"{class_name}-documentation"
                ref_node = addnodes.pending_xref(
                    ':ref:`%s`' % ref_to,
                    nodes.inline(
                        ':ref:`%s`' % ref_to,
                        f"Documentation for {class_name}",
                        classes=["xref", "std", "std-ref"],  # copied from ``:ref:``
                    ),
                    refdoc=self.env.docname,
                    refdomain="std",
                    refexplicit=False,
                    reftype='ref',
                    reftarget=class_name_to_target(class_doc_name[0]),
                    refwarn=True,
                )
                ref_nodes.append(ref_node)
            node.replace_self(nodes.paragraph("", "", *ref_nodes))





def setup(app):
    def noop(self, node):  # NoQA
        """A do-nothing function."""

    # The ``ClassListPending`` node does nothing and serves as a marker for later
    # use.
    app.add_node(
        ClassListPending,
        html=(noop, noop),
        latex=(noop, noop),
        text=(noop, noop),
    )

    app.add_directive("class_directive_doc", ClassDirectiveDoc)

    # The ``class_directive`` directive is used within the docstrings of classes
    # that we want to centrally list. It must be used with the class name as the
    # only directive content.
    app.add_directive('class_directive', ClassDirective)

    # The ``class_list_doc`` directive produces a list of references to the
    # classes in a two stage process. This first stage inserts a
    # ``ClassListPending`` node into the document as a placeholder.
    app.add_directive('class_list_doc', ClassListDirective)

    # We create the ``class_names_list`` attribute on the BuildEnvironment class
    # in this function
    app.connect('builder-inited', initialise_class_all_classes)

    # The ClassListTransform is the second and final stage of producing the list
    # of references. It finds all ``ClassListPending`` nodes and replaces them
    # with a list of references to classes generated from the names stored in
    # ``app.env.class_names_list``.
    app.add_post_transform(ClassListTransform)

    return {'parallel_read_safe': True, 'parallel_write_safe': True}