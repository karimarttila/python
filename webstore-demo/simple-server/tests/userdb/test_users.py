from simpleserver.util.consts import ENTER, EXIT
from simpleserver.util.logger import SSLogger
from simpleserver.userdb.users import Users

myLogger = SSLogger(__name__).get_logger()
myUsers = Users()


def test_email_already_exists():
    myLogger.debug(ENTER)
    found = myUsers.email_already_exists('timo.tillinen@foo.com')
    assert found is True
    found = myUsers.email_already_exists('NOT.FOUND@foo.com')
    assert found is False
    myLogger.debug(EXIT)


def test_add_user():
    myLogger.debug(ENTER)
    ret = myUsers.add_user('jamppa.jamppanen@foo.com', 'Jamppa', 'Jamppanen', 'passw0rd')
    assert ret is not None
    assert ret['ret'] == 'ok'
    assert ret['email'] == 'jamppa.jamppanen@foo.com'
    # Trying to add Jamppa again.
    ret = myUsers.add_user('jamppa.jamppanen@foo.com', 'Jamppa', 'Jamppanen', 'passw0rd')
    assert ret is not None
    assert ret['ret'] == 'failed'
    assert ret['email'] == 'jamppa.jamppanen@foo.com'
    assert ret['msg'] == 'Email already exists'
    myLogger.debug(EXIT)


def test_check_credentials():
    myLogger.debug(ENTER)
    ret = myUsers.check_credentials('kari.karttinen@foo.com', 'Kari')
    assert ret is True
    ret = myUsers.check_credentials('kari.karttinen@foo.com', 'WRONG-PASSWORD')
    assert ret is False
    myLogger.debug(EXIT)


