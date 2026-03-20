@shader_id: lib/utils

@import: lib/common
@import: lib/color
@import: lib/noise
@import: lib/shapes
@import: lib/uv
@import: lib/texture_utils
@import: lib/lighting_utils
@import: lib/vertex_utils

// ============================================================================
// lib/utils.glsl — General-purpose shader utility toolkit
//
// Aggregates all context-free utility libraries into a single import.
// No UBO or varying dependencies — works in ANY shader type
// (surface, fullscreen, post-processing, compute, etc.)
//
// Usage: @import: lib/utils
//
// Includes:
//   lib/common          — remap, inverseLerp, luminance, sq, safeNormalize
//   lib/color           — sRGB, HSV, brightness, contrast, saturation, tonemap
//   lib/noise           — hash, value/gradient/simplex noise, fbm, voronoi
//   lib/shapes          — SDF: circle, rect, ring, polygon, star, grid, checker
//   lib/uv              — tiling, rotation, flipbook, parallax, triplanar, polar
//   lib/texture_utils   — normal blending, detail blend, height blend, unpack
//   lib/lighting_utils  — fresnel, half-lambert, toon diffuse, rim, blinn-phong
//   lib/vertex_utils    — billboard, wind sway, displacement, pulse
//
// For individual imports, use the specific library (e.g. @import: lib/noise).
// ============================================================================

// ---- Math constants (consolidated from math.glsl) ----
const float PI       = 3.14159265359;
const float INV_PI   = 0.31830988618;
const float HALF_PI  = 1.57079632679;
const float TWO_PI   = 6.28318530718;
const float EPSILON  = 0.0001;
const float FLT_MIN  = 1.175494e-38;

float saturate(float x) {
    return clamp(x, 0.0, 1.0);
}

vec3 saturateVec3(vec3 x) {
    return clamp(x, vec3(0.0), vec3(1.0));
}
