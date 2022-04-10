#type vertex
#version 330 core

layout(location=0) in vec2 a_TexCoord;
layout(location=1) in vec3 a_Normal;
layout(location=2) in vec3 a_Position;

uniform mat4 u_Transform;
uniform mat4 u_ViewProjection;

out vec2 v_TexCoord;
out vec3 v_Normal;
out vec3 v_FragPos;

void main() {
    v_TexCoord = a_TexCoord;
    v_Normal = mat3(transpose(inverse(u_Transform))) * a_Normal;
    v_FragPos = vec3(u_Transform * vec4(a_Position, 1.0));
    gl_Position = u_ViewProjection * u_Transform * vec4(a_Position, 1.0);
}

#type pixel
#version 330 core

struct Material {
    vec3 Ambient;
    vec3 Diffuse;
    vec3 Specular;
    float Shininess;
};

struct Light {
    vec3 Position;

    vec3 Ambient;
    vec3 Diffuse;
    vec3 Specular;
};

layout(location=0) out vec4 color;

in vec2 v_TexCoord;
in vec3 v_Normal;
in vec3 v_FragPos;

uniform Material u_Material;
uniform Light u_Light;

uniform sampler2D u_Texture;

uniform vec3 u_CameraPos;

// Light info
uniform vec3 u_LightColor;
uniform vec3 u_LightPos;

void main() {
    // Ambient
    vec3 ambient = u_Light.Ambient * u_Material.Ambient;

    // Diffuse
    vec3 norm = normalize(v_Normal);
    vec3 lightDir = normalize(u_Light.Position - v_FragPos);

    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = u_Light.Diffuse * (diff * u_Material.Diffuse);

    // Specular
    vec3 viewDir = normalize(u_CameraPos - v_FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);

    float spec = pow(max(dot(viewDir, reflectDir), 0.0), u_Material.Shininess);
    vec3 specular = u_Light.Specular * (spec * u_Material.Specular);

    // Final combining
    vec3 result = ambient + diffuse + specular;
    color = vec4(result, 1.0);
}
