"""
EditorPanel — 编辑器面板统一基类 / Unified base class for editor panels.

所有面板都应继承此类并覆写 ``on_render_content(ctx)``。
基类处理窗口帧管理、样式推入/弹出、生命周期钩子和服务访问。

All panels should inherit from this class and override ``on_render_content(ctx)``.
The base class handles window frame management, style push/pop, lifecycle hooks,
and service access.

创建自定义面板 / Creating a custom panel::

    from InfEngine.engine.ui import EditorPanel, editor_panel, EditorEvent

    @editor_panel("My Debug Panel")
    class MyDebugPanel(EditorPanel):
        def on_enable(self):
            self.events.subscribe(EditorEvent.SELECTION_CHANGED, self._on_sel)

        def on_disable(self):
            self.events.unsubscribe(EditorEvent.SELECTION_CHANGED, self._on_sel)

        def on_render_content(self, ctx):
            ctx.text("Hello from my custom panel!")

        def _on_sel(self, obj):
            pass
"""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from .closable_panel import ClosablePanel

if TYPE_CHECKING:
    from InfEngine.lib import InfGUIContext
    from .editor_services import EditorServices
    from .event_bus import EditorEventBus


class EditorPanel(ClosablePanel):
    """编辑器面板统一基类。

    提供:
    - ``self.services`` — 访问 :class:`EditorServices` (engine, undo, etc.)
    - ``self.events``   — 访问 :class:`EditorEventBus`
    - ``on_enable()``   — 面板创建/重开时调用
    - ``on_disable()``  — 面板关闭时调用
    - ``on_render_content(ctx)`` — 覆写此方法渲染面板内容

    面板可覆写的钩子:
    - ``_window_flags()``       — 返回 ImGui 窗口标志
    - ``_initial_size()``       — 返回初始窗口尺寸 (w, h) 或 None
    - ``_push_window_style(ctx)`` — begin_window 前推入样式
    - ``_pop_window_style(ctx)``  — end_window 后弹出样式
    - ``_on_visible_pre(ctx)``    — begin_window 成功后、on_render_content 前
    - ``save_state() / load_state(data)`` — 面板状态持久化
    """

    def __init__(self, title: str, window_id: Optional[str] = None):
        super().__init__(title, window_id)
        self._enable_called = False

    # ------------------------------------------------------------------
    # 服务/事件访问 / Service & Event Access
    # ------------------------------------------------------------------

    @property
    def services(self) -> EditorServices:
        """访问编辑器子系统。Access to editor subsystems."""
        from .editor_services import EditorServices
        return EditorServices.instance()

    @property
    def events(self) -> EditorEventBus:
        """访问事件总线。Access to the editor event bus."""
        from .event_bus import EditorEventBus
        return EditorEventBus.instance()

    # ------------------------------------------------------------------
    # 生命周期钩子 / Lifecycle Hooks (子类覆写)
    # ------------------------------------------------------------------

    def on_enable(self) -> None:
        """面板首次渲染时调用。在此订阅事件。
        Called once when the panel is first rendered. Subscribe to events here."""
        pass

    def on_disable(self) -> None:
        """面板关闭时调用。在此取消订阅。
        Called when the panel is closed. Unsubscribe here."""
        pass

    # ------------------------------------------------------------------
    # 窗口配置钩子 / Window Configuration Hooks (子类覆写)
    # ------------------------------------------------------------------

    def _window_flags(self) -> int:
        """返回此面板的 ImGui 窗口标志。默认为 0。
        Return ImGui window flags for this panel. Default is 0."""
        return 0

    def _initial_size(self) -> Optional[tuple[float, float]]:
        """返回初始窗口尺寸 (w, h)，或 None 使用 ImGui 默认。
        Return initial window size (w, h), or None for ImGui default."""
        return None

    def _push_window_style(self, ctx) -> None:
        """在 begin_window 前推入样式变量/颜色。
        Push style vars/colors before begin_window.
        子类覆写时必须在 ``_pop_window_style`` 中弹出相同数量。"""
        pass

    def _pop_window_style(self, ctx) -> None:
        """在 end_window 后弹出样式变量/颜色。
        Pop style vars/colors after end_window.
        必须与 ``_push_window_style`` 中推入的数量一致。"""
        pass

    def _on_visible_pre(self, ctx) -> None:
        """begin_window 成功后、on_render_content 前调用。
        Called after begin_window succeeds, before on_render_content.
        用于焦点跟踪等一次性 per-frame 设置。"""
        pass

    def _on_not_visible(self, ctx) -> None:
        """begin_window 返回 False (窗口折叠/被遮挡) 时调用。
        Called when begin_window returns False (window collapsed/occluded).
        用于暂停渲染目标等资源管理。"""
        pass

    def _pre_render(self, ctx) -> None:
        """on_render 中、窗口 begin 前调用。
        Called in on_render before window begin.
        用于需要在窗口帧外执行的每帧逻辑（如延迟选择提交）。"""
        pass

    # ------------------------------------------------------------------
    # 内容渲染 / Content Rendering (子类覆写)
    # ------------------------------------------------------------------

    def on_render_content(self, ctx: InfGUIContext) -> None:
        """渲染面板内容。覆写此方法而不是 ``on_render``。
        Render panel content. Override this instead of ``on_render``."""
        pass

    # ------------------------------------------------------------------
    # 状态持久化 / State Persistence (子类覆写)
    # ------------------------------------------------------------------

    def save_state(self) -> dict:
        """返回面板状态字典，用于持久化。
        Return panel state dict for persistence."""
        return {}

    def load_state(self, data: dict) -> None:
        """从持久化数据恢复面板状态。
        Restore panel state from persisted data."""
        pass

    # ------------------------------------------------------------------
    # 统一渲染帧 / Unified Render Frame
    # ------------------------------------------------------------------

    def on_render(self, ctx) -> None:
        """统一渲染帧：样式推入 → 窗口 → 内容 → 窗口结束 → 样式弹出。

        子类不应覆写此方法。应覆写:
        - ``on_render_content(ctx)`` — 渲染内容
        - ``_window_flags()`` — 窗口标志
        - ``_initial_size()`` — 初始尺寸
        - ``_push_window_style(ctx)`` / ``_pop_window_style(ctx)`` — 样式

        Unified render frame. Subclasses should NOT override this.
        Override the hook methods above instead.
        """
        if not self._is_open:
            return

        # 触发 on_enable
        if not self._enable_called:
            self._enable_called = True
            self.on_enable()

        # 初始尺寸
        init_size = self._initial_size()
        if init_size is not None:
            from .theme import Theme
            ctx.set_next_window_size(init_size[0], init_size[1], Theme.COND_FIRST_USE_EVER)

        # 帧前逻辑
        self._pre_render(ctx)

        # 样式推入
        self._push_window_style(ctx)

        visible = self._begin_closable_window(ctx, self._window_flags())
        if visible:
            self._on_visible_pre(ctx)
            self.on_render_content(ctx)
        else:
            self._on_not_visible(ctx)
        ctx.end_window()

        # 样式弹出
        self._pop_window_style(ctx)

        # 检测关闭
        if not self._is_open:
            self.on_disable()
