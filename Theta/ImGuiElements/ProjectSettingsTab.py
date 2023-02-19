from PI import *

class ProjectSettingsTab:
    class SettingSelection:
        Null, \
        General, Time, Debugging \
            = range(4)

    __Show: bool = False
    __CurrentSelection: int = SettingSelection.Null

    def __init__(self) -> None: pass

    def Show(self) -> None: self.__Show = True

    def OnImGuiRender(self, bgColor: ImVec4, activeColor: ImVec4) -> None:
        if not self.__Show: return

        imgui.begin("ProjectSettings")

        imgui.columns(2)

        imgui.set_column_width(0, 150)
        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, ImVec2(0, 0))

        imgui.push_font(ImGuiLayer.GlobalHeadingFont)

        color = bgColor
        if self.__CurrentSelection == ProjectSettingsTab.SettingSelection.General: color = activeColor
        imgui.push_style_color(imgui.COLOR_BUTTON, *color)
        if imgui.button("General", 135): self.__CurrentSelection = ProjectSettingsTab.SettingSelection.General
        imgui.pop_style_color()

        color = bgColor
        if self.__CurrentSelection == ProjectSettingsTab.SettingSelection.Time: color = activeColor
        imgui.push_style_color(imgui.COLOR_BUTTON, *color)
        if imgui.button("Time", 135): self.__CurrentSelection = ProjectSettingsTab.SettingSelection.Time
        imgui.pop_style_color()

        color = bgColor
        if self.__CurrentSelection == ProjectSettingsTab.SettingSelection.Debugging: color = activeColor
        imgui.push_style_color(imgui.COLOR_BUTTON, *color)
        if imgui.button("Debugging", 135): self.__CurrentSelection = ProjectSettingsTab.SettingSelection.Debugging
        imgui.pop_style_color()

        imgui.pop_font()
        imgui.pop_style_var()

        imgui.next_column()
        
        if self.__CurrentSelection == ProjectSettingsTab.SettingSelection.General:
            imgui.push_font(ImGuiLayer.GlobalHeadingFont)
            imgui.text("General Settings:")
            imgui.pop_font()
        
        if self.__CurrentSelection == ProjectSettingsTab.SettingSelection.Time:
            imgui.push_font(ImGuiLayer.GlobalHeadingFont)
            imgui.text("Time Settings:")
            imgui.pop_font()
        
        if self.__CurrentSelection == ProjectSettingsTab.SettingSelection.Debugging:
            imgui.push_font(ImGuiLayer.GlobalHeadingFont)
            imgui.text("Debugging Settings:")
            imgui.pop_font()

        imgui.set_cursor_pos_x(imgui.get_window_content_region_max()[0] - 95)
        imgui.set_cursor_pos_y(imgui.get_window_content_region_max()[1] - 25)

        apply = imgui.button("Apply")
        if imgui.is_item_hovered():
            imgui.begin_tooltip()
            imgui.text("Project Settings are local to this project")
            imgui.end_tooltip()

        imgui.same_line()
        if imgui.button("Close"): self.__Show = False

        if apply: self.__Show = False

        imgui.end()
