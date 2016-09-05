from edderkop.formatters import Formatter


class GraphvizFormatter(Formatter):
    def header(self):
        return 'digraph G {\n'

    def format_page(self, page):
        return '"%s";\n' % (page,)

    def format_link(self, page, link):
        return '"%s" -> "%s";\n' % (page, link)

    def format_image(self, page, image):
        return '"%s" -> "%s";\n' % (page, image)

    def format_script(self, page, script):
        return '"%s" -> "%s";\n' % (page, script)

    def footer(self):
        return '}\n'

formatter_class = GraphvizFormatter
