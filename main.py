import os
import webapp2
import cgi
import re
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)
class Handler(webapp2.RequestHandler):
    def renderError(self, error):
        self.response.write(error)

class UserVerify(Handler):
    def get(self):
        t = jinja_env.get_template("signup-form.html")
        content = t.render(error_escaped=self.request.get("error"))
        self.response.write (content)
    def post(self):
        user_name = self.request.get("username")
        password = self.request.get("password")
        confirm_password = self.request.get("confirm")
        email =self.request.get("email")
        if not valid_username(user_name):
            error = " Please provide valid username"
            error_escaped = cgi.escape(error, quote=True)
            t = jinja_env.get_template("signup-form.html")
            content = t.render( error_escaped = error_escaped)
            self.response.write (content)
        if not valid_password(password):
            error = " Please provide valid password"
            error_escaped = cgi.escape(error, quote=True)
            t = jinja_env.get_template("signup-form.html")
            content = t.render( error_escaped = error_escaped)
            self.response.write (content)
        if (confirm_password == password)==False:
            error = "Password Verification failed"
            error_escaped = cgi.escape(error, quote=True)
            t = jinja_env.get_template("signup-form.html")
            content = t.render( error_escaped = error_escaped)
            self.response.write (content)

        self.redirect('/welcome?username=' + user_name)
class Welcome(Handler):
    def get(self):
        username = self.request.get("username")
        if valid_username(username):
            self.response.write("Welcome, " + username)
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', UserVerify),
    ('/welcome', Welcome),
], debug=True)
