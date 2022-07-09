from typing import Any, Dict
from screeninfo import get_monitors


def get_screen_params(number_screens=1) -> Dict[str, Any]:

    cnt = 1
    for m in get_monitors():
        if cnt == number_screens:
            break
        cnt += 1

    return {"height": m.height, "width": m.width}
