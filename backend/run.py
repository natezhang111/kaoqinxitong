<<<<<<< HEAD
from __future__ import annotations

import uvicorn

from app.core.config import DEBUG, HOST, PORT

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
    )
=======
from __future__ import annotations

import uvicorn

from app.core.config import DEBUG, HOST, PORT

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
    )
>>>>>>> 98bf8e49 (update)
