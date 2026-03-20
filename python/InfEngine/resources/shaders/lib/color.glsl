@shader_id: lib/color

// ============================================================================
// lib/color.glsl — Color space conversions and adjustments
//
// Provides: sRGB/linear, HSV, brightness, contrast, saturation.
// Usage: @import: lib/color
// ============================================================================

// ---- sRGB <-> Linear ----

vec3 sRGBToLinear(vec3 srgb) {
    return mix(
        srgb / 12.92,
        pow((srgb + 0.055) / 1.055, vec3(2.4)),
        step(vec3(0.04045), srgb)
    );
}

vec3 linearToSRGB(vec3 linear) {
    return mix(
        linear * 12.92,
        1.055 * pow(linear, vec3(1.0 / 2.4)) - 0.055,
        step(vec3(0.0031308), linear)
    );
}

// ---- HSV <-> RGB ----

vec3 rgbToHSV(vec3 c) {
    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
    float d = q.x - min(q.w, q.y);
    float e = 1.0e-10;
    return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}

vec3 hsvToRGB(vec3 c) {
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

// ---- Adjustments ----

vec3 adjustBrightness(vec3 color, float amount) {
    return color + amount;
}

vec3 adjustContrast(vec3 color, float contrast) {
    return (color - 0.5) * contrast + 0.5;
}

vec3 adjustSaturation(vec3 color, float saturation) {
    float lum = dot(color, vec3(0.2126, 0.7152, 0.0722));
    return mix(vec3(lum), color, saturation);
}

// Hue shift (in radians)
vec3 hueShift(vec3 color, float shift) {
    vec3 hsv = rgbToHSV(color);
    hsv.x = fract(hsv.x + shift / 6.28318530718);
    return hsvToRGB(hsv);
}

// Tone mapping — simple Reinhard
vec3 reinhardTonemap(vec3 color) {
    return color / (1.0 + color);
}

// ACES approximation (Narkowicz 2015)
vec3 acesTonemap(vec3 x) {
    float a = 2.51;
    float b = 0.03;
    float c = 2.43;
    float d = 0.59;
    float e = 0.14;
    return clamp((x * (a * x + b)) / (x * (c * x + d) + e), 0.0, 1.0);
}
