#type vertex
#version 450 core

struct Camera {
    vec3 Position;
    mat4 ViewProjection;
};

struct Transform {
    mat4 Transform;
};

layout(location=0) in vec2 a_TexCoord;
layout(location=1) in vec3 a_Normal;
layout(location=2) in vec3 a_Position;

out VS_OUT {
    vec3 Normal;
    vec3 FragPos;
    vec3 CameraPos;
    vec2 TexCoord;
} vs_out;

uniform Camera u_Camera;
uniform Transform u_Transform;

void main() {
    vs_out.Normal  = mat3(transpose(inverse(u_Transform.Transform))) * a_Normal;
    vs_out.FragPos = vec3(u_Transform.Transform * vec4(a_Position, 1.0));
    vs_out.CameraPos = u_Camera.Position;
    vs_out.TexCoord = a_TexCoord;

    gl_Position = u_Camera.ViewProjection * u_Transform.Transform * vec4(a_Position, 1.0);
}

#type fragment
#version 450 core

struct Material {
    // Albedo
    int IsAlbedoMap;
    sampler2D AlbedoMap;
    vec3 Diffuse;

    // Specular
    int IsSpecularMap;
    sampler2D SpecularMap;
    vec3 Specular;

    // Shininess
    float Shininess;
    float TilingFactor;
};

struct DirectionalLight {
    // All Lights have these properties
    vec3 Position;

    vec3 Ambient;
    vec3 Diffuse;
    vec3 Specular;

    float Intensity;

    // Directional Light specific properties
    vec3 Direction;
};

struct PointLight {
    // All Lights have these properties
    vec3 Position;

    vec3 Ambient;
    vec3 Diffuse;
    vec3 Specular;

    float Intensity;

