#type vertex
#version 330 core

layout(location=0) in vec2 a_TexCoord;
layout(location=1) in vec3 a_Normal;
layout(location=2) in vec3 a_Position;

uniform mat4 u_Transform;
uniform mat4 u_ViewProjection;

out vec2 v_TexCoord;

void main() {
    v_TexCoord = a_TexCoord;
    gl_Position = u_ViewProjection * u_Transform * vec4(a_Position, 1.0);
}

#type pixel
#version 330 core

layout(location=0) out vec4 color;

in vec2 v_TexCoord;

uniform vec4 u_Color;
uniform float u_Specular;
uniform sampler2D u_Texture;

uniform vec3 u_CameraPos;

// This is so that we do not have to check in actual Material class
// Light info
uniform vec3 u_LightColor;
uniform vec3 u_LightPos;

void main() {
    // color = texture(u_Texture, v_TexCoord) * u_Color;
    color = u_Color;
}
