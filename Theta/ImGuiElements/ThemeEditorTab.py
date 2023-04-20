from PI import imgui, UILib, ImVec4, LocalCache, ImGuiTheme, ImGuiLayer

class ThemeEditor:
    __ThemePreset: str
    __CurrentTheme: ImGuiTheme
    __CurrentThemeActive: ImGuiTheme

    __Show: bool = False

    def __init__(self) -> None:
        self.__ThemePreset = LocalCache.GetProperty("ThemePreferences", "Default Dark")

        if self.__ThemePreset == "Default Dark":
            self.__CurrentTheme: ImGuiTheme = ImGuiTheme.DefaultDark.Copy()
            self.__CurrentThemeActive: ImGuiTheme = ImGuiTheme.DefaultActive.Copy()
        
        elif self.__ThemePreset == "Default Light":
            self.__CurrentTheme: ImGuiTheme = ImGuiTheme.DefaultLight.Copy()
            self.__CurrentThemeActive: ImGuiTheme = ImGuiTheme.LightActive.Copy()
        
        elif self.__ThemePreset == "Ruth":
            self.__CurrentTheme: ImGuiTheme = ImGuiTheme.Ruth.Copy()
            self.__CurrentThemeActive: ImGuiTheme = ImGuiTheme.DefaultDark.Copy()
        
        elif self.__ThemePreset == "Custom":
            self.__CurrentTheme = ImGuiTheme()
            self.__CurrentThemeActive = ImGuiTheme()
            
            for field, value in LocalCache.GetProperty('Theme').items():
                self.__CurrentTheme.AddFields({ int(field) : ImVec4( value[0], value[1], value[2], value[3] ) })
            
            for field, value in LocalCache.GetProperty('ActiveTheme').items():
                self.__CurrentThemeActive.AddFields({
                    int(field) : ImVec4( value[0], value[1], value[2], value[3] )
                })
        
        ImGuiLayer.SetTheme(self.__CurrentTheme)

    @property
    def CurrentTheme       (self) -> ImGuiTheme : return self.__CurrentTheme
    @property
    def CurrentThemeActive (self) -> ImGuiTheme : return self.__CurrentThemeActive

    def SetCurrentTheme       (self) -> None: self.__CurrentTheme.Apply()
    def SetCurrentActiveTheme (self) -> None: self.__CurrentThemeActive.Apply()

    def Show(self) -> None: self.__Show = True

    def OnImGuiRender(self) -> None:
        if not self.__Show: return

        with imgui.begin("Themes"):
            columnWidth = 150

            presets = [ "Default Dark", "Default Light", "Ruth", "Custom" ]
            changed, _, preset = UILib.DrawDropdown("Preset", presets.index(self.__ThemePreset), presets)
            self.__ThemePreset = preset

            if preset == "Custom":
                imgui.text("")
                imgui.separator()

                changed, newColor = UILib.DrawColor3Controls(
                    "Window Background", self.__CurrentTheme.Fields[imgui.COLOR_WINDOW_BACKGROUND], columnWidth
                )
                if changed:
                    self.__CurrentTheme.AddFields({
                        imgui.COLOR_WINDOW_BACKGROUND : ImVec4( *newColor, 1.0 ),
                        imgui.COLOR_CHILD_BACKGROUND  : ImVec4( 0.0, 0.0, 0.0, 0.0 ),

                        imgui.COLOR_TITLE_BACKGROUND : ImVec4( newColor[0] * 0.9, newColor[1] * 0.9, newColor[2] * 0.9, 1.0 ),
                        imgui.COLOR_TITLE_BACKGROUND_COLLAPSED : ImVec4( 1., 1.0, 1.0, 0.51 ),
                        imgui.COLOR_TITLE_BACKGROUND_ACTIVE
                            : ImVec4( newColor[0] * 0.8, newColor[1] * 0.8, newColor[2] * 0.8, 1.0 ),

                        imgui.COLOR_MENUBAR_BACKGROUND
                            : ImVec4( newColor[0] * 0.7, newColor[1] * 0.7, newColor[2] * 0.7, 1.0 ),
                    })

                changed, newColor = UILib.DrawColor3Controls(
                    "Text", self.__CurrentTheme.Fields[imgui.COLOR_TEXT], columnWidth
                )
                if changed:
                    h, s, v = imgui.color_convert_rgb_to_hsv(newColor[0], newColor[1], newColor[2])
                    v = (v * 0.6) if v > 0.5 else (v * 1.6)
                    rd, gd, bd = imgui.color_convert_hsv_to_rgb(h, s, v)

                    self.__CurrentTheme.AddFields({
                        imgui.COLOR_TEXT : ImVec4( *newColor, 1.0 ),
                        imgui.COLOR_TEXT_DISABLED : ImVec4( rd, gd, bd, 1.0 )
                    })

                changed, newColor = UILib.DrawColor3Controls(
                    "Input Background", self.__CurrentTheme.Fields[imgui.COLOR_FRAME_BACKGROUND], columnWidth
                )
                if changed:
                    h, s, v = imgui.color_convert_rgb_to_hsv(newColor[0], newColor[1], newColor[2])
                    v = (v * 0.45) if v > 0.5 else (v * 1.45)
                    rd, gd, bd = imgui.color_convert_hsv_to_rgb(h, s, v)

                    self.__CurrentTheme.AddFields({
                        imgui.COLOR_FRAME_BACKGROUND         : ImVec4( *newColor, 1.0 ),
                        imgui.COLOR_FRAME_BACKGROUND_HOVERED : ImVec4( rd, gd, bd, 1.0 ),
                        imgui.COLOR_FRAME_BACKGROUND_ACTIVE  : ImVec4( rd, gd, bd, 1.0 ),
                    })

                changed, newColor = UILib.DrawColor3Controls(
                    "Tabs", self.__CurrentTheme.Fields[imgui.COLOR_TAB], columnWidth
                )
                if changed:
                    h, s, v = imgui.color_convert_rgb_to_hsv(newColor[0], newColor[1], newColor[2])
                    v = v if v > 0.8 else (v * 1.25)
                    r, g, b = imgui.color_convert_hsv_to_rgb(h, s, v)

                    self.__CurrentTheme.AddFields({
                        imgui.COLOR_TAB         : ImVec4( *newColor, 1.0 ),
                        imgui.COLOR_TAB_HOVERED : ImVec4( r, g, b, 1.0 ),
                        imgui.COLOR_TAB_ACTIVE  : ImVec4( *newColor, 1.0 ),

                        imgui.COLOR_TAB_UNFOCUSED         : ImVec4( r, g, b, 1.0 ),
                        imgui.COLOR_TAB_UNFOCUSED_ACTIVE  : ImVec4( *newColor, 1.0 )
                    })

                changed, newColor = UILib.DrawColor3Controls(
                    "Buttons", self.__CurrentTheme.Fields[imgui.COLOR_BUTTON], columnWidth
                )
                if changed:
                    h, s, v = imgui.color_convert_rgb_to_hsv(newColor[0], newColor[1], newColor[2])
                    v = (v * 0.25) if v > 0.8 else (v * 1.1)
                    r, g, b = imgui.color_convert_hsv_to_rgb(h, s, v)

                    self.__CurrentTheme.AddFields({
                        imgui.COLOR_BUTTON         : ImVec4( *newColor, 0.40 ),
                        imgui.COLOR_BUTTON_HOVERED : ImVec4( *newColor, 1.00 ),
                        imgui.COLOR_BUTTON_ACTIVE  : ImVec4( r, g, b, 1.00 ),
                    })

                imgui.text("")

                imgui.push_id("WhilePlaying")
                imgui.text("While Playing")
                imgui.separator()

                changed, newColor = UILib.DrawColor3Controls(
                    "Window Background", self.__CurrentThemeActive.Fields[imgui.COLOR_WINDOW_BACKGROUND], columnWidth
                )
                if changed:
                    self.__CurrentThemeActive.AddFields({
                        imgui.COLOR_WINDOW_BACKGROUND : ImVec4( *newColor, 1.0 ),
                        imgui.COLOR_CHILD_BACKGROUND  : ImVec4( 0.0, 0.0, 0.0, 0.0 ),

                        imgui.COLOR_TITLE_BACKGROUND : ImVec4( newColor[0] * 0.9, newColor[1] * 0.9, newColor[2] * 0.9, 1.0 ),
                        imgui.COLOR_TITLE_BACKGROUND_COLLAPSED : ImVec4( 1., 1.0, 1.0, 0.51 ),
                        imgui.COLOR_TITLE_BACKGROUND_ACTIVE
                            : ImVec4( newColor[0] * 0.8, newColor[1] * 0.8, newColor[2] * 0.8, 1.0 ),

                        imgui.COLOR_MENUBAR_BACKGROUND
                            : ImVec4( newColor[0] * 0.7, newColor[1] * 0.7, newColor[2] * 0.7, 1.0 ),
                    })

                changed, newColor = UILib.DrawColor3Controls(
                    "Text", self.__CurrentThemeActive.Fields[imgui.COLOR_TEXT], columnWidth
                )
                if changed:
                    h, s, v = imgui.color_convert_rgb_to_hsv(newColor[0], newColor[1], newColor[2])
                    v = (v * 0.6) if v > 0.5 else (v * 1.6)
                    rd, gd, bd = imgui.color_convert_hsv_to_rgb(h, s, v)

                    self.__CurrentThemeActive.AddFields({
                        imgui.COLOR_TEXT : ImVec4( *newColor, 1.0 ),
                        imgui.COLOR_TEXT_DISABLED : ImVec4( rd, gd, bd, 1.0 )
                    })

                changed, newColor = UILib.DrawColor3Controls(
                    "Input Background", self.__CurrentThemeActive.Fields[imgui.COLOR_FRAME_BACKGROUND], columnWidth
                )
                if changed:
                    h, s, v = imgui.color_convert_rgb_to_hsv(newColor[0], newColor[1], newColor[2])
                    v = (v * 0.45) if v > 0.5 else (v * 1.45)
                    rd, gd, bd = imgui.color_convert_hsv_to_rgb(h, s, v)

                    self.__CurrentThemeActive.AddFields({
                        imgui.COLOR_FRAME_BACKGROUND         : ImVec4( *newColor, 1.0 ),
                        imgui.COLOR_FRAME_BACKGROUND_HOVERED : ImVec4( rd, gd, bd, 1.0 ),
                        imgui.COLOR_FRAME_BACKGROUND_ACTIVE  : ImVec4( rd, gd, bd, 1.0 ),
                    })

                changed, newColor = UILib.DrawColor3Controls(
                    "Tabs", self.__CurrentThemeActive.Fields[imgui.COLOR_TAB], columnWidth
                )
                if changed:
                    h, s, v = imgui.color_convert_rgb_to_hsv(newColor[0], newColor[1], newColor[2])
                    v = v if v > 0.8 else (v * 1.25)
                    r, g, b = imgui.color_convert_hsv_to_rgb(h, s, v)

                    self.__CurrentThemeActive.AddFields({
                        imgui.COLOR_TAB         : ImVec4( *newColor, 1.0 ),
                        imgui.COLOR_TAB_HOVERED : ImVec4( r, g, b, 1.0 ),
                        imgui.COLOR_TAB_ACTIVE  : ImVec4( *newColor, 1.0 ),

                        imgui.COLOR_TAB_UNFOCUSED         : ImVec4( r, g, b, 1.0 ),
                        imgui.COLOR_TAB_UNFOCUSED_ACTIVE  : ImVec4( *newColor, 1.0 )
                    })

                changed, newColor = UILib.DrawColor3Controls(
                    "Buttons", self.__CurrentThemeActive.Fields[imgui.COLOR_BUTTON], columnWidth
                )
                if changed:
                    h, s, v = imgui.color_convert_rgb_to_hsv(newColor[0], newColor[1], newColor[2])
                    v = (v * 0.25) if v > 0.8 else (v * 1.1)
                    r, g, b = imgui.color_convert_hsv_to_rgb(h, s, v)

                    self.__CurrentThemeActive.AddFields({
                        imgui.COLOR_BUTTON         : ImVec4( *newColor, 0.40 ),
                        imgui.COLOR_BUTTON_HOVERED : ImVec4( *newColor, 1.00 ),
                        imgui.COLOR_BUTTON_ACTIVE  : ImVec4( r, g, b, 1.00 ),
                    })
                
                imgui.pop_id()
                imgui.text("")

            imgui.set_cursor_pos_y(imgui.get_window_content_region_max()[1] - 25)
            imgui.set_cursor_pos_x(imgui.get_window_content_region_max()[0] - 90)

            save = imgui.button("Save")
            UILib.TooltipIfHovered("Your Theme Preferences will be saved locally")

            imgui.same_line()
            if imgui.button("Close"): self.__Show = False

            if save:
                if preset == "Default Light":
                    self.__CurrentTheme = ImGuiTheme.DefaultLight.Copy()
                    self.__CurrentThemeActive = ImGuiTheme.LightActive.Copy()

                elif preset == "Default Dark":
                    self.__CurrentTheme = ImGuiTheme.DefaultDark.Copy()
                    self.__CurrentThemeActive = ImGuiTheme.Ruth.Copy()
                
                elif preset == "Ruth":
                    self.__CurrentTheme = ImGuiTheme.Ruth.Copy()
                    self.__CurrentThemeActive = ImGuiTheme.DefaultDark.Copy()

                LocalCache.SetProperty("ThemePreferences", preset)
                
                if preset == "Custom":
                    LocalCache.SetProperties (
                        Theme=self.__CurrentTheme.Fields,
                        ActiveTheme=self.__CurrentThemeActive.Fields
                    )
                
                else: LocalCache.DeleteProperty("Theme", "ActiveTheme")

                ImGuiLayer.SetTheme(self.__CurrentTheme)
                self.__Show = False
