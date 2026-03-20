@shader_id: surface

// ============================================================================
// surface.glsl — SurfaceData struct for the surface() shading model
//
// Provides a standardized data structure that surface() shaders fill in.
// The engine then evaluates lighting via the referenced .shadingmodel file.
//
// Usage:
//   @shading_model: pbr    (or @shading_model: unlit)
//   void surface(out SurfaceData s) {
//       s = InitSurfaceData();
//       s.albedo = texture(texSampler, v_TexCoord).rgb;
//       // ... fill other fields ...
//   }
// ============================================================================

struct SurfaceData {
    vec3  albedo;              // Base color (linear RGB)
    vec3  normalWS;            // World-space normal (normalized)
    float metallic;            // Metallic factor [0, 1]
    float smoothness;          // Smoothness factor [0, 1] (1 - perceptualRoughness)
    float occlusion;           // Ambient occlusion [0, 1]
    vec3  emission;            // Emissive color (linear RGB, pre-multiplied by intensity)
    float alpha;               // Opacity [0, 1]
    float specularHighlights;  // Specular highlights multiplier [0, 1]
};

SurfaceData InitSurfaceData() {
    SurfaceData s;
    s.albedo = vec3(1.0);
    s.normalWS = vec3(0.0, 1.0, 0.0);
    s.metallic = 0.0;
    s.smoothness = 0.5;
    s.occlusion = 1.0;
    s.emission = vec3(0.0);
    s.alpha = 1.0;
    s.specularHighlights = 1.0;
    return s;
}