    // Point Light specific properties
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

#define MAX_POINT_LIGHTS 64
#define MAX_SPOT_LIGHTS  64

in VS_OUT {
    vec3 Normal;
    vec3 FragPos;
    vec3 CameraPos;
    vec2 TexCoord;
} fs_in;

layout(location=0) out vec4 color;

uniform Material u_Material;

// Lights
uniform DirectionalLight u_DirectionalLight;
uniform PointLight       u_PointLights [ MAX_POINT_LIGHTS ];
uniform SpotLight        u_SpotLights  [ MAX_SPOT_LIGHTS  ];

uniform int u_NumPointLights;      // This is just to save time not looping over all lights
uniform int u_NumSpotLights;       // This is just to save time not looping over all lights

vec3 CalculateDirectionalLight (vec3, vec3, vec2);
vec3 CalculatePointLight       (vec3, vec3, vec2);
vec3 CalculateSpotLight        (vec3, vec3, vec2);

void main() {
    // These values are common to all lights
    // so they are precomputed.
    vec3 norm = normalize(fs_in.Normal);
    vec3 viewDir = normalize(fs_in.CameraPos - fs_in.FragPos);

    // Combining all the lights
    vec3 result = vec3(0.0, 0.0, 0.0);
    vec2 coords = fs_in.TexCoord * u_Material.TilingFactor;

    /*
    result += CalculateDirectionalLight (norm, viewDir, coords);
    result += CalculatePointLight       (norm, viewDir, coords);
    result += CalculateSpotLight        (norm, viewDir, coords);
    */

    // Ambient is just calculated for the directional Light
    // So all lights will not add their respective ambients
    // making the scene look bright
    vec3 ambient = u_DirectionalLight.Ambient * u_Material.Diffuse;
    result += ambient;

    // color = vec4(result, 1.0);
    color = vec4(1.0, 1.0, 1.0, 1.0);
}

/*
vec3 CalculateDirectionalLight(vec3 norm, vec3 viewDir, vec2 coords) {
    // Diffuse
    vec3 lightDir = normalize(-u_DirectionalLight.Direction);
    float diff = max(dot(norm, lightDir), 0.0);

    vec3 diffuse;
    if (u_Material.IsAlbedoMap == 1) {
        diffuse = u_DirectionalLight.Diffuse * diff * vec3(texture(u_Material.AlbedoMap, coords));
    } else {
        diffuse = u_DirectionalLight.Diffuse * (diff * u_Material.Diffuse);
    }

    // Specular
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), u_Material.Shininess);
    
    vec3 specular;
    if (u_Material.IsSpecularMap == 1) {
        specular = u_DirectionalLight.Specular * spec * vec3(texture(u_Material.SpecularMap, coords));
    } else {
        specular = u_DirectionalLight.Specular * (spec * u_Material.Specular);
    }

    // Final combining
    return (diffuse + specular) * u_DirectionalLight.Intensity;
}

vec3 CalculatePointLight(vec3 norm, vec3 viewDir, vec2 coords) {
    vec3 result = vec3(0.0, 0.0, 0.0);

    for (int i = 0; i < u_NumPointLights; i++) {
        // Diffuse
        vec3 lightDir = normalize(u_PointLights[i].Position - fs_in.FragPos);
        float diff = max(dot(norm, lightDir), 0.0);

        vec3 diffuse;
        if (u_Material.IsAlbedoMap == 1) {
            diffuse = u_PointLights[i].Diffuse * diff * vec3(texture(u_Material.AlbedoMap, coords));
        } else {
            diffuse = u_PointLights[i].Diffuse * (diff * u_Material.Diffuse);
        }

        // Specular
        vec3 reflectDir = reflect(-lightDir, norm);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), u_Material.Shininess);

        vec3 specular;
        if (u_Material.IsSpecularMap == 1) {
            specular = u_PointLights[i].Specular * diff * vec3(texture(u_Material.SpecularMap, coords));
        } else {
            specular = u_PointLights[i].Specular * (diff * u_Material.Specular);
        }

        // Attenuation
        float distance = length(u_PointLights[i].Position - fs_in.FragPos);
        
        // Attenuation = 1.0 / (ax^2 + bx + c)
        float attenuation = 1.0 / (
            u_PointLights[i].QuadraticFactor * distance * distance +
            u_PointLights[i].LinearFactor    * distance +
            u_PointLights[i].ConstantFactor
        );

        // Final combining
        result += (diffuse + specular) * u_PointLights[i].Intensity * attenuation;
    }

    return result;
}

vec3 CalculateSpotLight(vec3 norm, vec3 viewDir, vec2 coords) {
    vec3 result = vec3(0.0, 0.0, 0.0);

    float theta, epsilon, intensity;
    for (int i = 0; i < u_NumSpotLights; i++) {
        vec3 lightDir = normalize(u_SpotLights[i].Position - fs_in.FragPos);
        theta = dot(lightDir, normalize(-u_SpotLights[i].Direction));
        epsilon = u_SpotLights[i].CutOff - u_SpotLights[i].OuterCutOff;
        intensity = clamp((theta - u_SpotLights[i].OuterCutOff) / epsilon, 0.0, 1.0);

        // Diffuse
        float diff = max(dot(norm, lightDir), 0.0);
        vec3 diffuse;
        if (u_Material.IsAlbedoMap == 1) {
            diffuse = u_SpotLights[i].Diffuse * diff * vec3(texture(u_Material.AlbedoMap, coords));
        } else {
            diffuse = u_SpotLights[i].Diffuse * (diff * u_Material.Diffuse);
        }

        // Specular
        vec3 reflectDir = reflect(-lightDir, norm);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), u_Material.Shininess);

        vec3 specular;
        if (u_Material.IsAlbedoMap == 1) {
            specular = u_SpotLights[i].Specular * diff * vec3(texture(u_Material.SpecularMap, coords));
        } else {
            specular = u_SpotLights[i].Specular * (diff * u_Material.Specular);
        }

        // Attenuation
        float distance = length(u_SpotLights[i].Position - fs_in.FragPos);
        float attenuation = 1.0 / (
            u_SpotLights[i].QuadraticFactor * distance * distance +
            u_SpotLights[i].LinearFactor    * distance +
            u_SpotLights[i].ConstantFactor
        );

        // Final combining
        result += (diffuse + specular) * u_SpotLights[i].Intensity * intensity * attenuation;
    }

    return result;
}
*/
