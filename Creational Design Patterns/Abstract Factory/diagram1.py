import os
import tempfile


class DiagramFactory(object):
    pass


class SvgDiagramFactory(object):
    pass


def main():
    textFilename = os.path.join(tempfile.gettempdir(), 'diagram.txt')
    svgFilename = os.path.join(tempfile.gettempdir(), 'diagram.svg')

    txtDiagram = create_diagram(DiagramFactory())
    txtDiagram.save(textFilename)
    print('wrote', textFilename)

    svgDiagram = create_diagram(SvgDiagramFactory())
    svgDiagram.save(svgFilename)
    print('wrote', svgFilename)


def create_diagram(factory):
    diagram = factory.make_diagram(30, 7)
