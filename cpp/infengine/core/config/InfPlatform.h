#pragma once

/**
 * @file InfPlatform.h
 * @brief Centralised platform detection and Windows header isolation.
 *
 * Include this header instead of <windows.h> anywhere in the engine.
 * It guarantees:
 *   - NOMINMAX is defined before windows.h (prevents min/max macro conflicts)
 *   - WIN32_LEAN_AND_MEAN is defined (reduces windows.h bloat)
 *   - Platform macros INF_PLATFORM_WINDOWS / LINUX / MACOS / ANDROID
 *
 * Usage:
 *   #include <core/config/InfPlatform.h>
 */

// ── Platform detection ────────────────────────────────────────────────────────
#if defined(_WIN32) || defined(_WIN64)
#define INF_PLATFORM_WINDOWS 1
#elif defined(__ANDROID__)
#define INF_PLATFORM_ANDROID 1
#elif defined(__linux__)
#define INF_PLATFORM_LINUX 1
#elif defined(__APPLE__)
#include <TargetConditionals.h>
#if TARGET_OS_IPHONE
#define INF_PLATFORM_IOS 1
#else
#define INF_PLATFORM_MACOS 1
#endif
#endif

// ── Windows header configuration ──────────────────────────────────────────────
#ifdef INF_PLATFORM_WINDOWS
#ifndef NOMINMAX
#define NOMINMAX
#endif
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <windows.h>
#endif
