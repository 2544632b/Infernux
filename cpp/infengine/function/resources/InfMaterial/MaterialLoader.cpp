#include "MaterialLoader.h"

#include <core/log/InfLog.h>
#include <function/resources/AssetDatabase/AssetDatabase.h>
#include <function/resources/AssetDependencyGraph.h>
#include <function/resources/InfMaterial/InfMaterial.h>

#include <platform/filesystem/InfPath.h>

#include <filesystem>
#include <fstream>

namespace infengine
{

// =============================================================================
// Load — create a brand-new InfMaterial from a .mat file
// =============================================================================

std::shared_ptr<void> MaterialLoader::Load(const std::string &filePath, const std::string &guid, AssetDatabase *adb)
{
    if (filePath.empty() || guid.empty()) {
        INFLOG_WARN("MaterialLoader::Load: empty filePath or guid");
        return nullptr;
    }

    // Read file
    std::ifstream file(ToFsPath(filePath));
    if (!file.is_open()) {
        INFLOG_WARN("MaterialLoader::Load: cannot open '", filePath, "'");
        return nullptr;
    }
    std::string jsonStr((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    file.close();

    // Deserialize
    auto material = std::make_shared<InfMaterial>();
    if (!material->Deserialize(jsonStr)) {
        INFLOG_ERROR("MaterialLoader::Load: deserialization failed for '", filePath, "'");
        return nullptr;
    }

    // Identity — authoritative source is .meta / AssetDatabase, NOT JSON
    material->SetFilePath(filePath);
    material->SetName(FromFsPath(ToFsPath(filePath).stem()));
    material->SetGuid(guid);

    // Dependency graph edges (textures, shaders)
    RegisterDependencies(guid, *material, adb);

    INFLOG_INFO("MaterialLoader: loaded '", material->GetName(), "' (GUID: ", guid, ")");
    return material;
}

// =============================================================================
// Reload — hot-refresh into an existing instance (pointer identity preserved)
// =============================================================================

bool MaterialLoader::Reload(std::shared_ptr<void> existing, const std::string &filePath, const std::string &guid,
                            AssetDatabase *adb)
{
    auto mat = std::static_pointer_cast<InfMaterial>(existing);
    if (!mat) {
        INFLOG_WARN("MaterialLoader::Reload: null existing instance");
        return false;
    }

    // Read file
    std::ifstream file(ToFsPath(filePath));
    if (!file.is_open()) {
        INFLOG_WARN("MaterialLoader::Reload: cannot open '", filePath, "'");
        return false;
    }
    std::string jsonStr((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    file.close();

    // Save authoritative name and GUID (Deserialize may clobber m_name)
    const std::string savedName = mat->GetName();
    const std::string savedGuid = mat->GetGuid();

    // Deserialize *into the same instance* — shared_ptr identity preserved
    if (!mat->Deserialize(jsonStr)) {
        INFLOG_ERROR("MaterialLoader::Reload: deserialization failed for '", filePath, "'");
        return false;
    }

    // Restore authoritative identity
    mat->SetName(savedName);
    mat->SetGuid(savedGuid);

    // Re-wire dependency graph (texture/shader deps may have changed)
    RegisterDependencies(savedGuid, *mat, adb);

    // INFLOG_INFO("MaterialLoader: reloaded '", savedName, "' in-place");
    return true;
}

// =============================================================================
// ScanDependencies — enumerate outgoing GUIDs for the dependency graph
// =============================================================================

std::set<std::string> MaterialLoader::ScanDependencies(const std::string &filePath, AssetDatabase *adb)
{
    std::set<std::string> deps;

    std::ifstream file(filePath);
    if (!file.is_open())
        return deps;

    std::string jsonStr((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    file.close();

    // Temporary material just for parsing — lightweight, no GPU resources
    InfMaterial tmp;
    if (!tmp.Deserialize(jsonStr))
        return deps;

    // Texture GUIDs
    for (const auto &[propName, prop] : tmp.GetAllProperties()) {
        if (prop.type != MaterialPropertyType::Texture2D)
            continue;
        const auto *val = std::get_if<std::string>(&prop.value);
        if (val && !val->empty())
            deps.insert(*val);
    }

    // Shader GUIDs (resolved via AssetDatabase)
    if (adb) {
        auto addShaderDep = [&](const std::string &shaderPath) {
            if (shaderPath.empty())
                return;
            std::string depGuid = adb->GetGuidFromPath(shaderPath);
            if (!depGuid.empty())
                deps.insert(depGuid);
        };
        addShaderDep(tmp.GetVertShaderName());
        addShaderDep(tmp.GetFragShaderName());
    }

    return deps;
}

// =============================================================================
// RegisterDependencies — wire up AssetDependencyGraph edges
// =============================================================================

void MaterialLoader::RegisterDependencies(const std::string &materialGuid, const InfMaterial &mat, AssetDatabase *adb)
{
    if (materialGuid.empty())
        return;

    auto &graph = AssetDependencyGraph::Instance();

    // Clear stale edges before re-registering
    graph.ClearDependenciesOf(materialGuid);

    // Texture property GUIDs
    for (const auto &[propName, prop] : mat.GetAllProperties()) {
        if (prop.type != MaterialPropertyType::Texture2D)
            continue;
        const auto *val = std::get_if<std::string>(&prop.value);
        if (val && !val->empty())
            graph.AddDependency(materialGuid, *val);
    }

    // Shader GUIDs (shader files have .meta with GUID)
    if (adb) {
        auto addShaderDep = [&](const std::string &shaderPath) {
            if (shaderPath.empty())
                return;
            std::string depGuid = adb->GetGuidFromPath(shaderPath);
            if (!depGuid.empty())
                graph.AddDependency(materialGuid, depGuid);
        };
        addShaderDep(mat.GetVertShaderName());
        addShaderDep(mat.GetFragShaderName());
    }
}

} // namespace infengine
