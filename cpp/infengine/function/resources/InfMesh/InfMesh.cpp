#include "InfMesh.h"

#include <core/log/InfLog.h>

#include <limits>

namespace infengine
{

void InfMesh::SetData(std::vector<Vertex> vertices, std::vector<uint32_t> indices, std::vector<SubMesh> subMeshes)
{
    m_vertices = std::move(vertices);
    m_indices = std::move(indices);
    m_subMeshes = std::move(subMeshes);

    RecalculateBounds();

    INFLOG_DEBUG("InfMesh::SetData: '", m_name, "' — ", m_vertices.size(), " verts, ", m_indices.size(), " indices, ",
                 m_subMeshes.size(), " submesh(es)");
}

void InfMesh::RecalculateBounds()
{
    if (m_vertices.empty()) {
        m_boundsMin = glm::vec3(0.0f);
        m_boundsMax = glm::vec3(0.0f);
        return;
    }

    constexpr float INF = std::numeric_limits<float>::max();
    m_boundsMin = glm::vec3(INF);
    m_boundsMax = glm::vec3(-INF);

    for (const auto &v : m_vertices) {
        m_boundsMin = glm::min(m_boundsMin, v.pos);
        m_boundsMax = glm::max(m_boundsMax, v.pos);
    }
}

} // namespace infengine
