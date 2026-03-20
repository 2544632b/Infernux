@shader_id: lib/depth

// ============================================================================
// lib/depth.glsl — Depth buffer utilities
//
// Requires: InfGlobals UBO (auto-injected by engine at set 2, binding 0)
// Usage: @import: lib/depth
// ============================================================================

// ---- Depth fade (soft particles / intersection) ----

// Soft blending based on depth difference between fragment and scene
// sceneDepthLinear: linearized scene depth (from linearEyeDepth)
// fragmentDepth: current fragment view-space depth (e.g. v_ViewDepth)
// fadeDistance: distance over which to blend (world units)
// Returns 0.0 when fragment is AT the scene surface, 1.0 when fully separated
float depthFade(float sceneDepthLinear, float fragmentDepth, float fadeDistance) {
    return clamp((sceneDepthLinear - fragmentDepth) / fadeDistance, 0.0, 1.0);
}

// ---- World position reconstruction ----

// Reconstruct world-space position from depth buffer
// rawDepth: depth buffer sample [0,1]
// screenUV: normalized screen coordinates [0,1]
// invViewProj: inverse view-projection matrix
vec3 reconstructWorldPos(float rawDepth, vec2 screenUV, mat4 invViewProj) {
    // Convert screen UV to clip space [-1,1]
    vec4 clipPos = vec4(screenUV * 2.0 - 1.0, rawDepth, 1.0);
    vec4 worldPos = invViewProj * clipPos;
    return worldPos.xyz / worldPos.w;
}

// ---- Fog helpers ----

// Linear fog factor based on view distance
// viewDepth: view-space depth of fragment (e.g. v_ViewDepth)
// fogStart: distance where fog begins
// fogEnd: distance where fog is fully opaque
// Returns 0.0 = no fog, 1.0 = full fog
float linearFog(float viewDepth, float fogStart, float fogEnd) {
    return clamp((viewDepth - fogStart) / (fogEnd - fogStart), 0.0, 1.0);
}

// Exponential fog factor
// viewDepth: view-space depth of fragment
// density: fog density coefficient
float exponentialFog(float viewDepth, float density) {
    return 1.0 - exp(-density * viewDepth);
}

// Exponential squared fog factor (denser falloff)
float exponentialSquaredFog(float viewDepth, float density) {
    float f = density * viewDepth;
    return 1.0 - exp(-f * f);
}
