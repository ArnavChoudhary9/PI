#type vertex
#version 450 core

layout(location=0) in vec2 a_TexCoord;
layout(location=1) in vec3 a_Normal;
layout(location=2) in vec3 a_Position;

uniform mat4 u_Transform;
uniform mat4 u_ViewProjection;

void main() {
    gl_Position = u_ViewProjection * u_Transform * vec4(a_Position, 1.0);
}

#type pixel
#version 450 core

struct Material {
    vec3 Diffuse;
};

layout(location=0) out vec4 color;
layout(location=1) out int  entityID;

uniform Material u_Material;
uniform int u_EntityID;

void main() {
    color = vec4(u_Material.Diffuse, 1.0);
    entityID = u_EntityID;
}
