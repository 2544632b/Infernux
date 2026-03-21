#pragma once

#include <function/resources/AssetRegistry/IAssetLoader.h>
#include <function/resources/InfResource/InfResourceMeta.h>
#include <set>
#include <string>
#include <vector>

namespace infengine
{

/**
 * @brief Loader for Python script files (.py).
 *
 * This loader:
 * - Generates stable GUID for script assets
 * - Parses import statements to detect dependencies
 * - Extracts class names (especially InfComponent subclasses)
 * - Creates meta files for script tracking
 *
 * Note: Python scripts are not "loaded" into C++ memory, they are
 * dynamically imported by Python runtime. This loader only handles
 * metadata generation for the asset database.
 */
class InfPythonScriptLoader : public IAssetLoader
{
  public:
    InfPythonScriptLoader();

    // -- IAssetLoader meta interface --
    bool LoadMeta(const char *content, const std::string &filePath, InfResourceMeta &metaData) override;
    void CreateMeta(const char *content, size_t contentSize, const std::string &filePath,
                    InfResourceMeta &metaData) override;

    // -- IAssetLoader runtime interface (no-op for scripts) --
    std::shared_ptr<void> Load(const std::string & /*filePath*/, const std::string & /*guid*/,
                               AssetDatabase * /*adb*/) override
    {
        return nullptr;
    }
    bool Reload(std::shared_ptr<void> /*existing*/, const std::string & /*filePath*/, const std::string & /*guid*/,
                AssetDatabase * /*adb*/) override
    {
        return false;
    }
    std::set<std::string> ScanDependencies(const std::string & /*filePath*/, AssetDatabase * /*adb*/) override
    {
        return {};
    }

  private:
    /// @brief Parse Python source to extract import statements
    /// @param source Python source code
    /// @return Set of imported module names
    std::set<std::string> ParseImports(const std::string &source) const;

    /// @brief Parse Python source to extract class definitions
    /// @param source Python source code
    /// @return Vector of class names defined in the file
    std::vector<std::string> ParseClassNames(const std::string &source) const;

    /// @brief Check if a class inherits from InfComponent
    /// @param source Python source code
    /// @param className Name of the class to check
    /// @return True if the class appears to inherit from InfComponent
    bool IsInfComponentClass(const std::string &source, const std::string &className) const;
};

} // namespace infengine
