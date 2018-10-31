from simpleserver.util.consts import ENTER, EXIT
from simpleserver.util.logger import SSLogger
from simpleserver.util.props import Props
from datetime import datetime, timedelta
import jwt


class Session:
    """Session class."""

    myLogger = SSLogger(__name__).get_logger()
    mySessions = set()

    def create_json_web_token(self, user_email) -> str:
        """Creates and returns a json web token,
        and adds the token to sessions."""
        self.myLogger.debug(ENTER)
        exp = datetime.utcnow() + timedelta(seconds=self.expire_seconds)
        # Quick hack testing expired token.
        #exp = datetime.utcnow() + timedelta(seconds=-1)
        myClaim = {'email': user_email, 'exp': exp}
        ret = jwt.encode(myClaim, 'secret', algorithm='HS256')
        self.mySessions.add(ret)
        self.myLogger.debug(EXIT)
        return ret

    def validate_json_web_token(self, token) -> str:
        """Validates the token. Returns {:email :exp} from token if session ok, None otherwise.
        Token validation has two parts:
        1. Check that we actually created the token in the first place (should find it in my-sessions set.
        2. Validate the actual token (can unsign it, token is not expired)."""
        self.myLogger.debug(ENTER)
        ret = None
        # Validation #1:
        if (not token in self.mySessions):
            self.myLogger.warning('Token not found in my sessions - unknown token: ' + jwt);
        else: # Validation #2:
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                ret = {'email': payload['email']}
            except jwt.ExpiredSignatureError:
                self.myLogger.warning('Signature expired. Please log in again.')
            except jwt.InvalidTokenError:
                self.myLogger.warning('Invalid token. Please log in again.')
        self.myLogger.debug(EXIT)
        return ret


    def __init__(self):
        myProps = Props()
        self.expire_seconds = int(myProps.get_property('json-web-token-expiration-as-seconds'))



