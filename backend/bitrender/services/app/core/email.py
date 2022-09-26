from antidote import implements, wire

from bitrender.services.app.core import BaseAppService
from bitrender.services.app.interfaces.email import IEmailService


@wire
@implements(IEmailService)  # type: ignore
class EmailService(BaseAppService, IEmailService):
    """TODO generate docstring"""

    def __init__(self) -> None:
        BaseAppService.__init__(self)
