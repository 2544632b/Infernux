#include "InfTextureLoader.hpp"

#include <algorithm>
#include <core/log/InfLog.h>
#include <filesystem>
#include <platform/filesystem/InfPath.h>
#include <stb_image.h>
#include <vector>

namespace infengine
{

InfTextureData InfTextureLoader::LoadFromFile(const std::string &filePath, const std::string &name)
{
    InfTextureData result;
    result.sourcePath = filePath;
    result.name = name.empty() ? FromFsPath(ToFsPath(filePath).stem()) : name;

    int width, height, channels;
    // Read file bytes first to support Unicode paths on Windows
    std::vector<unsigned char> fileBytes;
    if (!ReadFileBytes(filePath, fileBytes) || fileBytes.empty()) {
        INFLOG_ERROR("Failed to read texture file: ", filePath);
        return result;
    }
    stbi_uc *pixels = stbi_load_from_memory(fileBytes.data(), static_cast<int>(fileBytes.size()), &width, &height,
                                            &channels, STBI_rgb_alpha);

    if (!pixels) {
        INFLOG_ERROR("stbi_load failed for: ", filePath, " - ", stbi_failure_reason());
        return result;
    }

    result.width = width;
    result.height = height;
    result.channels = 4; // Always RGBA
    size_t dataSize = static_cast<size_t>(width) * height * 4;
    result.pixels.assign(pixels, pixels + dataSize);

    stbi_image_free(pixels);

    INFLOG_DEBUG("Loaded texture: ", result.name, " [", width, "x", height, "]");
    return result;
}

InfTextureData InfTextureLoader::LoadFromMemory(const unsigned char *data, size_t dataSize, const std::string &name)
{
    InfTextureData result;
    result.name = name;

    int width, height, channels;
    stbi_uc *pixels =
        stbi_load_from_memory(data, static_cast<int>(dataSize), &width, &height, &channels, STBI_rgb_alpha);

    if (!pixels) {
        INFLOG_ERROR("stbi_load_from_memory failed: ", stbi_failure_reason());
        return result;
    }

    result.width = width;
    result.height = height;
    result.channels = 4;
    size_t pixelDataSize = static_cast<size_t>(width) * height * 4;
    result.pixels.assign(pixels, pixels + pixelDataSize);

    stbi_image_free(pixels);

    INFLOG_DEBUG("Loaded texture from memory: ", result.name, " [", width, "x", height, "]");
    return result;
}

InfTextureData InfTextureLoader::CreateSolidColor(int width, int height, unsigned char r, unsigned char g,
                                                  unsigned char b, unsigned char a, const std::string &name)
{
    InfTextureData result;
    result.name = name;
    result.width = width;
    result.height = height;
    result.channels = 4;
    result.pixels.resize(static_cast<size_t>(width) * height * 4);

    for (int i = 0; i < width * height; ++i) {
        result.pixels[i * 4 + 0] = r;
        result.pixels[i * 4 + 1] = g;
        result.pixels[i * 4 + 2] = b;
        result.pixels[i * 4 + 3] = a;
    }

    INFLOG_DEBUG("Created solid color texture: ", name, " [", width, "x", height, "] RGBA(", (int)r, ",", (int)g, ",",
                 (int)b, ",", (int)a, ")");
    return result;
}

InfTextureData InfTextureLoader::CreateCheckerboard(int width, int height, int checkerSize, const std::string &name)
{
    InfTextureData result;
    result.name = name;
    result.width = width;
    result.height = height;
    result.channels = 4;
    result.pixels.resize(static_cast<size_t>(width) * height * 4);

    // Magenta and black checkerboard (classic "missing texture" pattern)
    const unsigned char color1[4] = {255, 0, 255, 255}; // Magenta
    const unsigned char color2[4] = {0, 0, 0, 255};     // Black

    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            int checkerX = x / checkerSize;
            int checkerY = y / checkerSize;
            const unsigned char *color = ((checkerX + checkerY) % 2 == 0) ? color1 : color2;

            int idx = (y * width + x) * 4;
            result.pixels[idx + 0] = color[0];
            result.pixels[idx + 1] = color[1];
            result.pixels[idx + 2] = color[2];
            result.pixels[idx + 3] = color[3];
        }
    }

    INFLOG_DEBUG("Created checkerboard texture: ", name, " [", width, "x", height, "] checker size: ", checkerSize);
    return result;
}

} // namespace infengine
