from fabric.api import run
from fabric.api import local
from fabric.api import settings
from datetime import datetime as dt
#RMA_TEST_SERVERNAME='crm1.corp.enlightedinc.com' # crm1.corp.enlightedinc.com
#RMA_TEST_SERVERNAME='10.8.3.10' # crm1.corp.enlightedinc.com
RMA_TEST_SERVERNAME='fogtest.com' # fogtest.com
#RMA_TEST_SERVER_USER='crm' # crm1.corp.enlightedinc.com
RMA_TEST_SERVER_USER='marc' # fogtest.com
#RMA_TEST_DEST='python_apps/django/rma_test' # crm1.corp.
RMA_TEST_DEST='python_test_apps/rma'
#RMA_TEST_RELOAD_FILE='/home/crm/python_apps/django/rma_test/rma/reload' # crm1.corp.enlightedinc.com
RMA_TEST_RELOAD_FILE='%sreload'%RMA_TEST_DEST # fogtest.com
RMA_TEST_PHP_DOC_DIR='/home/marc/sfgeek.net/rma_doc'
def sync():
    """
    sync with RMA_TEST_SERVERNAME test directory
    """
    local('find . | grep \.py$ | xargs chmod 644')
    local('rsync -arv --delete  --exclude "log.txt" --exclude "runwsgiserver.sh" --exclude "reload" --exclude \
    "pid.txt" --exclude "*/static/*" --exclude ".git"  --exclude "*.log" /home/marc/python_apps/django/rma/* %s@%s:%s/'%\
          (RMA_TEST_SERVER_USER, RMA_TEST_SERVERNAME, RMA_TEST_DEST))
    local('fab -H %s@%s post_sync_back'%(RMA_TEST_SERVER_USER, RMA_TEST_SERVERNAME ))


def post_sync_back():
    run('touch %s'%RMA_TEST_RELOAD_FILE)
def collect_static():
    local('fab -H crm@crm1.corp.enlightedinc.com collect_static_back')

def collect_static_back():
    pass
    run('python /home/crm/python_apps/django/rma_test/manage.py collectstatic --noinput')
def test_back():
    """
    run the document build and deploy on server.
    Only run the make on the test site.  Compiling the document causes the doc string tests to run and those tests
    might ruin good data.
    :return:
    """
    sync()
    with settings(warn_only=True):
        result = run('cd ~/python_apps/django/rma_test; python manage.py test #> test_coverage.txt 2>&1; cd .docs; make html')
        #build_dox_back()
def build_dox_back():
    """
    run the document build and deploy on server.
    Only run the make on the test site.  Compiling the document causes the doc string tests to run and those tests
    might ruin good data.
    :return:
    """
    run('cd %s; pip freeze > requirements.txt'%RMA_TEST_DEST)
    run('source envs/enlighted/bin/activate ; cd %s/docs; make html'%RMA_TEST_DEST)
    run('source envs/enlighted/bin/activate ; cd %s/docs/_build; rsync -avh html/*  %s'%(RMA_TEST_DEST, RMA_TEST_PHP_DOC_DIR))

def  build_dox_front():
    """
    call build_dox_back (locally) with hard coded credentials
    :return:
    """
    local('fab -H %s@%s build_dox_back'%(RMA_TEST_SERVER_USER, RMA_TEST_SERVERNAME))

def  test_front():
    """
    call build_dox_back (locally) with hard coded credentials
    :return:
    """
    local('fab -H crm@%s test_back'%RMA_TEST_SERVERNAME)

def restart_django_wsgi_back():
    """
    run touch reload on servers
    :return:
    """
    run('cd python_apps/django/rma/rma; touch reload')
    run('cd python_apps/django/rma_test/rma; touch reload')


def  restart_django_wsgi_front():
    """
    call build_dox_back (locally) with hard coded credentials
    :return:
    """
    local('fab -H crm@%s restart_django_wsgi_back'%RMA_TEST_SERVERNAME)

def dump_rma_test_app_data_front():
    local('fab -H crm@%s dump_rma_test_app_data_back'%RMA_TEST_SERVERNAME)

def dump_rma_test_app_data_back():
    """
    call python manage.py dumpdata on apps return_merchandise_authorizations, parts, customers, and commissioned_sites

    :return:
    """

    run('cd python_apps/django/rma_test/; python manage.py dumpdata --traceback return_merchandise_authorizations parts customers commissioned_sites auth_user > data/data.json')
