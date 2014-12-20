import logging
import webapp2
import json
from google.appengine.api import users

from config_page import ConfigPage
import commands
import context
import entity


class MainPage(webapp2.RequestHandler):
  def get(self):
    template = context.jinja_environment.get_template('index.html')
    self.response.out.write(template.render({}))

class LogoutPage(webapp2.RequestHandler):
  def get(self):
    self.redirect(users.create_logout_url('/'))

class CommandPage(webapp2.RequestHandler):
  def post(self):
    logging.info(self.request)
    response = commands.run(self.request)
    if response:
      self.response.headers['Content-Type'] = 'text/plain; charset=utf-8'
      self.response.write(response.encode('utf-8'))

class KarmaPage(webapp2.RequestHandler):
  def get(self):
    entities = entity.Entity.all()
    data = {entity.key(): entity.score for entity in entities}
    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
    json.dump(data, self.response)

application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/logout', LogoutPage),
  ('/config', ConfigPage),
  ('/slash', CommandPage),
  ('/karma', KarmaPage),
], debug=True)
