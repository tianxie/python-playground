import os
import tempfile


def main():
    textFilename = os.path.join(tempfile.gettempdir(), 'diagram.txt')
    svgFilename = os.path.join(tempfile.gettempdir(), 'diagram.svg')

    txtDiagram = create_diagram(DiagramFactory())
    txtDiagram.save(textFilename)
    print('wrote', textFilename)

    # svgDiagram = create_diagram(SvgDiagramFactory())
    # svgDiagram.save(svgFilename)
    # print('wrote', svgFilename)


def create_diagram(factory):
    diagram = factory.make_diagram(30, 7)
    # rectangle = factory.make_rectangle(4, 1, 22, 5, "yellow")
    # text = factory.make_text(7, 3, "Abstract Factory")
    # diagram.add(rectangle)
    # diagram.add(text)
    return diagram


class DiagramFactory(object):
    def make_diagram(self, width, height):
        return Diagram(width, height)

    # def make_rectangle(self, x, y, width, height, fill="white", stroke="black"):
    #     return Rectangle(x, y, width, height, fill, stroke)
    #
    # def make_text(self, x, y, text, fontsize=12):
    #     return Text(x, y, text, fontsize)


# class SvgDiagramFactory(DiagramFactory):
#     def make_diagram(self, width, height):
#         return SvgDiagram(width, height)
#
#     def make_rectangle(self, x, y, width, height, fill="white", stroke="black"):
#         return SvgRectangle(x, y, width, height, fill, stroke)
#
#     def make_text(self, x, y, text, fontsize=12):
#         return SvgText(x, y, text, fontsize)


BLANK = " "
CORNER = "+"
HORIZONTAL = "-"
VERTICAL = "|"


class Diagram(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.diagram = _create_rectangle(self.width, self.height, BLANK)

    def add(self, component):
        for y, row in enumerate(component.rows):
            for x, char in enumerate(row):
                self.diagram[y + component.y][x + component.x] = char

    def save(self, filenameOrFile):
        file = None if isinstance(filenameOrFile, str) else filenameOrFile
        try:
            if file is None:
                file = open(filenameOrFile, "w")
            for row in self.diagram:
                print("".join(row), file)
        finally:
            if isinstance(filenameOrFile, str) and file is not None:
                file.close()


def _create_rectangle(width, height, fill):
    rows = [[fill for _ in range(width)] for _ in range(height)]
    for x in range(1, width - 1):
        rows[0][x] = HORIZONTAL
        rows[height - 1][x] = HORIZONTAL
    for y in range(1, height - 1):
        rows[y][0] = VERTICAL
        rows[y][width - 1] = VERTICAL
    for y, x in ((0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)):
        rows[y][x] = CORNER
    return rows

if __name__ == "__main__":
    main()