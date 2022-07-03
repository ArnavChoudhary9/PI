#type vertex
#version 450 core

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
#version 450 core

struct Material {
    sampler2D AlbedoMap;
    sampler2D SpecularMap;

    float TilingFactor;

    int IsSpecularTexture;

    vec3 Diffuse;
    vec3 Specular;

    float Shininess;
};

struct DirectionalLight {
    // All Lights have these properties
    vec3 Position;

    vec3 Ambient;
    vec3 Diffuse;
    vec3 Specular;

    float Intensity;

    // Directional Light specific property
    vec3 Direction;
};

struct PointLight {
    // All Lights have these properties
    vec3 Position;

    vec3 Ambient;
    vec3 Diffuse;
    vec3 Specular;

    float Intensity;

    // Point Light specific property
    float ConstantFactor;
    float LinearFactor;
    float QuadraticFactor;
};

struct SpotLight {
    // All Lights have these properties
    vec3 Position;

    vec3 Ambient;
    vec3 Diffuse;
    vec3 Specular;

    float Intensity;

    // Spot Light specific properties
    vec3 Direction;
    float CutOff;
    float OuterCutOff;

    // Technically a spot light is also a point light
    float ConstantFactor;
    float LinearFactor;
    float QuadraticFactor;
};

#define MAX_POINT_LIGHTS 32
#define MAX_SPOT_LIGHTS  32

layout(location=0) out vec4 color;
layout(location=1) out int  entityID;

in vec2 v_TexCoord;
in vec3 v_Normal;
in vec3 v_FragPos;

uniform Material u_Material;

// Lights
uniform DirectionalLight u_DirectionalLight;
uniform PointLight       u_PointLights[MAX_POINT_LIGHTS];
uniform SpotLight        u_SpotLights [MAX_SPOT_LIGHTS];

uniform int u_NumPointLights;      // This is just to save time not looping over all lights
uniform int u_NumSpotLights;       // This is just to save time not looping over all lights

uniform vec3 u_CameraPos;
uniform int  u_EntityID;

vec3 CalculateDirectionalLight_Textured(vec3, vec3, vec2);
vec3 CalculatePointLight_Textured(vec3, vec3, vec2);
vec3 CalculateSpotLight_Textured(vec3, vec3, vec2);

void main() {
    // These values are common to all lights
    // so they are precomputed.
    vec3 norm = normalize(v_Normal);
    vec3 viewDir = normalize(u_CameraPos - v_FragPos);

    // Combining all the lights
    vec3 result = vec3(0.0, 0.0, 0.0);

    vec2 coords = v_TexCoord * u_Material.TilingFactor;

    result += CalculateDirectionalLight_Textured(norm, viewDir, coords);
    result += CalculatePointLight_Textured(norm, viewDir, coords);
    result += CalculateSpotLight_Textured(norm, viewDir, coords);

    // Ambient is just calculated for the directional Light
    // So all lights will not add their respective ambients
    // making the scene look bright
    vec3 ambient = u_DirectionalLight.Ambient * vec3(texture(u_Material.AlbedoMap, coords)) * u_Material.Diffuse;
    result += ambient;

    color = vec4(result, 1.0);
    entityID = u_EntityID;
}

vec3 CalculateDirectionalLight_Textured(vec3 norm, vec3 viewDir, vec2 coords) {
    // Diffuse
    vec3 lightDir = normalize(-u_DirectionalLight.Direction);

    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = u_DirectionalLight.Diffuse * diff * vec3(texture(u_Material.AlbedoMap, coords)) * u_Material.Diffuse;

    // Specular
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), u_Material.Shininess);

    vec3 specular;
    if (u_Material.IsSpecularTexture == 1) {
        specular = u_DirectionalLight.Specular * spec * vec3(texture(u_Material.SpecularMap, coords));
    } else {
        specular = u_DirectionalLight.Specular * (spec * u_Material.Specular);
    }

    // Final combining
    return (diffuse + specular) * u_DirectionalLight.Intensity;
}

vec3 CalculatePointLight_Textured(vec3 norm, vec3 viewDir, vec2 coords) {
    vec3 result = vec3(0.0, 0.0, 0.0);

    for (int i = 0; i < u_NumPointLights; i++) {
        // Diffuse
        vec3 lightDir = normalize(u_PointLights[i].Position - v_FragPos);

        float diff = max(dot(norm, lightDir), 0.0);
        vec3 diffuse = u_PointLights[i].Diffuse * diff * vec3(texture(u_Material.AlbedoMap, coords)) * u_Material.Diffuse;

        // Specular
        vec3 reflectDir = reflect(-lightDir, norm);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), u_Material.Shininess);

        vec3 specular;
        if (u_Material.IsSpecularTexture == 1) {
            specular = u_PointLights[i].Specular * spec * vec3(texture(u_Material.SpecularMap, coords));
        } else {
            specular = u_PointLights[i].Specular * (spec * u_Material.Specular);
        }

        // Attenuation
        float distance = length(u_PointLights[i].Position - v_FragPos);
        float attenuation = 1.0 / (
            u_PointLights[i].ConstantFactor +
            u_PointLights[i].LinearFactor * distance +
            u_PointLights[i].QuadraticFactor * distance * distance
        );

        // Final combining
        result += (diffuse + specular) * attenuation;
    }

    return result;
}

vec3 CalculateSpotLight_Textured(vec3 norm, vec3 viewDir, vec2 coords) {
    vec3 result = vec3(0.0, 0.0, 0.0);

    float theta, epsilon, intensity;
    for (int i = 0; i < u_NumSpotLights; i++) {
        vec3 lightDir = normalize(u_SpotLights[i].Position - v_FragPos);
        theta = dot(lightDir, normalize(-u_SpotLights[i].Direction));
        epsilon = u_SpotLights[i].CutOff - u_SpotLights[i].OuterCutOff;
        intensity = clamp((theta - u_SpotLights[i].OuterCutOff) / epsilon, 0.0, 1.0);

        // Diffuse
        float diff = max(dot(norm, lightDir), 0.0);
        vec3 diffuse = u_SpotLights[i].Diffuse * diff * vec3(texture(u_Material.AlbedoMap, coords)) * u_Material.Diffuse;

        // Specular
        vec3 reflectDir = reflect(-lightDir, norm);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), u_Material.Shininess);

        vec3 specular;
        if (u_Material.IsSpecularTexture == 1) {
            specular = u_SpotLights[i].Specular * spec * vec3(texture(u_Material.SpecularMap, coords));
        } else {
            specular = u_SpotLights[i].Specular * (spec * u_Material.Specular);
        }

        // Attenuation
        float distance = length(u_SpotLights[i].Position - v_FragPos);
        float attenuation = 1.0 / (
            u_SpotLights[i].ConstantFactor +
            u_SpotLights[i].LinearFactor * distance +
            u_SpotLights[i].QuadraticFactor * distance * distance
        );

        // Final combining
        result += (diffuse + specular) * u_SpotLights[i].Intensity * intensity * attenuation;
    }

    return result;
}
