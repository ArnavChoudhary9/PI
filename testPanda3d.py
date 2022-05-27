from panda3d.bullet import BulletWorld, BulletRigidBodyNode, BulletBoxShape
from panda3d.core   import Vec3, TransformState, VBase3

# help(BulletRigidBodyNode)

world = BulletWorld()
world.setGravity(Vec3(0, 0, -9.81))

shape = BulletBoxShape(Vec3(1, 1, 1))
node  = BulletRigidBodyNode("Box")
node.addShape(shape)
node.setMass(1.0)
node.setTransform( TransformState.makePos(VBase3(0, 0, 1)) )
world.attachRigidBody(node)

for _ in range(60):
    node.applyTorque(Vec3(1, 0, 0))
    world.doPhysics(1 / 60)

print(Vec3(0, 0, 0), node.getTransform(), node.getAngularVelocity(), node.getLinearVelocity(), sep="\n")
