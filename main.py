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
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
class Index(Handler):
    def get(self):
        t = jinja_env.get_template("signup-form.html")
        content = t.render(error=self.request.get("error"))
        self.response.write (content)
class UserVerify(Handler):
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        confirm_password = self.request.get("confirm")
        email =self.request.get("email")
        have_error = False
        params = dict(username = username,
                      email = email)
        if not valid_username(username):
            params['error_username'] = " Please provide valid username"
            have_error = True

        if not valid_password(password):
            params['error_password'] = " Please provide valid password"
            have_error = True

        if (confirm_password == password)==False:
            params['error_verify'] = "Password Verification failed"
            have_error = True
        if not valid_email(email):
            params['error_verify'] = " Please provide valid E-mail"
            have_error = True
        if have_error:
            self.render('signup-form.html', **params)
        else:

            self.response.write("Welcome, " + "<strong>" + username + "<strong>")
#class Welcome(Handler):
    #def get(self):
    #    username = self.request.get("username")
    #    if valid_username(username):
    #        self.response.write("Welcome, " + username)
    #    else:
    #        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/userverify', UserVerify),
], debug=True)
