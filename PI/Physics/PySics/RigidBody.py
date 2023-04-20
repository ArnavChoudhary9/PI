from .Colliders import *
from .Utility   import *

class Axis:
    X: pyrr.Vector3 = pyrr.Vector3([ 1, 0, 0 ])
    Y: pyrr.Vector3 = pyrr.Vector3([ 0, 1, 0 ])
    Z: pyrr.Vector3 = pyrr.Vector3([ 0, 0, 1 ])

class PySicsMaterial:
    Mass: float

    Position: pyrr.Vector3
    Rotation: pyrr.Vector3
    Collider: Collider

    IsStatic : bool
    CCD      : bool

    def __init__(self,
        mass     : float=1.0,
        position : pyrr.Vector3=pyrr.Vector3([ 0, 0, 0 ]),
        rotation : pyrr.Vector3=pyrr.Vector3([ 0, 0, 0 ]),
        collider : Collider=None,
        isStatic : bool=False,
        ccd      : bool=True
    ) -> None:
        self.Mass     = mass

        self.Position = position
        self.Rotation = rotation
        self.Collider = collider

        self.IsStatic = isStatic
        self.CCD      = ccd

class RigidBody:
    Mass: float

    Position: pyrr.Vector3
    Rotation: pyrr.Vector3
    Velocity: pyrr.Vector3

    Collider: Collider

    AllowMovement: pyrr.Vector3
    AllowRotation: pyrr.Vector3

    IsStatic : bool
    CCD      : bool

    _Node: Any      # For Book Keeping

    __CentralForce: pyrr.Vector3
    __CentralTorque: pyrr.Vector3

    def __init__(self, mat: PySicsMaterial) -> None:
        self.Mass     = mat.Mass

        self.Position = mat.Position
        self.Rotation = mat.Rotation
        self.Velocity = pyrr.Vector3([ 0, 0, 0 ])

        self.Collider = mat.Collider

        self.AllowMovement = Axis.X + Axis.Y + Axis.Z
        self.AllowRotation = Axis.X + Axis.Y + Axis.Z

        self.IsStatic = mat.IsStatic
        self.CCD = mat.CCD

        self.__CentralForce  = pyrr.Vector3([ 0, 0, 0 ])
        self.__CentralTorque = pyrr.Vector3([ 0, 0, 0 ])

        if mat.IsStatic: self.Mass = 0.0

    def __repr__(self) -> str:
        s = "-" * 50
        s +=  "\n<RigidBody>:\n"
        s += f"\tMass: {self.Mass}\n"
        s += f"\tIs Static: {self.IsStatic}\n\n"
        s += f"\tPosition: {self.Position}\n"
        s += f"\tRotation: {self.Rotation}\n"
        s += f"\tVelocity: {self.Velocity}\n\n"
        s += f"\tCollider: {self.Collider}\n\n"
        s += f"\tMovement Allowed in: {self.AllowMovement}\n"
        s += f"\tRotation Allowed in: {self.AllowRotation}\n"
        s += "-" * 50
        s += "\n"

        return s

    @property
    def CentralForce  (self) -> pyrr.Vector3: return self.__CentralForce
    @property
    def CentralTorque (self) -> pyrr.Vector3: return self.__CentralTorque

    def ApplyCentralForce  (self, force  : pyrr.Vector3) -> None: self.__CentralForce  = self.__CentralForce  + force
    def ApplyCentralTorque (self, torque : pyrr.Vector3) -> None: self.__CentralTorque = self.__CentralTorque + torque

    def _SetCentralForce  (self, force  : pyrr.Vector3=pyrr.Vector3([ 0, 0, 0 ])): self.__CentralForce  = force
    def _SetCentralTorque (self, torque : pyrr.Vector3=pyrr.Vector3([ 0, 0, 0 ])): self.__CentralTorque = torque
