from datetime import datetime, timedelta

import jwt

from simpleserver.util.consts import ENTER, EXIT
from simpleserver.util.logger import SSLogger
from simpleserver.util.props import Props


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
        # exp = datetime.utcnow() + timedelta(seconds=-1)
        my_claim = {'email': user_email, 'exp': exp}
        token = jwt.encode(my_claim, 'secret', algorithm='HS256')
        ret = token.decode("utf-8")
        self.mySessions.add(ret)
        self.myLogger.debug(EXIT)
        return ret

    def validate_json_web_token(self, token):
        """Validates the token. Returns {:email :exp} from token if session ok, None otherwise.
        Token validation has two parts:
        1. Check that we actually created the token in the first place (should find it in my-sessions set.
        2. Validate the actual token (can unsign it, token is not expired)."""
        self.myLogger.debug(ENTER)
        ret = None
        # Validation #1:
        if not (token in self.mySessions):
            self.myLogger.warning('Token not found in my sessions - unknown token: ' + token)
        else:  # Validation #2:
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
        my_props = Props()
        self.expire_seconds = int(my_props.get_property('json-web-token-expiration-as-seconds'))




