"""
This module provides plans for controlling the beam shutter and safety interlocks
at the 8ID-E station.
"""

# B-PILOT (the plan-runner GUI) offers these as plain-Python calls (no RE()). Leading
# underscore => never star-exported, so this changes nothing at runtime.
__bpilot_python__ = [
    "showbeam",
    "blockbeam",
    "shutteron",
    "shutteroff",
    "pre_align",
    "post_align",
    "PIND_status",
    "att",
]


from apsbits.core.instrument_init import oregistry
import epics as pe
import time

shutter_8ide = oregistry["shutter_8ide"]
pd = oregistry["pd"]
filter_beam = oregistry["filter_8ide"]
softglue = oregistry["softglue"]

def showbeam():
    """Open the beam shutter to show the beam."""
    shutter_8ide.operation.put(0)
    time.sleep(0.05)

def blockbeam():
    """Block the beam by closing the shutter."""
    shutter_8ide.operation.put(1)
    time.sleep(0.05)

def shutteron():
    """Enable the shutter control logic."""
    shutter_8ide.logic.put(0)
    time.sleep(0.5)

def shutteroff():
    """Disable the shutter control logic."""
    shutter_8ide.logic.put(1)
    time.sleep(0.5)

def post_align():
    """Configure system for post-alignment state by blocking the beam."""
    pe.caput("8idiSoft:FLIGHT:bo1:8", 1)
    blockbeam()
    time.sleep(0.5)

def pre_align():
    """Configure system for pre-alignment state by disabling shutter control."""
    pe.caput("8idiSoft:FLIGHT:bo1:8", 0)
    softglue.enable_rigaku.put('0')
    shutteroff()
    time.sleep(0.5)

def PIND_status(status=0):
    """Remove the PIND from the beam path.

    Parameters
    ----------
    status : int
        status :: Value written to pd.active; the default 0 removes the PIND from the beam path.
    """
    pd.active.put(status)

def att(att_ratio: float=1.0):
    """Set the attenuation ratio with multiple attempts.

    Parameters
    ----------
    att_ratio : float
        attenuation ratio :: Attenuation ratio to set. Values below 1.0 are raised to 1.0 (the original note gives a 0-15 range).
    """
    if att_ratio < 1.0:
        att_ratio = 1.0
    else:
        pass
    filter_beam.attenuation.move(att_ratio)
    time.sleep(0.5)
