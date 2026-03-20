@shader_id: lib/common

// ============================================================================
// lib/common.glsl — Common utility functions
//
// Frequently used helpers extracted for reuse across shaders.
// Usage: @import: lib/common
// ============================================================================

// Remap a value from one range to another
float remap(float value, float fromLow, float fromHigh, float toLow, float toHigh) {
    float t = (value - fromLow) / (fromHigh - fromLow);
    return mix(toLow, toHigh, t);
}

// Inverse lerp: compute t such that mix(a, b, t) == value
float inverseLerp(float a, float b, float value) {
    return (value - a) / (b - a);
}

// Smooth remap with clamping
float remapClamped(float value, float fromLow, float fromHigh, float toLow, float toHigh) {
    float t = clamp((value - fromLow) / (fromHigh - fromLow), 0.0, 1.0);
    return mix(toLow, toHigh, t);
}

// Square of a value (avoids ambiguous pow(x, 2))
float sq(float x) { return x * x; }
vec2  sq(vec2  x) { return x * x; }
vec3  sq(vec3  x) { return x * x; }

// Luminance (Rec. 709)
float luminance(vec3 color) {
    return dot(color, vec3(0.2126, 0.7152, 0.0722));
}

// Safe normalize — returns fallback when length is near zero
vec3 safeNormalize(vec3 v, vec3 fallback) {
    float len = length(v);
    return (len > 1e-6) ? v / len : fallback;
}
