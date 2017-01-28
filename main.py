
import webapp2
import cgi
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Sign UP</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">User Signup</a>
    </h1>
"""
page_footer = """
</body>
</html>
"""
empty_space = " "
class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.flicklist.com/
    """
    def get(self):

        user_signup_form = """
        <div><form action="/userverify" method="post">
            <label>
            <span>Username</span>
                <input type="text" name="username"/><br>
            </label><br>
            <label>
            Password
                <input type="text" name="password"/><br>
            </label><br>
            <label>
            Confirm Pasword
                <input type="text" name="confirm"/><br>
            </label><br>
            <label>
            Email(Optional)
                <input type="text" name="email"/><br>
            </label>
            <buton><input type="submit" value="Submit"/></button>
        </form></div>
        """
        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""
        main_content = page_header + user_signup_form + error_element
        content = main_content + page_footer
        self.response.write(content)
class UserVerify(webapp2.RequestHandler):
    """ Handles requests coming in to '/add'
        e.g. www.flicklist.com/add
    """
    def post(self):
        user_name = self.request.get("username")
        password = self.request.get("password")
        confirm_password = self.request.get("confirm")
        email =self.request.get("email")
        if (empty_space in user_name):
            error = "'{0}' Please provide valid username".format(user_name)
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)

        elif (len( user_name)<1):
            error = "'{0}' Please provide valid username".format(user_name)
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)
        main_content = "<strong>"+ "Well Come, " + user_name.capitalize() +"</strong>"
        content =  main_content + page_footer
        self.response.write(content)
        if (empty_space in password):
            error = "'{0}' Please provide valid password".format(password)
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)

        elif (len( password)<1):
            error = "'{0}' Please provide valid password".format(password)
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)

        content =   ''
        self.response.write(content)
        if (confirm_password == password)==False:
            error = "'{0}' Password Verification failed".format(confirm_password)
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)
        content =   ''
        self.response.write(content)
        if (empty_space in email):
            error = "'{0}' Please provide valid email".format(email)
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)

        elif (len( email)<1):
            error = "'{0}' Please provide valid username".format(email)
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)
        content =   ''
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/userverify', UserVerify)
], debug=True)
