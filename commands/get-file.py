
import generate as gen
import md5
import parse

from cmd_base import *

class GetFile (SimpleCommand):
    _cmd = 'get-file'

    def do_cmd(self):
        repos = self.link.repos
        args = self.args
        url = self.link.url
        rev = None

        path = parse.string(args[0])
        if len(path) > 0:
            url = '/'.join((url, path))

        if len(args[1]) > 0:
            rev = int(args[1][0])

        want_props = parse.bool(args[2])
        want_contents = parse.bool(args[3])

        print "props: %s, contents: %s" % (want_props, want_contents)

        rev, props, contents = repos.get_file(url, rev)

        p = []
        if want_props:
            for name, value in props:
                p.append(gen.list(gen.string(name), gen.string(value)))

        m = md5.new()
        data = contents.read(8192)
        total_len = len(data)
        while len(data) > 0:
            m.update(data)
            data = contents.read(8192)
            total_len += len(data)
        csum = gen.string(m.hexdigest())

        response = (gen.list(csum), rev, gen.list(*p))

        self.link.send_msg(gen.success(*response))

        if want_contents:
            if total_len == len(data):
                self.link.send_msg(gen.string(data))
            else:
                contents.reopen()
                data = contents.read(8192)
                while len(data) > 0:
                    self.link.send_msg(gen.string(data))
                    data = contents.read(8192)
            self.link.send_msg(gen.string(''))
            self.link.send_msg(gen.success())

        contents.close()
