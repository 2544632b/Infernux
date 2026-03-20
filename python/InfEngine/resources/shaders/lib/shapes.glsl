@shader_id: lib/shapes

// ============================================================================
// lib/shapes.glsl — Procedural shape functions (SDF-based)
//
// Provides: checkerboard, circle, rounded rectangle, ring, polygon, grid lines.
// All functions operate on 2D UV coordinates.
// Usage: @import: lib/shapes
// ============================================================================

// ---- Pattern generators ----

// Checkerboard pattern
// Returns 0.0 or 1.0 in alternating cells
float checkerboard(vec2 uv, float scale) {
    vec2 c = floor(uv * scale);
    return mod(c.x + c.y, 2.0);
}

// Grid lines pattern
// lineWidth: thickness of lines in UV space (e.g. 0.02)
// Returns 1.0 on lines, 0.0 elsewhere
float gridLines(vec2 uv, float scale, float lineWidth) {
    vec2 grid = abs(fract(uv * scale - 0.5) - 0.5);
    vec2 line = smoothstep(vec2(0.0), vec2(lineWidth), grid);
    return 1.0 - min(line.x, line.y);
}

// ---- Signed Distance Fields ----

// Circle SDF — smooth anti-aliased circle
// Returns 1.0 inside, 0.0 outside, smooth transition at edge
float circleSDF(vec2 uv, vec2 center, float radius) {
    float dist = length(uv - center);
    return 1.0 - smoothstep(radius - fwidth(dist), radius + fwidth(dist), dist);
}

// Rounded rectangle SDF
// halfSize: half-extents of the rectangle (before rounding)
// radius: corner rounding radius
float roundedRectSDF(vec2 uv, vec2 center, vec2 halfSize, float radius) {
    vec2 d = abs(uv - center) - halfSize + radius;
    float dist = length(max(d, 0.0)) - radius;
    return 1.0 - smoothstep(-fwidth(dist), fwidth(dist), dist);
}

// Box SDF (sharp corners)
float boxSDF(vec2 uv, vec2 center, vec2 halfSize) {
    vec2 d = abs(uv - center) - halfSize;
    float dist = length(max(d, 0.0)) + min(max(d.x, d.y), 0.0);
    return 1.0 - smoothstep(-fwidth(dist), fwidth(dist), dist);
}

// Ring shape — annular region between inner and outer radius
float ringShape(vec2 uv, vec2 center, float innerRadius, float outerRadius) {
    float dist = length(uv - center);
    float outer = 1.0 - smoothstep(outerRadius - fwidth(dist), outerRadius + fwidth(dist), dist);
    float inner = 1.0 - smoothstep(innerRadius - fwidth(dist), innerRadius + fwidth(dist), dist);
    return outer - inner;
}

// ---- Polygon SDF ----

// Regular polygon (N-sided) SDF
// sides: number of sides (3 = triangle, 4 = diamond, 6 = hexagon, etc.)
float polygonSDF(vec2 uv, vec2 center, float radius, float sides) {
    vec2 p = uv - center;
    float angle = atan(p.y, p.x);
    float slice = 6.28318530718 / sides;
    float dist = cos(floor(0.5 + angle / slice) * slice - angle) * length(p);
    return 1.0 - smoothstep(radius - fwidth(dist), radius + fwidth(dist), dist);
}

// ---- Utility ----

// Star shape (N-pointed)
// innerRadius: radius of inner vertices
// outerRadius: radius of outer vertices
// points: number of star points
float starSDF(vec2 uv, vec2 center, float innerRadius, float outerRadius, float points) {
    vec2 p = uv - center;
    float angle = atan(p.y, p.x);
    float slice = 6.28318530718 / points;
    float halfSlice = slice * 0.5;
    float a = mod(angle, slice) - halfSlice;
    float r = mix(innerRadius, outerRadius, step(0.0, cos(a * points)));
    float dist = length(p);
    return 1.0 - smoothstep(r - fwidth(dist), r + fwidth(dist), dist);
}
