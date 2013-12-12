import webapp2
import os
import re

import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)

def verify_password(p_password, p_verify):
	return p_password == p_verify, PASSWORD_RE.match(p_password)

def verify_username(p_username):
	return USER_RE.match(p_username)

def verify_email(p_email):
	return p_email == '' or EMAIL_RE.match(p_email)

class BaseHandler(webapp2.RequestHandler):
	def render(self, template, **kw):
		self.response.out.write(render_str(template, **kw))

	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

class Signup(BaseHandler):
	def get(self):
		self.render('signup.html', username = "", email = "")

	def post(self):
		p_username = self.request.get("username")
		is_username_valid = verify_username(p_username)

		p_password = self.request.get("password")
		p_verify = self.request.get("verify")
		is_password_match, is_password_valid = verify_password(p_password, p_verify)

		p_email = self.request.get("email")
		is_email_valid = verify_email(p_email)

		if is_username_valid and is_password_match and is_password_valid and is_email_valid:
			self.redirect('/welcome?username=' + p_username)
		else:
			self.render('signup.html',
									username = p_username,
									email = p_email,
									error_username = "" if is_username_valid else "Username is invalid",
									error_password = "" if is_password_valid else "Password is invalid",
									error_verify= "" if is_password_match else "Passwords don't match",
									error_email = "" if is_email_valid else "Email is invalid")

class WelcomeHandler(BaseHandler):
	def get(self):
		self.render('welcome.html', username = self.request.get("username"))

app = webapp2.WSGIApplication([('/', Signup), ('/welcome', WelcomeHandler)], 
                              debug=True)
