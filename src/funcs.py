import time
import src.database
import src.store.settings

def validate_flt(flt: src.database.DFlight):
  if (time.time() - int(str(flt.last_updated)) > 30) or float(
    str(flt.distance_to_destination)
  ) < float(str(flt.distance_to_origin)) or not str(flt.origin).startswith(src.store.settings.ORIGIN_PREFIX) or (src.store.settings.REQUIRE_SQUAWK and flt.squawk is None):
    return False
  else:
    return True