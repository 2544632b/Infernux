@shader_id: lib/texture_utils

// ============================================================================
// lib/texture_utils.glsl — Texture sampling utilities
//
// Provides: normal blending, detail texture, texture bombing.
// Usage: @import: lib/texture_utils
// ============================================================================

// Blend two tangent-space normals (Reoriented Normal Mapping / RNM)
vec3 blendNormalsRNM(vec3 base, vec3 detail) {
    vec3 t = base + vec3(0.0, 0.0, 1.0);
    vec3 u = detail * vec3(-1.0, -1.0, 1.0);
    return normalize(t * dot(t, u) - u * t.z);
}

// Simple linear blend of tangent-space normals
vec3 blendNormalsLinear(vec3 base, vec3 detail) {
    return normalize(vec3(base.xy + detail.xy, base.z));
}

// Detail texture blending (overlay-style)
vec3 detailBlend(vec3 baseColor, vec3 detailColor, float strength) {
    vec3 result = mix(
        2.0 * baseColor * detailColor,
        1.0 - 2.0 * (1.0 - baseColor) * (1.0 - detailColor),
        step(0.5, baseColor));
    return mix(baseColor, result, strength);
}

// Heightmap-based texture blending (for terrain-like layering)
float heightBlend(float h1, float h2, float blend, float contrast) {
    float height1 = h1 + (1.0 - blend);
    float height2 = h2 + blend;
    float maxH = max(height1, height2) - contrast;
    float b1 = max(height1 - maxH, 0.0);
    float b2 = max(height2 - maxH, 0.0);
    return b2 / (b1 + b2 + 1e-6);
}

// Decode normal from normal map texture sample [0,1] -> [-1,1]
vec3 unpackNormal(vec4 normalSample) {
    return normalSample.rgb * 2.0 - 1.0;
}

// Decode normal with adjustable scale
vec3 unpackNormalScale(vec4 normalSample, float scale) {
    vec3 n = normalSample.rgb * 2.0 - 1.0;
    n.xy *= scale;
    return normalize(n);
}
