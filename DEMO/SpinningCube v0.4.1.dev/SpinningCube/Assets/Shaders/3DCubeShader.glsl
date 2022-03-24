#type vertex
#version 330 core

layout(location=0) in vec3 a_Position;
layout(location=1) in vec4 a_Color;

uniform mat4 u_Translation;
uniform mat4 u_Rotation;
uniform mat4 u_Scale;

uniform mat4 u_ViewProjection;

out vec4 v_Color;

void main() {
    v_Color = a_Color;
    gl_Position = u_ViewProjection * u_Translation * u_Rotation * u_Scale * vec4(a_Position, 1.0);
}

#type pixel
#version 330 core

layout(location=0) out vec4 out_Color;

in vec4 v_Color;

void main() {
    // out_Color = vec4(0.8, 0.8, 0.8, 1);
    out_Color = v_Color;
}
