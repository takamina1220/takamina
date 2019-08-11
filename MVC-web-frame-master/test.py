import os

from jinja2 import FileSystemLoader, Environment

parent = os.path.dirname(os.path.dirname(__file__))
path = os.path.join(parent, 'templates')
loader = FileSystemLoader(path)
e = Environment(loader=loader)


def render(filename, *args, **kwargs):
    template = e.get_template(filename)
    return template.render(*args, **kwargs)


def test():
    render("test.html")
