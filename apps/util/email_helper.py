from dataclasses import dataclass
from typing import Optional


@dataclass
class EmailHelper:
    subject: Optional[str] = None
    body: Optional[str] = None
    from_email: Optional[str] = None
    to: Optional[list] = None
    bcc: Optional[list] = None
