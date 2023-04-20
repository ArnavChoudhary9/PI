from PI import *
from PI.Scripting import *

class CameraFire(Behaviour):
    Speed: float = 10

    def OnUpdate(self, dt: float) -> None:
        forward = pyrr.quaternion.apply_to_vector(
            pyrr.quaternion.create_from_eulers(-self._Transform.Rotation),
            pyrr.Vector3([ 0.0, 0.0, 1.0 ])
        )
        right = pyrr.quaternion.apply_to_vector(
            pyrr.quaternion.create_from_eulers(-self._Transform.Rotation),
            pyrr.Vector3([ 1.0, 0.0, 0.0 ])
        )
        up = pyrr.quaternion.apply_to_vector(
            pyrr.quaternion.create_from_eulers(-self._Transform.Rotation),
            pyrr.Vector3([ 0.0, 1.0, 0.0 ])
        )

        if Input.IsMouseButtonPressed(MouseButtonCodes.PI_MOUSE_BUTTON_LEFT):
            entity = self.InstanciateEntity("Bullet")

            trans = entity.GetComponent(TransformComponent)
            trans.SetScale(pyrr.Vector3([ 0.1, 0.1, 0.1 ]))
            trans.SetTranslation(self._Transform.Translation.copy() - forward)
            
            entity.AddComponent(ScriptComponent, "Bullet", "Bullet")
            entity.AddComponent(MeshComponent, "InternalAssets\\Meshes\\Sphere.obj")

            collidor = entity.AddComponent(CollidorComponent,
                CollidorComponent.Shapes.Box, scale=pyrr.Vector3([ 0.1, 0.1, 0.1 ])
            )
            rb = entity.AddComponent(RigidBodyComponent, PySicsMaterial(
                mass=0.01,
                position=trans.Translation,
                rotation=trans.Rotation,
                collider=collidor.Collidor
            ))

            rb.RigidBody.ApplyCentralForce(-forward * 500)

        if Input.IsKeyPressed(KeyCodes.PI_KEY_A): self._Transform.Translate(-right*self.Speed*dt)
        if Input.IsKeyPressed(KeyCodes.PI_KEY_D): self._Transform.Translate( right*self.Speed*dt)
        
        if Input.IsKeyPressed(KeyCodes.PI_KEY_S): self._Transform.Translate(-up*self.Speed*dt)
        if Input.IsKeyPressed(KeyCodes.PI_KEY_W): self._Transform.Translate( up*self.Speed*dt)
