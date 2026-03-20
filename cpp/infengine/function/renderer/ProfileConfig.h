#pragma once

/**
 * @file ProfileConfig.h
 * @brief Compile-time switch for frame profiling instrumentation.
 *
 * Set INFENGINE_FRAME_PROFILE to 1 to enable per-frame timing measurements
 * across the renderer (DrawFrame, DrawSceneFiltered, DrawShadowCasters,
 * RenderGraph::Execute, executor sub-timing).
 *
 * Set to 0 (default) to compile out all profiling overhead.
 */

#ifndef INFENGINE_FRAME_PROFILE
#define INFENGINE_FRAME_PROFILE 0
#endif

#ifndef INFENGINE_FRAME_PROFILE_TERMINAL
#define INFENGINE_FRAME_PROFILE_TERMINAL 0
#endif
