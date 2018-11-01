from simpleserver.util.consts import ENTER, EXIT
from simpleserver.util.logger import SSLogger
from simpleserver.webserver.session import Session

myLogger = SSLogger(__name__).get_logger()
mySession = Session()


def test_json_web_token():
    myLogger.debug(ENTER)
    jwt = mySession.create_json_web_token('jamppa.tuominen@foo.com')
    assert jwt is not None
    assert len(jwt) > 20
    ret = mySession.validate_json_web_token(jwt)
    assert ret is not None
    assert ret['email'] == 'jamppa.tuominen@foo.com'
    myLogger.debug(EXIT)
