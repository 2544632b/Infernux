/**
 * @file FullscreenRenderer.cpp
 * @brief Implementation of the FullscreenRenderer utility
 */

#include "FullscreenRenderer.h"
#include "InfVkCoreModular.h"
#include "shader/ShaderProgram.h"
#include "vk/VkDeviceContext.h"
#include "vk/VkPipelineManager.h"
#include "vk/VkSwapchainManager.h"
#include <core/error/InfError.h>

namespace infengine
{

// ============================================================================
// Lifecycle
// ============================================================================

FullscreenRenderer::~FullscreenRenderer()
{
    Destroy();
}

void FullscreenRenderer::Initialize(InfVkCoreModular *vkCore)
{
    if (!vkCore) {
        INFLOG_ERROR("FullscreenRenderer::Initialize: null vkCore");
        return;
    }
    m_vkCore = vkCore;
    m_device = vkCore->GetDevice();

    CreateLinearSampler();
    CreateNearestSampler();
    CreateDescriptorPools();

    INFLOG_INFO("FullscreenRenderer initialized");
}

void FullscreenRenderer::Destroy()
{
    if (m_device == VK_NULL_HANDLE)
        return;

    vkDeviceWaitIdle(m_device);

    for (auto &[key, entry] : m_pipelineCache) {
        if (entry.pipeline != VK_NULL_HANDLE)
            vkDestroyPipeline(m_device, entry.pipeline, nullptr);
        if (entry.layoutOwned && entry.layout != VK_NULL_HANDLE)
            vkDestroyPipelineLayout(m_device, entry.layout, nullptr);
        if (entry.descSetLayout != VK_NULL_HANDLE)
            vkDestroyDescriptorSetLayout(m_device, entry.descSetLayout, nullptr);
        if (entry.emptyGapLayout != VK_NULL_HANDLE)
            vkDestroyDescriptorSetLayout(m_device, entry.emptyGapLayout, nullptr);
    }
    m_pipelineCache.clear();

    for (VkDescriptorPool pool : m_descriptorPools) {
        if (pool != VK_NULL_HANDLE) {
            vkDestroyDescriptorPool(m_device, pool, nullptr);
        }
    }
    m_descriptorPools.clear();

    if (m_linearSampler != VK_NULL_HANDLE) {
        vkDestroySampler(m_device, m_linearSampler, nullptr);
        m_linearSampler = VK_NULL_HANDLE;
    }

    if (m_nearestSampler != VK_NULL_HANDLE) {
        vkDestroySampler(m_device, m_nearestSampler, nullptr);
        m_nearestSampler = VK_NULL_HANDLE;
    }

    m_device = VK_NULL_HANDLE;
    m_vkCore = nullptr;
}

// ============================================================================
// Pipeline management
// ============================================================================

const FullscreenPipelineEntry &FullscreenRenderer::EnsurePipeline(const FullscreenPipelineKey &key)
{
    auto it = m_pipelineCache.find(key);
    if (it != m_pipelineCache.end()) {
        return it->second;
    }

    auto entry = CreatePipeline(key);
    auto [insertIt, inserted] = m_pipelineCache.emplace(key, entry);
    return insertIt->second;
}

FullscreenPipelineEntry FullscreenRenderer::CreatePipeline(const FullscreenPipelineKey &key)
{
    FullscreenPipelineEntry entry{};

    if (!m_vkCore) {
        INFLOG_ERROR("FullscreenRenderer::CreatePipeline: not initialized");
        return entry;
    }

    auto &pipelineMgr = m_vkCore->GetPipelineManager();

    // ------------------------------------------------------------------
    // 1. Descriptor set layout: N combined image samplers (fragment)
    // ------------------------------------------------------------------
    std::vector<VkDescriptorSetLayoutBinding> bindings;
    for (uint32_t i = 0; i < key.inputTextureCount; ++i) {
        VkDescriptorSetLayoutBinding b{};
        b.binding = i;
        b.descriptorType = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
        b.descriptorCount = 1;
        b.stageFlags = VK_SHADER_STAGE_FRAGMENT_BIT;
        b.pImmutableSamplers = nullptr;
        bindings.push_back(b);
    }

    VkDescriptorSetLayoutCreateInfo layoutCI{};
    layoutCI.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO;
    layoutCI.bindingCount = static_cast<uint32_t>(bindings.size());
    layoutCI.pBindings = bindings.data();

    VkDescriptorSetLayout descSetLayout = VK_NULL_HANDLE;
    if (vkCreateDescriptorSetLayout(m_device, &layoutCI, nullptr, &descSetLayout) != VK_SUCCESS) {
        INFLOG_ERROR("FullscreenRenderer: Failed to create descriptor set layout for '", key.shaderName, "'");
        return entry;
    }
    entry.descSetLayout = descSetLayout;

    // ------------------------------------------------------------------
    // 2. Pipeline layout: desc sets + push constants (128 bytes, fragment)
    //    set 0 = textures, set 1 = empty (per-view gap), set 2 = globals
    // ------------------------------------------------------------------
    VkPushConstantRange pushRange{};
    pushRange.stageFlags = VK_SHADER_STAGE_FRAGMENT_BIT;
    pushRange.offset = 0;
    pushRange.size = sizeof(FullscreenPushConstants);

    // Build set layout array: [0]=textures, optional [1]=empty, [2]=globals
    std::vector<VkDescriptorSetLayout> setLayouts = {descSetLayout};
    VkDescriptorSetLayout emptyLayout = VK_NULL_HANDLE;
    VkDescriptorSetLayout globalsLayout = ShaderProgram::GetGlobalsDescSetLayout();

    if (globalsLayout != VK_NULL_HANDLE) {
        // Create empty layout for the per-view gap (set 1)
        VkDescriptorSetLayoutCreateInfo emptyCI{};
        emptyCI.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO;
        emptyCI.bindingCount = 0;
        emptyCI.pBindings = nullptr;
        vkCreateDescriptorSetLayout(m_device, &emptyCI, nullptr, &emptyLayout);
        setLayouts.push_back(emptyLayout);   // set 1
        setLayouts.push_back(globalsLayout); // set 2
    }

    VkPipelineLayoutCreateInfo pipeLayoutCI{};
    pipeLayoutCI.sType = VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO;
    pipeLayoutCI.setLayoutCount = static_cast<uint32_t>(setLayouts.size());
    pipeLayoutCI.pSetLayouts = setLayouts.data();
    pipeLayoutCI.pushConstantRangeCount = 1;
    pipeLayoutCI.pPushConstantRanges = &pushRange;

    VkPipelineLayout pipeLayout = VK_NULL_HANDLE;
    if (vkCreatePipelineLayout(m_device, &pipeLayoutCI, nullptr, &pipeLayout) != VK_SUCCESS) {
        INFLOG_ERROR("FullscreenRenderer: Failed to create pipeline layout for '", key.shaderName, "'");
        vkDestroyDescriptorSetLayout(m_device, descSetLayout, nullptr);
        if (emptyLayout != VK_NULL_HANDLE)
            vkDestroyDescriptorSetLayout(m_device, emptyLayout, nullptr);
        entry.descSetLayout = VK_NULL_HANDLE;
        return entry;
    }
    entry.layout = pipeLayout;
    entry.emptyGapLayout = emptyLayout;
    entry.layoutOwned = true;

    // ------------------------------------------------------------------
    // 3. Shader modules
    // ------------------------------------------------------------------
    // Try effect-specific vertex shader first; fall back to the shared
    // fullscreen_triangle vertex shader if not found.
    VkShaderModule vertModule = m_vkCore->GetShaderModule(key.shaderName, "vertex");
    if (vertModule == VK_NULL_HANDLE) {
        vertModule = m_vkCore->GetShaderModule("fullscreen_triangle", "vertex");
    }
    VkShaderModule fragModule = m_vkCore->GetShaderModule(key.shaderName, "fragment");

    if (vertModule == VK_NULL_HANDLE || fragModule == VK_NULL_HANDLE) {
        INFLOG_ERROR("FullscreenRenderer: Missing shader modules for '", key.shaderName,
                     "' (vert=", (vertModule != VK_NULL_HANDLE ? "OK" : "MISSING"),
                     ", frag=", (fragModule != VK_NULL_HANDLE ? "OK" : "MISSING"), ")");
        vkDestroyPipelineLayout(m_device, pipeLayout, nullptr);
        vkDestroyDescriptorSetLayout(m_device, descSetLayout, nullptr);
        if (emptyLayout != VK_NULL_HANDLE)
            vkDestroyDescriptorSetLayout(m_device, emptyLayout, nullptr);
        entry.layout = VK_NULL_HANDLE;
        entry.layoutOwned = false;
        entry.descSetLayout = VK_NULL_HANDLE;
        entry.emptyGapLayout = VK_NULL_HANDLE;
        return entry;
    }

    // ------------------------------------------------------------------
    // 4. Graphics pipeline (no vertex input, no depth, no cull)
    // ------------------------------------------------------------------
    // Shader stages
    VkPipelineShaderStageCreateInfo shaderStages[2]{};
    shaderStages[0].sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
    shaderStages[0].stage = VK_SHADER_STAGE_VERTEX_BIT;
    shaderStages[0].module = vertModule;
    shaderStages[0].pName = "main";
    shaderStages[1].sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
    shaderStages[1].stage = VK_SHADER_STAGE_FRAGMENT_BIT;
    shaderStages[1].module = fragModule;
    shaderStages[1].pName = "main";

    // Empty vertex input (procedural fullscreen triangle)
    VkPipelineVertexInputStateCreateInfo vertexInput{};
    vertexInput.sType = VK_STRUCTURE_TYPE_PIPELINE_VERTEX_INPUT_STATE_CREATE_INFO;

    VkPipelineInputAssemblyStateCreateInfo inputAssembly{};
    inputAssembly.sType = VK_STRUCTURE_TYPE_PIPELINE_INPUT_ASSEMBLY_STATE_CREATE_INFO;
    inputAssembly.topology = VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST;

    // Dynamic viewport + scissor
    VkPipelineViewportStateCreateInfo viewportState{};
    viewportState.sType = VK_STRUCTURE_TYPE_PIPELINE_VIEWPORT_STATE_CREATE_INFO;
    viewportState.viewportCount = 1;
    viewportState.scissorCount = 1;

    VkDynamicState dynamicStates[] = {VK_DYNAMIC_STATE_VIEWPORT, VK_DYNAMIC_STATE_SCISSOR};
    VkPipelineDynamicStateCreateInfo dynamicState{};
    dynamicState.sType = VK_STRUCTURE_TYPE_PIPELINE_DYNAMIC_STATE_CREATE_INFO;
    dynamicState.dynamicStateCount = 2;
    dynamicState.pDynamicStates = dynamicStates;

    // Rasterization: no cull, fill
    VkPipelineRasterizationStateCreateInfo rasterizer{};
    rasterizer.sType = VK_STRUCTURE_TYPE_PIPELINE_RASTERIZATION_STATE_CREATE_INFO;
    rasterizer.polygonMode = VK_POLYGON_MODE_FILL;
    rasterizer.cullMode = VK_CULL_MODE_NONE;
    rasterizer.frontFace = VK_FRONT_FACE_CLOCKWISE;
    rasterizer.lineWidth = 1.0f;

    // Multisample
    VkPipelineMultisampleStateCreateInfo multisampling{};
    multisampling.sType = VK_STRUCTURE_TYPE_PIPELINE_MULTISAMPLE_STATE_CREATE_INFO;
    multisampling.rasterizationSamples = key.samples;

    // No depth
    VkPipelineDepthStencilStateCreateInfo depthStencil{};
    depthStencil.sType = VK_STRUCTURE_TYPE_PIPELINE_DEPTH_STENCIL_STATE_CREATE_INFO;
    depthStencil.depthTestEnable = VK_FALSE;
    depthStencil.depthWriteEnable = VK_FALSE;

    // Color blend: no blend (overwrite), single attachment
    VkPipelineColorBlendAttachmentState blendAttachment{};
    blendAttachment.colorWriteMask =
        VK_COLOR_COMPONENT_R_BIT | VK_COLOR_COMPONENT_G_BIT | VK_COLOR_COMPONENT_B_BIT | VK_COLOR_COMPONENT_A_BIT;
    blendAttachment.blendEnable = VK_FALSE;

    VkPipelineColorBlendStateCreateInfo colorBlending{};
    colorBlending.sType = VK_STRUCTURE_TYPE_PIPELINE_COLOR_BLEND_STATE_CREATE_INFO;
    colorBlending.attachmentCount = 1;
    colorBlending.pAttachments = &blendAttachment;

    // Create pipeline
    VkGraphicsPipelineCreateInfo pipelineCI{};
    pipelineCI.sType = VK_STRUCTURE_TYPE_GRAPHICS_PIPELINE_CREATE_INFO;
    pipelineCI.stageCount = 2;
    pipelineCI.pStages = shaderStages;
    pipelineCI.pVertexInputState = &vertexInput;
    pipelineCI.pInputAssemblyState = &inputAssembly;
    pipelineCI.pViewportState = &viewportState;
    pipelineCI.pRasterizationState = &rasterizer;
    pipelineCI.pMultisampleState = &multisampling;
    pipelineCI.pDepthStencilState = &depthStencil;
    pipelineCI.pColorBlendState = &colorBlending;
    pipelineCI.pDynamicState = &dynamicState;
    pipelineCI.layout = pipeLayout;
    pipelineCI.renderPass = key.renderPass;
    pipelineCI.subpass = 0;

    VkPipeline pipeline = VK_NULL_HANDLE;
    if (vkCreateGraphicsPipelines(m_device, VK_NULL_HANDLE, 1, &pipelineCI, nullptr, &pipeline) != VK_SUCCESS) {
        INFLOG_ERROR("FullscreenRenderer: Failed to create pipeline for '", key.shaderName, "'");
        vkDestroyPipelineLayout(m_device, pipeLayout, nullptr);
        vkDestroyDescriptorSetLayout(m_device, descSetLayout, nullptr);
        entry.layout = VK_NULL_HANDLE;
        entry.layoutOwned = false;
        entry.descSetLayout = VK_NULL_HANDLE;
        return entry;
    }
    entry.pipeline = pipeline;

    return entry;
}

// ============================================================================
// Per-frame pool reset
// ============================================================================

void FullscreenRenderer::ResetPool()
{
    VkDescriptorPool pool = GetCurrentDescriptorPool();
    if (pool != VK_NULL_HANDLE) {
        vkResetDescriptorPool(m_device, pool, 0);
    }
}

// ============================================================================
// Descriptor set allocation
// ============================================================================

VkDescriptorSet FullscreenRenderer::AllocateDescriptorSet(VkDescriptorSetLayout layout, const VkImageView *inputViews,
                                                          uint32_t inputViewCount, const bool *depthInputs,
                                                          VkSampler colorSampler)
{
    VkDescriptorPool pool = GetCurrentDescriptorPool();
    if (pool == VK_NULL_HANDLE || layout == VK_NULL_HANDLE)
        return VK_NULL_HANDLE;

    VkDescriptorSetAllocateInfo allocInfo{};
    allocInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO;
    allocInfo.descriptorPool = pool;
    allocInfo.descriptorSetCount = 1;
    allocInfo.pSetLayouts = &layout;

    VkDescriptorSet descSet = VK_NULL_HANDLE;
    if (vkAllocateDescriptorSets(m_device, &allocInfo, &descSet) != VK_SUCCESS) {
        INFLOG_ERROR("FullscreenRenderer: Failed to allocate descriptor set");
        return VK_NULL_HANDLE;
    }

    // Write image descriptors
    std::array<VkDescriptorImageInfo, 8> smallImageInfos{};
    std::array<VkWriteDescriptorSet, 8> smallWrites{};
    std::vector<VkDescriptorImageInfo> largeImageInfos;
    std::vector<VkWriteDescriptorSet> largeWrites;

    VkDescriptorImageInfo *imageInfos = nullptr;
    VkWriteDescriptorSet *writes = nullptr;
    if (inputViewCount <= smallImageInfos.size()) {
        imageInfos = smallImageInfos.data();
        writes = smallWrites.data();
    } else {
        largeImageInfos.resize(inputViewCount);
        largeWrites.resize(inputViewCount);
        imageInfos = largeImageInfos.data();
        writes = largeWrites.data();
    }

    for (uint32_t i = 0; i < inputViewCount; ++i) {
        const bool isDepthInput = (depthInputs != nullptr) ? depthInputs[i] : false;
        imageInfos[i].sampler = isDepthInput ? m_nearestSampler : colorSampler;
        imageInfos[i].imageView = inputViews[i];
        imageInfos[i].imageLayout =
            isDepthInput ? VK_IMAGE_LAYOUT_DEPTH_STENCIL_READ_ONLY_OPTIMAL : VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL;

        writes[i] = {};
        writes[i].sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET;
        writes[i].dstSet = descSet;
        writes[i].dstBinding = i;
        writes[i].dstArrayElement = 0;
        writes[i].descriptorType = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
        writes[i].descriptorCount = 1;
        writes[i].pImageInfo = &imageInfos[i];
    }

    if (inputViewCount > 0) {
        vkUpdateDescriptorSets(m_device, inputViewCount, writes, 0, nullptr);
    }

    return descSet;
}

// ============================================================================
// Draw
// ============================================================================

void FullscreenRenderer::Draw(VkCommandBuffer cmdBuf, const FullscreenPipelineEntry &entry, VkDescriptorSet descSet,
                              const FullscreenPushConstants &pushConstants, uint32_t pushConstantSize)
{
    if (entry.pipeline == VK_NULL_HANDLE)
        return;

    // Bind pipeline
    vkCmdBindPipeline(cmdBuf, VK_PIPELINE_BIND_POINT_GRAPHICS, entry.pipeline);

    // Bind descriptor set 0 (input textures)
    if (descSet != VK_NULL_HANDLE) {
        vkCmdBindDescriptorSets(cmdBuf, VK_PIPELINE_BIND_POINT_GRAPHICS, entry.layout, 0, 1, &descSet, 0, nullptr);
    }

    // Bind descriptor set 2 (engine globals UBO) — provides _Globals to fullscreen shaders
    if (m_vkCore && entry.emptyGapLayout != VK_NULL_HANDLE) {
        VkDescriptorSet globalsDescSet = m_vkCore->GetCurrentGlobalsDescSet();
        if (globalsDescSet != VK_NULL_HANDLE) {
            vkCmdBindDescriptorSets(cmdBuf, VK_PIPELINE_BIND_POINT_GRAPHICS, entry.layout, 2, 1, &globalsDescSet, 0,
                                    nullptr);
        }
    }

    // Push constants
    if (pushConstantSize > 0) {
        vkCmdPushConstants(cmdBuf, entry.layout, VK_SHADER_STAGE_FRAGMENT_BIT, 0, pushConstantSize,
                           pushConstants.values);
    }

    // Draw fullscreen triangle (3 vertices, no vertex buffer)
    vkCmdDraw(cmdBuf, 3, 1, 0, 0);
}

// ============================================================================
// Private helpers
// ============================================================================

uint32_t FullscreenRenderer::GetCurrentFrameIndex() const
{
    if (!m_vkCore) {
        return 0;
    }
    return m_vkCore->GetSwapchain().GetCurrentFrame() %
           static_cast<uint32_t>(m_descriptorPools.empty() ? 1 : m_descriptorPools.size());
}

VkDescriptorPool FullscreenRenderer::GetCurrentDescriptorPool() const
{
    if (m_descriptorPools.empty()) {
        return VK_NULL_HANDLE;
    }
    return m_descriptorPools[GetCurrentFrameIndex()];
}

void FullscreenRenderer::CreateDescriptorPools()
{
    m_descriptorPools.assign(vk::VkSwapchainManager::MAX_FRAMES_IN_FLIGHT, VK_NULL_HANDLE);

    for (size_t frameIndex = 0; frameIndex < m_descriptorPools.size(); ++frameIndex) {
        VkDescriptorPoolSize poolSize{};
        poolSize.type = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
        poolSize.descriptorCount = 256;

        VkDescriptorPoolCreateInfo poolCI{};
        poolCI.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO;
        poolCI.flags = VK_DESCRIPTOR_POOL_CREATE_FREE_DESCRIPTOR_SET_BIT;
        poolCI.maxSets = 128;
        poolCI.poolSizeCount = 1;
        poolCI.pPoolSizes = &poolSize;

        if (vkCreateDescriptorPool(m_device, &poolCI, nullptr, &m_descriptorPools[frameIndex]) != VK_SUCCESS) {
            INFLOG_ERROR("FullscreenRenderer: Failed to create descriptor pool for frame ", frameIndex);
            for (VkDescriptorPool pool : m_descriptorPools) {
                if (pool != VK_NULL_HANDLE) {
                    vkDestroyDescriptorPool(m_device, pool, nullptr);
                }
            }
            m_descriptorPools.clear();
            return;
        }
    }
}

void FullscreenRenderer::CreateLinearSampler()
{
    VkSamplerCreateInfo samplerCI{};
    samplerCI.sType = VK_STRUCTURE_TYPE_SAMPLER_CREATE_INFO;
    samplerCI.magFilter = VK_FILTER_LINEAR;
    samplerCI.minFilter = VK_FILTER_LINEAR;
    samplerCI.mipmapMode = VK_SAMPLER_MIPMAP_MODE_LINEAR;
    samplerCI.addressModeU = VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE;
    samplerCI.addressModeV = VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE;
    samplerCI.addressModeW = VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE;
    samplerCI.mipLodBias = 0.0f;
    samplerCI.maxAnisotropy = 1.0f;
    samplerCI.minLod = 0.0f;
    samplerCI.maxLod = 0.0f;

    if (vkCreateSampler(m_device, &samplerCI, nullptr, &m_linearSampler) != VK_SUCCESS) {
        INFLOG_ERROR("FullscreenRenderer: Failed to create linear sampler");
    }
}

void FullscreenRenderer::CreateNearestSampler()
{
    VkSamplerCreateInfo samplerCI{};
    samplerCI.sType = VK_STRUCTURE_TYPE_SAMPLER_CREATE_INFO;
    samplerCI.magFilter = VK_FILTER_NEAREST;
    samplerCI.minFilter = VK_FILTER_NEAREST;
    samplerCI.mipmapMode = VK_SAMPLER_MIPMAP_MODE_NEAREST;
    samplerCI.addressModeU = VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE;
    samplerCI.addressModeV = VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE;
    samplerCI.addressModeW = VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE;
    samplerCI.mipLodBias = 0.0f;
    samplerCI.maxAnisotropy = 1.0f;
    samplerCI.minLod = 0.0f;
    samplerCI.maxLod = 0.0f;

    if (vkCreateSampler(m_device, &samplerCI, nullptr, &m_nearestSampler) != VK_SUCCESS) {
        INFLOG_ERROR("FullscreenRenderer: Failed to create nearest sampler");
    }
}

} // namespace infengine
