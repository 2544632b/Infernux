@shader_id: lib/lighting_utils

// ============================================================================
// lib/lighting_utils.glsl — Lighting helper functions
//
// Standalone lighting utilities for surface shaders.
// For full PBR: use @import: pbr instead.
// Usage: @import: lib/lighting_utils
// ============================================================================

// ---- Fresnel ----

// Fresnel effect (Schlick approximation, single-channel)
// power: typically 5.0 for physical accuracy, or custom for artistic control
float fresnel(vec3 normal, vec3 viewDir, float power) {
    return pow(1.0 - max(dot(normal, viewDir), 0.0), power);
}

// Fresnel with F0 reflectance at normal incidence (vec3, for PBR metals)
vec3 fresnelSchlick(float cosTheta, vec3 F0) {
    return F0 + (1.0 - F0) * pow(clamp(1.0 - cosTheta, 0.0, 1.0), 5.0);
}

// Fresnel with roughness (for environment map reflections)
vec3 fresnelSchlickRoughness(float cosTheta, vec3 F0, float roughness) {
    return F0 + (max(vec3(1.0 - roughness), F0) - F0) *
           pow(clamp(1.0 - cosTheta, 0.0, 1.0), 5.0);
}

// ---- Diffuse models ----

// Half Lambert — wraps diffuse lighting to avoid harsh terminator
// Commonly used in toon/stylized shading
float halfLambert(vec3 normal, vec3 lightDir) {
    return dot(normal, lightDir) * 0.5 + 0.5;
}

// Quantized diffuse for cel/toon shading
// bands: number of discrete shading bands (e.g. 3)
float toonDiffuse(vec3 normal, vec3 lightDir, float bands) {
    float NdotL = dot(normal, lightDir) * 0.5 + 0.5;
    return floor(NdotL * bands) / bands;
}

// ---- Rim / Edge lighting ----

// Rim light — glowing edge effect based on view angle
// power: sharpness of the rim (higher = thinner)
// strength: intensity multiplier
float rimLight(vec3 normal, vec3 viewDir, float power, float strength) {
    float rim = 1.0 - max(dot(normal, viewDir), 0.0);
    return pow(rim, power) * strength;
}

// ---- Specular helpers ----

// Blinn-Phong specular highlight (simple, non-PBR)
float blinnPhongSpecular(vec3 normal, vec3 lightDir, vec3 viewDir, float shininess) {
    vec3 halfDir = normalize(lightDir + viewDir);
    return pow(max(dot(normal, halfDir), 0.0), shininess);
}
