import cherrypy
from MatchModule.string_parser import string_parser


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return '''<html>
          <head></head>
          <body>
            <form method="get" action="run_matcher">
              <input type="text" value="" name="words" />
              <button type="submit">Submit</button>
            </form>
          </body>
        </html>'''

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def run_matcher(self, words):
        parse = string_parser(words)
        x = parse.run()
        return x

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())


