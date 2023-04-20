from PI import *

class ProjectSettingsTab:
    class SettingSelection:
        Null, \
        General, Time, Debugging \
            = range(4)

    __Show: bool = False
    __CurrentSelection: int = SettingSelection.Null

    __Settings: Dict[str, Any]
    __TempSettings: Dict[str, Any]

    def __init__(self) -> None: self.Init()

    def Init(self) -> None:
        defaultSettings = {
            "Time.Scale": 1,
            "Time.GameScale": 1,

            "Debugging.EnableDebugging": False,
            "Debugging.PythonPath": "",
            "Debugging.Port": 6969,
            "Debugging.WaitOnPlay": True,
        }

        self.__Settings: Dict[str, Any] = ProjectCache.GetProperty("ProjectSettings", defaultSettings)
        self.__TempSettings = self.__Settings.copy()

        if self.__Settings["Debugging.EnableDebugging"]:
            self.__StartDebugAdapter()

    def __del__(self) -> None: ProjectCache.SetProperty("ProjectSettings", self.__Settings)

    def Show(self) -> None: self.__Show = True

    @property
    def Settings(self) -> Dict[str, Any]: return self.__Settings

    def __StartDebugAdapter(self) -> None:
        pythonPath = self.__TempSettings["Debugging.PythonPath"]
        port = self.__TempSettings["Debugging.Port"]

        if (not ScriptingEngine.Debugger.Init(pythonPath) or
            not ScriptingEngine.Debugger.Listen(port)):
            DebugConsole.Error(f"Envalid python path!! or Debugger is already Running")

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

            with imgui.begin_child("##UI", height=imgui.get_window_content_region_max()[1] - 90):
                timeScaleChanged, newTimeScale = UILib.DrawFloatControls(
                    "Scale", self.__TempSettings["Time.Scale"], speed=0.01, minValue=0.01, maxValue=10,
                    tooltip="This applies to all items"
                )
                if timeScaleChanged: self.__TempSettings["Time.Scale"] = newTimeScale

                timeScaleChanged, newTimeScale = UILib.DrawFloatControls(
                    "GameScale", self.__TempSettings["Time.GameScale"], speed=0.01, minValue=0.01, maxValue=10,
                    tooltip="This only applies to Script.OnUpdate()"
                )
                if timeScaleChanged: self.__TempSettings["Time.GameScale"] = newTimeScale
        
        if self.__CurrentSelection == ProjectSettingsTab.SettingSelection.Debugging:
            imgui.push_font(ImGuiLayer.GlobalHeadingFont)
            imgui.text("Debugging Settings:")
            imgui.pop_font()

            with imgui.begin_child("##UI", height=imgui.get_window_content_region_max()[1] - 90):
                enabledChanged, enable = UILib.DrawBoolControls(
                    "Enable Debugging", self.__TempSettings["Debugging.EnableDebugging"], columnWidth=125
                )
                if enabledChanged: self.__TempSettings["Debugging.EnableDebugging"] = enable

                if self.__TempSettings["Debugging.EnableDebugging"]:
                    imgui.separator()
                    changed, newPythonPath = UILib.DrawSelectableFileField(
                        "Python Path", self.__TempSettings["Debugging.PythonPath"], columnWidth=100,
                        filetypes=( ("Python (python.exe)", ".exe"), ), selectorTooltip="Select Python Location"
                    )                    
                    if changed: self.__TempSettings["Debugging.PythonPath"] = newPythonPath

                    changed, newPort = UILib.DrawIntControls(
                        "Port", self.__TempSettings["Debugging.Port"], speed=0.25
                    )
                    if changed: self.__TempSettings["Debugging.Port"] = newPort

                    changed, waitOnPlay = UILib.DrawBoolControls(
                        "Wait On Play", self.__TempSettings["Debugging.WaitOnPlay"]
                    )
                    if changed: self.__TempSettings["Debugging.WaitOnPlay"] = waitOnPlay

                    if not ScriptingEngine.Debugger.Running and UILib.DrawButton("Start Debug Adapter"):
                        self.__StartDebugAdapter()

        imgui.set_cursor_pos_x(imgui.get_window_content_region_max()[0] - 95)
        imgui.set_cursor_pos_y(imgui.get_window_content_region_max()[1] - 25)

        apply = UILib.DrawButton("Apply", tooltip="Project Settings are local to this project")

        imgui.same_line()
        if imgui.button("Close"):
            self.__TempSettings = self.__Settings.copy()
            self.__Show = False

        if apply:
            # Time Settings
            if self.__TempSettings["Time.Scale"] != self.__Settings["Time.Scale"]:
                Timestep.Scale = self.__TempSettings["Time.Scale"]
            if self.__TempSettings["Time.GameScale"] != self.__Settings["Time.GameScale"]:
                Timestep.GameScale = self.__TempSettings["Time.GameScale"]

            # Debugger Settings
            if self.__TempSettings["Debugging.EnableDebugging"] != self.__Settings["Debugging.EnableDebugging"]:
                if not ScriptingEngine.Debugger.Running:
                    self.__StartDebugAdapter()

            self.__Settings = self.__TempSettings.copy()
            ProjectCache.SetProperty("ProjectSettings", self.__Settings)
            ProjectCache.DumpFields()
            self.__Show = False

        imgui.end()
