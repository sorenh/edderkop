import os.path

from six.moves.urllib.parse import urlparse


def target_url(base_url, href):
    parsed_base_url = urlparse(base_url)

    href = href.split('#', 1)[0]

    if not href:
        return base_url

    if '://' in href:
        return href
    elif href.startswith('/'):
        return '%s://%s%s' % (parsed_base_url.scheme, parsed_base_url.netloc, href)
    else:
        path = parsed_base_url.path or '/'

        if not path.endswith('/'):
            path = '/'.join(path.split('/')[:-1]) + '/'

        return '%s://%s%s' % (parsed_base_url.scheme, parsed_base_url.netloc, os.path.normpath(os.path.join(path, href)))


def href_usable(href):
    if not href:
        return False

    if ':' in href and not (href.startswith('http://') or href.startswith('https://')):
        # Things like 'javascript:foo()' and whatever
        return False

    return True
