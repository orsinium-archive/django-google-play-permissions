import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    """Make session that retry request on error
    """
    # get session
    session = session or requests.Session()
    # make retry rule
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    # make adapter
    adapter = HTTPAdapter(max_retries=retry)
    # mount adapter to session
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
