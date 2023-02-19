from PI import imgui, StateManager, PI_V_SYNC

class DebugStatsPanel:
    @staticmethod
    def OnImGuiRender(framerate: float, hoveredEntity: int) -> bool:
        with imgui.begin("DEBUG Stats"):
            global PI_V_SYNC
            clicked, vSync = imgui.checkbox("VSync", PI_V_SYNC)

            if clicked:
                StateManager.GetCurrentWindow().SetVSync(vSync)
                PI_V_SYNC = vSync

            imgui.text("FPS: {}".format(round(framerate)))
            imgui.text("Last Frame Time: {}".format(round(1 / framerate, 5)))
            imgui.text("Hovered Entity: {}".format(int(hoveredEntity) if hoveredEntity else 0))

            imgui.text("\nRenderer Stats:")
            imgui.separator()
            imgui.text("Draw Calls: {}".format(StateManager.Stats.DrawCalls))

            flags = imgui.TREE_NODE_OPEN_ON_ARROW | imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH
            if imgui.tree_node("Shaders (Binded {} times)".format(StateManager.Stats.Shaders.ShadersBinded),
                flags=flags):

                imgui.text("Uniforms:")
                imgui.text("\tTotal Uniforms Uploaded : {}" \
                    .format(StateManager.Stats.Shaders.Uniforms.TotalUniforms))

                imgui.text("")
                imgui.text("\tTotal Ints Uploaded : {}" \
                    .format(StateManager.Stats.Shaders.Uniforms.Ints))

                imgui.text("\tTotal Floats Uploaded : {}" \
                    .format(StateManager.Stats.Shaders.Uniforms.Floats))

                imgui.text("")
                imgui.text("\tTotal Vector3's Uploaded : {}" \
                    .format(StateManager.Stats.Shaders.Uniforms.Vector3))

                imgui.text("\tTotal Vector4's Uploaded : {}" \
                    .format(StateManager.Stats.Shaders.Uniforms.Vector4))

                imgui.text("")
                imgui.text("\tTotal Matrix 3x3 Uploaded : {}" \
                    .format(StateManager.Stats.Shaders.Uniforms.Matrix_3x3))

                imgui.text("\tTotal Matrix 4x4 Uploaded : {}" \
                    .format(StateManager.Stats.Shaders.Uniforms.Matrix_4x4))

                imgui.tree_pop()

            return vSync
