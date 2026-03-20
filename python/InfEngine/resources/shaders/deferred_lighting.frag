#version 450
@shader_id: deferred_lighting
@hidden

// Deferred lighting pass.
// The current built-in deferred path stores the lit scene color in slot 0
// and auxiliary material data in the remaining GBuffer targets. This pass
// therefore reconstructs the final color by passing through slot 0 and
// re-adding emission, while keeping the other inputs available for future
// true deferred relighting.
//
// Binding layout (matches GBuffer MRT + depth + shadow map):
//   binding 0 — gAlbedo     (RGBA8_UNORM: lit scene color)
//   binding 1 — gNormal     (RGBA16_SFLOAT: encoded world normal.xyz)
//   binding 2 — gMaterial   (RGBA8_UNORM: metallic, smoothness, specularHighlights, alpha)
//   binding 3 — gEmission   (RGBA16_SFLOAT: emission.rgb)
//   binding 4 — sceneDepth  (D32_SFLOAT)
//   binding 5 — shadowMap   (D32_SFLOAT)

layout(set = 0, binding = 0) uniform sampler2D _GAlbedo;
layout(set = 0, binding = 1) uniform sampler2D _GNormal;
layout(set = 0, binding = 2) uniform sampler2D _GMaterial;
layout(set = 0, binding = 3) uniform sampler2D _GEmission;
layout(set = 0, binding = 4) uniform sampler2D _SceneDepth;
layout(set = 0, binding = 5) uniform sampler2D _ShadowMap;

layout(location = 0) in  vec2 inUV;
layout(location = 0) out vec4 outColor;

void main() {
    vec4 litColor = texture(_GAlbedo, inUV);
    vec4 material = texture(_GMaterial, inUV);
    vec3 emission = texture(_GEmission, inUV).rgb;

    outColor = vec4(litColor.rgb + emission, material.a > 0.0 ? material.a : litColor.a);
}
