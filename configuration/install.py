from string import Template
import sys
import subprocess
import os
from uuid import uuid4

HOME_PATH = os.environ['HOME']
CONF_PATH = os.path.join(HOME_PATH, 'vagrant_django', 'configuration')
SCRIPTS_PATH = os.path.join(HOME_PATH, 'vagrant_django', 'scripts')
VIRTUALENV_PATH = os.path.join(HOME_PATH, 'django_environment')

if not(sys.version_info > (3, 0)):
    print("You're not using python3. Use python3.")
    sys.exit()


def write_config_template_to_location(template, arguments, destination):
    """
    template: the name of the file in CONF_PATH that contains a python
        string.Template style template to render.
    arguments: a dictionary of arguments to pass to the template.
    destination: the place in the filesystem to write this file to.
    """
    print("Writing to {}".format(destination))
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
    print(os.environ)

    config_args['project_slug'] = default_input('What is the name of your django project?',
                                                default='butterbutt')
    config_args['domain'] = default_input('What domain will this site be located at?',
                                          default='butterbutt.butt')

    config_args['admin_name'] = default_input("What's your name?",
                                              default="Butter Butt")

    config_args['admin_email'] = default_input("What's your e-mail address?",
                                               default="butter@butts.org")

    config_args['mandrill_key'] = default_input("Go to mandrill.com and make an account. Then type your API key in here.",
                                            default="Nope")

    config_args['secret_key'] = str(uuid4())
    config_args['db_password'] = str(uuid4())
    config_args['django_path'] = os.path.join(HOME_PATH, 'vagrant_django', config_args['project_slug'])
    config_args['virtualenv_path'] = VIRTUALENV_PATH

    print(config_args)

    manage_path = os.path.join(config_args['django_path'], 'manage.py')

    # Modify bashrc with helpers
    bashrc_path = os.path.join(HOME_PATH, '.bashrc')
    write_config_template_to_location(template='template.bashrc',
                                      arguments=config_args,
                                      destination=bashrc_path)

    # Put tasks.py in place
    tasks_path = '{}/tasks.py'.format(os.path.join(HOME_PATH, 'vagrant_django'))
    if not os.path.exists(tasks_path):
        write_config_template_to_location(template='template.tasks.py',
                                          arguments=config_args,
                                          destination=tasks_path)

    # Put settings.py in place
    settings_path = os.path.join(config_args['django_path'], config_args['project_slug'], 'settings.py')
    local_settings_path = os.path.join(config_args['django_path'], config_args['project_slug'], 'local_settings.py')
    write_config_template_to_location(template='template.settings.py',
                                      arguments=config_args,
                                      destination=settings_path)
    if not os.path.exists(local_settings_path):
        write_config_template_to_location(template='template.local.settings.py',
                                          arguments=config_args,
                                          destination=local_settings_path)

    # Put NGINX configuration in place
    nginx_config_path = '/etc/nginx/sites-available/{}'.format(config_args['project_slug'])
    nginx_enabled_path = '/etc/nginx/sites-enabled/{}'.format(config_args['project_slug'])
    write_config_template_to_location(template='template.nginx.conf',
                                      arguments=config_args,
                                      destination=nginx_config_path)
    subprocess.call("ln -s {} {}".format(nginx_config_path, nginx_enabled_path).split())

    # Put UWSGI configuration in place
    write_config_template_to_location(template='template.uwsgi.sh',
                                      arguments=config_args,
                                      destination='{}/uwsgi.sh'.format(SCRIPTS_PATH))
    subprocess.call("chmod a+x {}/uwsgi.sh".format(SCRIPTS_PATH).split())


    # Put Redis configuration in place
    subprocess.call("mv /etc/redis/redis.conf /etc/redis/redis.conf.backup".split())
    subprocess.call("ln -s {}/template.redis.conf /etc/redis/redis.conf".format(CONF_PATH).split())

    # Put all scripts in place
    scripts = ['template.create_postgres.sh',
               'template.backup_postgres.sh',
               'template.rebuild_postgres.sh',
               'template.reset_postgres.sh']
    for script in scripts:
        filename = script[9:]
        dest = os.path.join(SCRIPTS_PATH, filename)
        write_config_template_to_location(template=script,
                                          arguments=config_args,
                                          destination=dest)
        subprocess.call("dos2unix {}".format(dest).split())

    # Create PostgreSQL Database
    postgres_call = "bash {}/create_postgres.sh".format(SCRIPTS_PATH)
    subprocess.call(postgres_call.split())
