@shader_id: lib/surface_utils

@import: lib/normal_utils
@import: lib/camera
@import: lib/common

// ============================================================================
// lib/surface_utils.glsl — Surface shader utility functions
//
// Auto-imported for all surface() shaders. Provides pre-built helpers
// for common surface() operations: normal mapping, material sampling,
// coordinate access, view/depth helpers, and more.
//
// Available varyings (from fragment_varyings.glsl):
//   v_WorldPos   — world-space fragment position
//   v_Normal     — interpolated world-space normal
//   v_Tangent    — world-space tangent (w = bitangent sign)
//   v_Color      — vertex color
//   v_TexCoord   — primary UV coordinates
//   v_ViewDepth  — linear eye-space depth
//
// Available uniforms (auto-injected by engine):
//   material.<name>  — MaterialProperties UBO from @property declarations
//   _Globals.*       — Engine globals (time, screen, camera, etc.)
// ============================================================================

// ============================================================================
// Fragment Inputs — Quick access to interpolated vertex data
// ============================================================================

// World-space fragment position
vec3 getWorldPosition() {
    return v_WorldPos;
}

// Interpolated world-space normal (normalized)
vec3 getWorldNormal() {
    return normalize(v_Normal);
}

// Interpolated world-space tangent (not normalized — use for TBN construction)
vec4 getWorldTangent() {
    return v_Tangent;
}

// Vertex color (linear)
vec3 getVertexColor() {
    return v_Color;
}

// Vertex alpha (from vertex color .a via v_Color)
// Note: v_Color is vec3 — alpha is in vertex attribute but not interpolated.
// Use v_TexCoord or material alpha instead.

// Primary UV coordinates
vec2 getUV() {
    return v_TexCoord;
}

// Linear eye-space depth of this fragment
float getViewDepth() {
    return v_ViewDepth;
}

// ============================================================================
// View & Camera — Direction, distance, Fresnel
// ============================================================================

// Normalized view direction (from fragment toward camera)
vec3 getViewDir() {
    return getViewDirection(v_WorldPos);
}

// Distance from camera to fragment
float getCameraDistance() {
    return length(getCameraPosition() - v_WorldPos);
}

// Basic Fresnel using surface normal (Schlick approximation with F0 = 0.04)
float getFresnel() {
    vec3 N = getWorldNormal();
    vec3 V = getViewDir();
    float NdotV = max(dot(N, V), 0.0);
    return 0.04 + 0.96 * pow(1.0 - NdotV, 5.0);
}

// Fresnel with custom F0 (reflectance at normal incidence)
float getFresnelF0(float f0) {
    vec3 N = getWorldNormal();
    vec3 V = getViewDir();
    float NdotV = max(dot(N, V), 0.0);
    return f0 + (1.0 - f0) * pow(1.0 - NdotV, 5.0);
}

// ============================================================================
// Normal Mapping — Simplified one-call interface
// ============================================================================

// Sample a normal map and return world-space normal.
// Uses the fragment's interpolated normal & tangent automatically.
//   normalMap : tangent-space normal map sampler
//   uv        : texture coordinates (use getUV() for primary)
//   scale     : normal map strength (1.0 = normal, 0.0 = flat)
vec3 sampleNormal(sampler2D normalMap, vec2 uv, float scale) {
    return getNormalFromMap(normalMap, uv, scale, v_Normal, v_Tangent);
}

// Overload: uses primary UV
vec3 sampleNormal(sampler2D normalMap, float scale) {
    return getNormalFromMap(normalMap, v_TexCoord, scale, v_Normal, v_Tangent);
}

// Sample a height map and return world-space normal (bump mapping).
//   heightMap  : grayscale height texture
//   uv         : texture coordinates
//   strength   : bump strength
//   texelSize  : 1.0 / textureSize (e.g. vec2(1.0/1024.0))
vec3 sampleNormalFromHeight(sampler2D heightMap, vec2 uv, float strength, vec2 texelSize) {
    return normalFromHeightWS(heightMap, uv, strength, texelSize, v_Normal, v_Tangent);
}

// ============================================================================
// Texture Sampling — Convenience wrappers
// ============================================================================

// Sample an albedo/color texture at primary UV, returns linear RGB
vec3 sampleAlbedo(sampler2D tex) {
    return texture(tex, v_TexCoord).rgb;
}

// Sample an albedo/color texture at primary UV, returns RGBA
vec4 sampleAlbedoAlpha(sampler2D tex) {
    return texture(tex, v_TexCoord);
}

// Sample a single-channel map (metallic, smoothness, AO, height, etc.)
float sampleGrayscale(sampler2D tex) {
    return texture(tex, v_TexCoord).r;
}

// Sample a single-channel map at custom UV
float sampleGrayscale(sampler2D tex, vec2 uv) {
    return texture(tex, uv).r;
}

// Sample emission map at primary UV (expects linear HDR)
vec3 sampleEmission(sampler2D tex) {
    return texture(tex, v_TexCoord).rgb;
}

// ============================================================================
// Depth — Utilities that work with the fragment's own depth
// ============================================================================

// Normalized depth [0, 1] (0 = near plane, 1 = far plane)
float getLinear01Depth() {
    return v_ViewDepth / getCameraFar();
}

// ============================================================================
// Object Space — Fragment position relative to object
// ============================================================================

// Approximate object-space position using world position and camera data.
// Note: For exact object-space coordinates, pass them via a custom varying
// in a vertex() hook. This approximation uses the fragment world position.
// For procedural textures, consider using v_WorldPos directly.
