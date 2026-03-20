#pragma once

namespace infengine
{

// ============================================================================
// ShaderCompileTarget — identifies which rendering pass variant to compile for.
//
// Shared between InfShaderLoader (compile-time variant generation) and
// InfMaterial (per-pass pipeline storage).  Defined in a lightweight header
// to avoid pulling in heavy shader-compiler includes through InfMaterial.h.
// ============================================================================

enum class ShaderCompileTarget : int
{
    Forward = 0, // Standard forward rendering (default)
    GBuffer = 1, // Deferred GBuffer output
    Shadow = 2,  // Depth-only shadow caster

    Count // Sentinel — number of targets; must be last
};

} // namespace infengine
