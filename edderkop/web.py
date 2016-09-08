import os.path

from flask import Flask, Response, request

from edderkop.crawler import Crawler

app = Flask(__name__)


class WebStream(object):
    def __init__(self):
        self.seen_nodes = set()
        self.seen_links = set()

    def add_page(self, url):
        if url not in self.seen_nodes:
            self.seen_nodes.add(url)
            return ('<script>addPage("%s");</script>\n' % (url,))
        return ''

    def add_link(self, source, target, external):
        out = ''
        if target not in self.seen_nodes:
            self.seen_nodes.add(target)
            method = external and 'addExternalPage' or 'addPage'
            out += '<script>%s("%s");</script>\n' % (method, target,)

        if (source, target) not in self.seen_links:
            self.seen_links.add((source, target))
            out += '<script>addLink({"source": "%s", "target": "%s"});</script>\n' % (source, target)
        return out

    def add_image(self, source, img):
        out = ''
        if img not in self.seen_nodes:
            self.seen_nodes.add(img)
            out += '<script>addImage("%s");</script>\n' % (img,)

        if (source, img) not in self.seen_links:
            self.seen_links.add((source, img))
            out += '<script>addLink({"source": "%s", "target": "%s"});</script>\n' % (source, img)
        return out

    def add_script(self, source, script):
        out = ''
        if script not in self.seen_nodes:
            self.seen_nodes.add(script)
            out += '<script>addScript("%s");</script>\n' % (script,)

        if (source, script) not in self.seen_links:
            self.seen_links.add((source, script))
            out += '<script>addLink({"source": "%s", "target": "%s"});</script>\n' % (source, script)
        return out


@app.route('/', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        return '<form method="POST"><input type="text" name="url" placeholder="URL to crawl" /><input type="submit" value="Go!" /></form>'
    elif request.method == 'POST':
        url = request.form['url']

        def generate():
            with open(os.path.join(os.path.dirname(__file__), 'web_data', 'index.html'), 'r') as fp:
                yield fp.read()

            yield '<script>setSite("%s");</script>\n' % (url,)

            receiver = WebStream()
            crawler = Crawler(receiver)
            crawler.add_url(url)

            for x in crawler.run():
                yield x

        return Response(generate(), mimetype='text/html')
