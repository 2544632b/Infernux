// ============================================================================
// default_gbuffer_evaluate.glsl — Engine default GBuffer packing
//
// Used automatically when a .shadingmodel file does not provide a custom
// @target: gbuffer block.  Packs standard SurfaceData fields into G-Buffer
// outputs suitable for a deferred lighting pass.
//
// G-Buffer layout:
//   gbuf0.rgb  = albedo,    gbuf0.a = alpha
//   gbuf1.rgb  = normal,    gbuf1.a = smoothness
//   gbuf2.r    = metallic,  gbuf2.g = occlusion, gbuf2.b = specularHighlights, gbuf2.a = 1.0
//   gbuf3.rgb  = emission,  gbuf3.a = 1.0
// ============================================================================

void evaluate(in SurfaceData s, out vec4 gbuf0, out vec4 gbuf1,
              out vec4 gbuf2, out vec4 gbuf3) {
    gbuf0 = vec4(clamp(s.albedo, 0.0, 1.0), s.alpha);
    gbuf1 = vec4(normalize(s.normalWS) * 0.5 + 0.5, s.smoothness);
    gbuf2 = vec4(clamp(s.metallic, 0.0, 1.0), s.occlusion, s.specularHighlights, 1.0);
    gbuf3 = vec4(s.emission, 1.0);
}
