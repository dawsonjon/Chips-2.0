from graphviz import Digraph

class BlockDiagram():

    def __init__(self, chip):
        self.chip = chip

        g = Digraph(self.chip.name, graph_attr = {"rankdir":"LR"})

        sources = {}
        sinks = {}

        for instance in self.chip.instances:

            for port, wire in instance.inputs.iteritems():
                sinks[str(id(wire))] = str(id(instance)) + ":" + port

            for port, wire in instance.outputs.iteritems():
                sources[str(id(wire))] = str(id(instance)) + ":" + port

            inputs = "|".join(["<%s> %s"%(i, i) for i in instance.inputs.keys()])
            outputs = "|".join(["<%s> %s"%(i, i) for i in instance.outputs.keys()])
            label = "{{%s}|%s|{%s}}"%(
                inputs,
                instance.component_name,
                outputs
            )
            g.node(str(id(instance)), label=label, shape="record")

        for input_ in self.chip.inputs:
            sources[str(id(input_))] = str(id(input_))
            g.node(str(id(input_)), label=input_.name, shape="record")

        for output_ in self.chip.outputs:
            sinks[str(id(output_))] = str(id(output_))
            g.node(str(id(output_)), label=output_.name, shape="record")

        for wire, source in sources.iteritems():
            sink = sinks[wire]
            g.edge(source, sink)

        self.g = g

    def render(self, *args, **vargs):
        return self.g.render(*args, **vargs)

    def view(self, *args, **vargs):
        return self.g.view(*args, **vargs)


if __name__ == "__main__":
    from chips.api.api import *
    from chips.components.components import *
    c =  Chip("my_chip")
    a = Input(c, "a")
    b = Input(c, "b")
    d = Input(c, "d")
    e = Input(c, "e")
    x, y = tee(c, add(c, add(c, a, b), add(c, d, e)))
    discard(c, x)
    discard(c, y)
    b = BlockDiagram(c)
    b.view()

