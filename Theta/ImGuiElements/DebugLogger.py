from PI import *

class DebugLogger:
    __Filter: int
    __Icons: Dict[str, Texture2D]

    ErrorOccurred = False

    def __init__(self) -> None:
        self.__Icons = {}
        self.__Filter = LocalCache.GetProperty('DebugConsole.Filter')
        self.__Filter = self.__Filter if self.__Filter is not None else DebugConsole.Severity.ALL

        try:
            self.__Icons["Info"]    = Texture2D.Create(".\\Theta\\Resources\\Icons\\Info.png")
            self.__Icons["Warning"] = Texture2D.Create(".\\Theta\\Resources\\Icons\\Warning.png")
            self.__Icons["Error"]   = Texture2D.Create(".\\Theta\\Resources\\Icons\\Error.png")

        # This is here for Building
        # 'cause the Build looks for files in '.'
        except FileNotFoundError:
            self.__Icons["Info"]    = Texture2D.Create(".\\Resources\\Icons\\Info.png")
            self.__Icons["Warning"] = Texture2D.Create(".\\Resources\\Icons\\Warning.png")
            self.__Icons["Error"]   = Texture2D.Create(".\\Resources\\Icons\\Error.png")

    def OnImGuiRender(self) -> None:
        with imgui.begin("Console", flags=imgui.WINDOW_NO_FOCUS_ON_APPEARING):

            if self.ErrorOccurred and (self.__Filter & DebugConsole.Severity.ERROR):
                imgui.set_window_focus()
                self.ErrorOccurred = False
                DebugConsole.ClearError()

            imgui.set_cursor_pos_y(22)
            imgui.set_cursor_pos_x(2)

            clear = imgui.button("Clear")
            imgui.same_line()
            if clear: DebugConsole.Clear()

            copy = imgui.button("Copy Latest")
            imgui.same_line()
            if copy:
                logs = DebugConsole.GetLogs(self.__Filter)
                if len(logs) > 0: text = logs[-1][1]
                else: text = ""
                imgui.set_clipboard_text(text)

            imgui.set_cursor_pos_x(imgui.get_window_content_region_max()[0] - 78)
            imgui.push_style_var(imgui.STYLE_ITEM_SPACING, ImVec2(0, 0))

            if not self.__Filter & DebugConsole.Severity.TRACE: imgui.push_style_color(imgui.COLOR_BUTTON, 0, 0, 0, 0)
            else: imgui.push_style_color(imgui.COLOR_BUTTON, 0.35, 0.35, 0.35, 1)
            includeTraces = imgui.image_button(self.__Icons["Info"].RendererID, 20, 20, (0, 1), (1, 0))
            imgui.pop_style_color()

            if includeTraces: self.__Filter ^= DebugConsole.Severity.TRACE
            imgui.same_line()

            if not self.__Filter & DebugConsole.Severity.WARN: imgui.push_style_color(imgui.COLOR_BUTTON, 0, 0, 0, 0)
            else: imgui.push_style_color(imgui.COLOR_BUTTON, 0.35, 0.35, 0.35, 1)
            includeWarns = imgui.image_button(self.__Icons["Warning"].RendererID, 20, 20, (0, 1), (1, 0))
            imgui.pop_style_color()

            if includeWarns: self.__Filter ^= DebugConsole.Severity.WARN
            imgui.same_line()

            if not self.__Filter & DebugConsole.Severity.ERROR: imgui.push_style_color(imgui.COLOR_BUTTON, 0, 0, 0, 0)
            else: imgui.push_style_color(imgui.COLOR_BUTTON, 0.35, 0.35, 0.35, 1)
            includeErrors = imgui.image_button(self.__Icons["Error"].RendererID, 20, 20, (0, 1), (1, 0))
            imgui.pop_style_color()

            if includeErrors: self.__Filter ^= DebugConsole.Severity.ERROR
            LocalCache.SetProperty("DebugConsole.Filter", self.__Filter)

            imgui.pop_style_var()

            imgui.set_cursor_pos_x(0)
            imgui.separator()
            
            for severity, log in DebugConsole.GetLogs(self.__Filter):
                if severity == DebugConsole.Severity.TRACE:
                    imgui.image(self.__Icons["Info"].RendererID, 12, 12, (0, 1), (1, 0))
                    imgui.same_line()

                    imgui.text_wrapped(log)
                
                elif severity == DebugConsole.Severity.WARN:
                    imgui.image(self.__Icons["Warning"].RendererID, 12, 12, (0, 1), (1, 0))
                    imgui.same_line()

                    imgui.push_style_color(imgui.COLOR_TEXT, 0.875, 0.8, 0.1, 1.0)
                    imgui.text_wrapped(log)
                    imgui.pop_style_color()
                
                elif severity == DebugConsole.Severity.ERROR:
                    imgui.image(self.__Icons["Error"].RendererID, 12, 12, (0, 1), (1, 0))
                    imgui.same_line()

                    imgui.push_style_color(imgui.COLOR_TEXT, 0.875, 0.1, 0.1, 1.0)
                    imgui.text_wrapped(log)
                    imgui.pop_style_color()

                imgui.separator()

            if DebugConsole.HasErrorOccurred(): self.ErrorOccurred = True
