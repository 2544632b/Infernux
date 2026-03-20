@shader_id: lib/noise

// ============================================================================
// lib/noise.glsl — Procedural noise functions
//
// Provides: hash, value noise, Perlin gradient noise, simplex noise, FBM.
// Usage: @import: lib/noise
// ============================================================================

// ---- Hash functions ----

float hash11(float p) {
    p = fract(p * 0.1031);
    p *= p + 33.33;
    p *= p + p;
    return fract(p);
}

float hash21(vec2 p) {
    vec3 p3 = fract(vec3(p.xyx) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.x + p3.y) * p3.z);
}

vec2 hash22(vec2 p) {
    vec3 p3 = fract(vec3(p.xyx) * vec3(0.1031, 0.1030, 0.0973));
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.xx + p3.yz) * p3.zy);
}

vec3 hash33(vec3 p3) {
    p3 = fract(p3 * vec3(0.1031, 0.1030, 0.0973));
    p3 += dot(p3, p3.yxz + 33.33);
    return fract((p3.xxy + p3.yxx) * p3.zyx);
}

// ---- Value noise ----

float valueNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f); // Hermite smoothstep

    float a = hash21(i);
    float b = hash21(i + vec2(1.0, 0.0));
    float c = hash21(i + vec2(0.0, 1.0));
    float d = hash21(i + vec2(1.0, 1.0));

    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

// ---- Perlin gradient noise (2D) ----

vec2 gradientDir(vec2 p) {
    p = mod(p, 289.0);
    float x = mod((34.0 * p.x + 1.0) * p.x, 289.0);
    x = mod((34.0 * (x + p.y) + 1.0) * (x + p.y), 289.0);
    x = fract(x / 41.0) * 2.0 - 1.0;
    return normalize(vec2(x, abs(x) - 0.5));
}

float gradientNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * f * (f * (f * 6.0 - 15.0) + 10.0); // Quintic Hermite

    return mix(
        mix(dot(gradientDir(i + vec2(0.0, 0.0)), f - vec2(0.0, 0.0)),
            dot(gradientDir(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0)), u.x),
        mix(dot(gradientDir(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0)),
            dot(gradientDir(i + vec2(1.0, 1.0)), f - vec2(1.0, 1.0)), u.x),
        u.y);
}

// ---- Simplex noise (2D) ----

float simplexNoise(vec2 p) {
    const float K1 = 0.366025404; // (sqrt(3) - 1) / 2
    const float K2 = 0.211324865; // (3 - sqrt(3)) / 6

    vec2 i = floor(p + (p.x + p.y) * K1);
    vec2 a = p - i + (i.x + i.y) * K2;
    float m = step(a.y, a.x);
    vec2 o = vec2(m, 1.0 - m);
    vec2 b = a - o + K2;
    vec2 c = a - 1.0 + 2.0 * K2;

    vec3 h = max(0.5 - vec3(dot(a, a), dot(b, b), dot(c, c)), 0.0);
    vec3 n = h * h * h * h * vec3(
        dot(a, hash22(i) * 2.0 - 1.0),
        dot(b, hash22(i + o) * 2.0 - 1.0),
        dot(c, hash22(i + 1.0) * 2.0 - 1.0));

    return dot(n, vec3(70.0));
}

// ---- Fractional Brownian Motion ----

float fbm(vec2 p, int octaves) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;
    for (int i = 0; i < octaves; ++i) {
        value += amplitude * gradientNoise(p * frequency);
        frequency *= 2.0;
        amplitude *= 0.5;
    }
    return value;
}

// ---- Voronoi / Worley noise ----

float voronoiNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    float minDist = 1.0;
    for (int y = -1; y <= 1; ++y) {
        for (int x = -1; x <= 1; ++x) {
            vec2 neighbor = vec2(float(x), float(y));
            vec2 point = hash22(i + neighbor);
            vec2 diff = neighbor + point - f;
            minDist = min(minDist, length(diff));
        }
    }
    return minDist;
}
