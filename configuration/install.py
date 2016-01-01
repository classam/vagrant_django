from string import Template
import sys
import subprocess
import os
from uuid import uuid4

if not(sys.version_info > (3, 0)):
    print("You're not using python3. Use python3.")
    sys.exit()

HOME_PATH = os.environ['HOME']
THREEPANEL_PATH = os.path.join(HOME_PATH, 'threepanel', 'threepanel')
CONF_PATH = os.path.join(HOME_PATH, 'threepanel', 'configuration')

def write_config_template_to_location(template, arguments, destination):
    """
    template: the name of the file in CONF_PATH that contains a python
        string.Template style template to render.
    arguments: a dictionary of arguments to pass to the template.
    destination: the place in the filesystem to write this file to.
    """
    with open(os.path.join(CONF_PATH, template), 'r') as template_file:
        template = Template(template_file.read())
        rendered_template = template.substitute(arguments)
    with open(destination, 'w') as target_file:
        target_file.write(rendered_template)

def default_input(question, default):
    returnval = input(question + " [{}]: ".format(default))
    if returnval.strip() == "":
        returnval = default
    return returnval.strip()

if __name__ == '__main__':
    config_args = {}
    config_args['home'] = HOME_PATH
    config_args['debug'] = 'True'
    config_args['project_slug'] = default_input('Give this project a name.',
                                                default='project_awesomesauce')
    config_args['domain'] = default_input('What domain will this site be located at?',
                                          default='cube-drone.com')
    config_args['admin_name'] = default_input("What's your name?",
                                              default="Sexy McMann")
    config_args['admin_email'] = default_input("What's your e-mail address?",
                                               default="butts@butts.org")

    config_args['mandrill_key'] = default_input("Go to mandrill.com and make an account. Then type your API key in here.",
                                            default="Nope")
    config_args['secret_key'] = str(uuid4())
    config_args['db_password'] = str(uuid4())

    domain = config_args['domain']

    print(config_args)

    # Put settings.py in place
    settings_path = os.path.join(HOME_PATH, 'threepanel', 'threepanel', 'threepanel', 'settings.py')
    write_config_template_to_location(template='template.settings.py',
                                      arguments=config_args,
                                      destination=settings_path)

    # Put NGINX configuration in place
    write_config_template_to_location(template='template.nginx.conf',
                                      arguments=config_args,
                                      destination='/etc/nginx/sites-available/{}'.format(domain))

    # Put UWSGI configuration in place
    write_config_template_to_location(template='template.uwsgi.sh',
                                      arguments=config_args,
                                      destination='{}/uwsgi.sh'.format(HOME_PATH))
    subprocess.call("chmod a+x {}/uwsgi.sh".format(HOME_PATH).split())

    # Make Threepanel available
    subprocess.call("ln -s /etc/nginx/sites-available/{} /etc/nginx/sites-enabled/{}".format(domain, domain).split())

    # Put Redis configuration in place
    subprocess.call("mv /etc/redis/redis.conf /etc/redis/redis.conf.backup".split())
    subprocess.call("ln -s {}/template.redis.conf /etc/redis/redis.conf".format(CONF_PATH).split())

    # Oh god Windows fucks up line endings so bad
    subprocess.call("dos2unix {}/create_postgres.sh".format(CONF_PATH).split())

    # Create PostgreSQL Database
    postgres_call = "bash {}/create_postgres.sh {}".format(CONF_PATH, config_args['db_password'])
    print(postgres_call)
    subprocess.call(postgres_call.split())
