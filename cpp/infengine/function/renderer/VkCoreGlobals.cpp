/**
 * @file VkCoreGlobals.cpp
 * @brief InfVkCoreModular — Engine globals UBO (set 2, binding 0)
 *
 * Split from InfVkCoreModular.cpp for maintainability.
 * Contains: StageGlobals, CreateGlobalsBuffers,
 *           CreateGlobalsDescriptorResources, DestroyGlobalsDescriptorResources,
 *           CmdUpdateGlobals.
 */

#include "InfError.h"
#include "InfVkCoreModular.h"

#include <function/renderer/shader/ShaderProgram.h>

#include <cstring>

namespace infengine
{

// ============================================================================
// Public API
// ============================================================================

void InfVkCoreModular::StageGlobals(const EngineGlobalsUBO &globals)
{
    m_stagedGlobals = globals;
    m_globalsDirty = true;
}

// ============================================================================
// Buffer creation
// ============================================================================

void InfVkCoreModular::CreateGlobalsBuffers()
{
    constexpr VkDeviceSize bufferSize = sizeof(EngineGlobalsUBO);

    m_globalsBuffers.resize(m_maxFramesInFlight);
    for (size_t i = 0; i < m_maxFramesInFlight; ++i) {
        m_globalsBuffers[i] = m_resourceManager.CreateUniformBuffer(bufferSize);
    }

    INFLOG_INFO("Created engine globals UBO buffers: ", bufferSize, " bytes x ", m_maxFramesInFlight, " frames");
}

// ============================================================================
// Descriptor resources (layout + pool + sets)
// ============================================================================

bool InfVkCoreModular::CreateGlobalsDescriptorResources()
{
    VkDevice device = GetDevice();
    if (device == VK_NULL_HANDLE)
        return false;

    // Layout: set 2, binding 0 = uniform buffer, vertex + fragment stages
    VkDescriptorSetLayoutBinding binding{};
    binding.binding = 0;
    binding.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
    binding.descriptorCount = 1;
    binding.stageFlags = VK_SHADER_STAGE_VERTEX_BIT | VK_SHADER_STAGE_FRAGMENT_BIT;
    binding.pImmutableSamplers = nullptr;

    VkDescriptorSetLayoutCreateInfo layoutInfo{};
    layoutInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO;
    layoutInfo.bindingCount = 1;
    layoutInfo.pBindings = &binding;

    if (vkCreateDescriptorSetLayout(device, &layoutInfo, nullptr, &m_globalsDescSetLayout) != VK_SUCCESS) {
        INFLOG_ERROR("Failed to create globals descriptor set layout");
        return false;
    }

    // Publish to ShaderProgram so all pipelines pick up the shared layout at set 2
    ShaderProgram::SetGlobalsDescSetLayout(m_globalsDescSetLayout);

    // Pool: one set per frame-in-flight
    VkDescriptorPoolSize poolSize{};
    poolSize.type = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
    poolSize.descriptorCount = static_cast<uint32_t>(m_maxFramesInFlight);

    VkDescriptorPoolCreateInfo poolInfo{};
    poolInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO;
    poolInfo.flags = 0;
    poolInfo.maxSets = static_cast<uint32_t>(m_maxFramesInFlight);
    poolInfo.poolSizeCount = 1;
    poolInfo.pPoolSizes = &poolSize;

    if (vkCreateDescriptorPool(device, &poolInfo, nullptr, &m_globalsDescPool) != VK_SUCCESS) {
        INFLOG_ERROR("Failed to create globals descriptor pool");
        vkDestroyDescriptorSetLayout(device, m_globalsDescSetLayout, nullptr);
        m_globalsDescSetLayout = VK_NULL_HANDLE;
        ShaderProgram::SetGlobalsDescSetLayout(VK_NULL_HANDLE);
        return false;
    }

    // Allocate descriptor sets
    std::vector<VkDescriptorSetLayout> layouts(m_maxFramesInFlight, m_globalsDescSetLayout);

    VkDescriptorSetAllocateInfo allocInfo{};
    allocInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO;
    allocInfo.descriptorPool = m_globalsDescPool;
    allocInfo.descriptorSetCount = static_cast<uint32_t>(m_maxFramesInFlight);
    allocInfo.pSetLayouts = layouts.data();

    m_globalsDescSets.resize(m_maxFramesInFlight);
    if (vkAllocateDescriptorSets(device, &allocInfo, m_globalsDescSets.data()) != VK_SUCCESS) {
        INFLOG_ERROR("Failed to allocate globals descriptor sets");
        vkDestroyDescriptorPool(device, m_globalsDescPool, nullptr);
        m_globalsDescPool = VK_NULL_HANDLE;
        vkDestroyDescriptorSetLayout(device, m_globalsDescSetLayout, nullptr);
        m_globalsDescSetLayout = VK_NULL_HANDLE;
        ShaderProgram::SetGlobalsDescSetLayout(VK_NULL_HANDLE);
        return false;
    }

    // Write each descriptor set to point at the corresponding globals buffer
    for (size_t i = 0; i < m_maxFramesInFlight; ++i) {
        if (!m_globalsBuffers[i])
            continue;

        VkDescriptorBufferInfo bufInfo{};
        bufInfo.buffer = m_globalsBuffers[i]->GetBuffer();
        bufInfo.offset = 0;
        bufInfo.range = sizeof(EngineGlobalsUBO);

        VkWriteDescriptorSet write{};
        write.sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET;
        write.dstSet = m_globalsDescSets[i];
        write.dstBinding = 0;
        write.dstArrayElement = 0;
        write.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
        write.descriptorCount = 1;
        write.pBufferInfo = &bufInfo;

        vkUpdateDescriptorSets(device, 1, &write, 0, nullptr);
    }

    INFLOG_INFO("Created globals descriptor set layout, pool, and ", m_maxFramesInFlight, " sets (set 2)");
    return true;
}

void InfVkCoreModular::DestroyGlobalsDescriptorResources()
{
    VkDevice device = GetDevice();
    if (device == VK_NULL_HANDLE)
        return;

    m_globalsDescSets.clear();

    if (m_globalsDescPool != VK_NULL_HANDLE) {
        vkDestroyDescriptorPool(device, m_globalsDescPool, nullptr);
        m_globalsDescPool = VK_NULL_HANDLE;
    }
    if (m_globalsDescSetLayout != VK_NULL_HANDLE) {
        ShaderProgram::SetGlobalsDescSetLayout(VK_NULL_HANDLE);
        vkDestroyDescriptorSetLayout(device, m_globalsDescSetLayout, nullptr);
        m_globalsDescSetLayout = VK_NULL_HANDLE;
    }
}

// ============================================================================
// Command-buffer inline update
// ============================================================================

void InfVkCoreModular::CmdUpdateGlobals(VkCommandBuffer cmdBuf)
{
    if (!m_globalsDirty)
        return;
    if (m_globalsBuffers.empty() || !m_globalsBuffers[0])
        return;

    VkBuffer buffer = m_globalsBuffers[0]->GetBuffer();

    // Barrier: ensure previous shader reads from the globals UBO are complete
    VkMemoryBarrier barrier{};
    barrier.sType = VK_STRUCTURE_TYPE_MEMORY_BARRIER;
    barrier.srcAccessMask = VK_ACCESS_UNIFORM_READ_BIT;
    barrier.dstAccessMask = VK_ACCESS_TRANSFER_WRITE_BIT;
    vkCmdPipelineBarrier(cmdBuf, VK_PIPELINE_STAGE_VERTEX_SHADER_BIT | VK_PIPELINE_STAGE_FRAGMENT_SHADER_BIT,
                         VK_PIPELINE_STAGE_TRANSFER_BIT, 0, 1, &barrier, 0, nullptr, 0, nullptr);

    // Update the globals UBO inline in the command buffer
    // vkCmdUpdateBuffer has a 65536-byte limit; EngineGlobalsUBO is 128 bytes.
    vkCmdUpdateBuffer(cmdBuf, buffer, 0, sizeof(EngineGlobalsUBO), &m_stagedGlobals);

    // Barrier: ensure write is visible before subsequent shader reads
    barrier.srcAccessMask = VK_ACCESS_TRANSFER_WRITE_BIT;
    barrier.dstAccessMask = VK_ACCESS_UNIFORM_READ_BIT;
    vkCmdPipelineBarrier(cmdBuf, VK_PIPELINE_STAGE_TRANSFER_BIT,
                         VK_PIPELINE_STAGE_VERTEX_SHADER_BIT | VK_PIPELINE_STAGE_FRAGMENT_SHADER_BIT, 0, 1, &barrier, 0,
                         nullptr, 0, nullptr);

    m_globalsDirty = false;
}

} // namespace infengine
