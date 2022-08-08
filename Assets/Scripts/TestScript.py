from PI import *
from PI.Scripting import *

from pyrr import Vector3

class TestScript(Behaviour):
    # Only Annotations will also work,
    # but there type shuld have constructor with no arguments
    TestStr    : str
    TestFloat  : float
    TestInt    : int
    TestBool   : bool
    TestVector : Vector3
    TestColor  : Color4
