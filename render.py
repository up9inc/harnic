from jinja2 import Environment, FileSystemLoader, select_autoescape

from har import HAR


env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)


def render_diff(hars, records):
    template = env.get_template("index.html")
    context = {
        'hars': hars,
        'records': records,
    }
    template.stream(**context).dump('index.html')


if __name__ == '__main__':
    h1 = HAR('hars/e-maxx.ru/1.har')
    h2 = HAR('hars/e-maxx.ru/2.har')
    diff = h1.compare(h2)

    render_diff((h1, h2), diff.records)
