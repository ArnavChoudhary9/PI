from ..Core    import Random
from ..Logging import PI_CORE_WARN

import imgui
import pyrr
from typing import Callable, Iterable, List, Tuple

class UILib:
    class _FILE_DIALOGUE_RESOURCES:
        IsLoaded: bool = False
        
        _Root = None

        LoadFileLoader: Callable[[ Iterable[Tuple[str, str]] ], str]
        SaveFileLoader: Callable[[ Iterable[Tuple[str, str]] ], str]

        @staticmethod
        def Init() -> None:
            if not UILib._FILE_DIALOGUE_RESOURCES.IsLoaded:
                import tkinter as tk
                from   tkinter import filedialog
                
                UILib._FILE_DIALOGUE_RESOURCES._Root = tk.Tk()
                UILib._FILE_DIALOGUE_RESOURCES._Root.withdraw()

                UILib._FILE_DIALOGUE_RESOURCES.LoadFileLoader = filedialog.askopenfilename
                UILib._FILE_DIALOGUE_RESOURCES.SaveFileLoader = filedialog.asksaveasfilename

            UILib._FILE_DIALOGUE_RESOURCES.IsLoaded = True

    @staticmethod
    def DrawVector3Controls(lable: str, values: pyrr.Vector3, resetValue: float=0, speed: float=0.05, columnWidth: float=100) -> Tuple[bool, pyrr.Vector3]:
        imgui.push_id(lable)

        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()

        imgui.push_item_width(imgui.calculate_item_width()/3)
        imgui.push_item_width(imgui.calculate_item_width()/2.5*2)
        imgui.push_item_width(imgui.calculate_item_width())

        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, imgui.Vec2( 0, 1 ))
        lineHeight = 23.5

        imgui.push_style_color(imgui.COLOR_BUTTON, 0.8, 0.1, 0.15, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.9, 0.2, 0.2, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.8, 0.1, 0.15, 1.0 )
        if imgui.button("X", lineHeight + 3.0, lineHeight): values.x = resetValue
        imgui.pop_style_color(3)

        imgui.same_line()
        XHasChanged, XChanged = imgui.drag_float("##X", values.x, speed, 0.0, 0.0, format="%.2f")
        imgui.pop_item_width()
        imgui.same_line()

        imgui.push_style_color(imgui.COLOR_BUTTON, 0.2, 0.7, 0.2, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.3, 0.8, 0.3, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.2, 0.7, 0.2, 1.0 )
        if imgui.button("Y", lineHeight + 3.0, lineHeight): values.y = resetValue
        imgui.pop_style_color(3)

        imgui.same_line()
        YHasChanged, YChanged = imgui.drag_float("##Y", values.y, speed, 0.0, 0.0, format="%.2f")
        imgui.pop_item_width()
        imgui.same_line()

        imgui.push_style_color(imgui.COLOR_BUTTON, 0.1, 0.25, 0.8, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.2, 0.35, 0.9, 1.0 )
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.1, 0.25, 0.8, 1.0 )
        if imgui.button("Z", lineHeight + 3.0, lineHeight): values.z = resetValue
        imgui.pop_style_color(3)

        imgui.same_line()
        ZHasChanged, ZChanged = imgui.drag_float("##Z", values.z, speed, 0.0, 0.0, format="%.2f")
        imgui.pop_item_width()

        imgui.pop_style_var()
        imgui.columns(1)
        imgui.pop_id()

        if XHasChanged or YHasChanged or ZHasChanged: return True, pyrr.Vector3([ XChanged, YChanged, ZChanged ])
        else: return False, pyrr.Vector3([ values.x, values.y, values.z ])

    @staticmethod
    def DrawTextFieldControls(
        lable: str, value: str, columnWidth: float=50, acceptDragDrop: bool=False, filter: Tuple[str]=None
    ) -> Tuple[bool, str]:
        imgui.push_id(lable)

        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()
        
        imgui.push_item_width(imgui.calculate_item_width() * 1.5)
        changed, newText = imgui.input_text("##Filter", value, 512)
        imgui.pop_item_width()

        dragDrop = False
        if acceptDragDrop:
            if imgui.begin_drag_drop_target():
                data: bytes = imgui.accept_drag_drop_payload("CONTENT_BROWSER_ITEM")
                if data:
                    data = data.decode('utf-8')
                    if not filter: changed, newText, dragDrop = True, data, True
                    else:
                        if data.lower().endswith(filter): changed, newText, dragDrop = True, data, True
                        else: PI_CORE_WARN("This text field only accepts {} files", filter)
                imgui.end_drag_drop_target()

        imgui.columns(1)
        imgui.pop_id()

        return changed, newText, dragDrop

    @staticmethod
    def DrawTextLable(lable: str, value: str, columnWidth: float=50) -> None:
        imgui.push_id(lable)
        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()
        imgui.text(value)
        imgui.columns(1)
        imgui.pop_id()

    # Output -> ( changed, index, value )
    @staticmethod
    def DrawDropdown(lable: str, index: int, values: List[str], columnWidth: float=50) -> Tuple[bool, int, str]:
        imgui.push_id(lable)
        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()

        imgui.push_item_width(imgui.calculate_item_width() * 1.5)
        
        changed, index = imgui.combo("##lable", index, values)

        imgui.pop_item_width()

        imgui.columns(1)
        imgui.pop_id()

        return changed, index, values[index]

    @staticmethod
    def DrawFloatControls(
            lable: str, value: float, speed: float=0.05,
            minValue: float=0.0, maxValue: float=0.0,
            columnWidth: float=100
        ) -> Tuple[bool, float]:
        imgui.push_id(lable)
        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()
        
        changed, value = imgui.drag_float(
            "##Value", value, change_speed=speed, min_value=minValue, max_value=maxValue, format="%.2f"
        )
        
        imgui.columns(1)
        imgui.pop_id()

        return changed, value
        
    @staticmethod
    def DrawIntControls(lable: str, value: int, speed: float=0.05, columnWidth: float=100) -> Tuple[bool, int]:
        imgui.push_id(lable)
        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()
        changed, value = imgui.drag_int("##Value", value, change_speed=speed)
        imgui.columns(1)
        imgui.pop_id()

        return changed, value

    @staticmethod
    def DrawBoolControls(lable: str, state: bool, columnWidth: float=100) -> Tuple[bool, bool]:
        imgui.push_id(lable)
        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()
        changed, state = imgui.checkbox("##Value", state)
        imgui.columns(1)
        imgui.pop_id()

        return changed, state

    @staticmethod
    def DrawColor4Controls(lable: str, value: pyrr.Vector4, columnWidth: float=100) -> Tuple[bool, pyrr.Vector4]:
        imgui.push_id(lable)
        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()
        changed, value = imgui.color_edit4("##Value", value.x, value.y, value.z, value.w)
        imgui.columns(1)
        imgui.pop_id()

        return changed, value

    @staticmethod
    def DrawColor3Controls(lable: str, value: pyrr.Vector3, columnWidth: float=100) -> Tuple[bool, pyrr.Vector3]:
        imgui.push_id(lable)
        imgui.columns(2)
        imgui.set_column_width(0, columnWidth)
        imgui.text(lable)
        imgui.next_column()
        changed, value = imgui.color_edit3("##Value", value[0], value[1], value[2])
        imgui.columns(1)
        imgui.pop_id()

        return changed, value

    @staticmethod
    def DrawFileLoadDialog(filetypes=Iterable[Tuple[str, str]]) -> Tuple[bool, str]:
        UILib._FILE_DIALOGUE_RESOURCES.Init()
        fileName = UILib._FILE_DIALOGUE_RESOURCES.LoadFileLoader(filetypes=filetypes)
        return fileName == "", fileName
        
    @staticmethod
    def DrawFileSaveDialog(filetypes=Iterable[Tuple[str, str]]) -> Tuple[bool, str]:
        UILib._FILE_DIALOGUE_RESOURCES.Init()
        fileName = UILib._FILE_DIALOGUE_RESOURCES.SaveFileLoader(filetypes=filetypes)
        return fileName == "", fileName
