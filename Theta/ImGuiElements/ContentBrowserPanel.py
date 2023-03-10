from PI import *

import pathlib
import os

class ContentBrowserPanel:
    __Project: Project

    __CurrentDirectory: pathlib.Path
    __LastDirectory: pathlib.Path

    __DirectoryIcon: Texture2D = None
    __FileIcon: Texture2D = None

    __AdditionalImages: Dict[str, Texture2D]

    def __init__(self, project: Project) -> None:
        self.__Project = project
        
        self.__CurrentDirectory = project.AssetsLocation
        self.__LastDirectory = project.AssetsLocation

        try:
            self.__DirectoryIcon = Texture2D.Create(".\\Theta\\Resources\\Icons\\ContentBrowser\\DirectoryIcon.png")
            self.__FileIcon      = Texture2D.Create(".\\Theta\\Resources\\Icons\\ContentBrowser\\FileIcon.png")

        # This is here for Building
        # 'cause the Build looks for files in '.'
        except FileNotFoundError:
            self.__DirectoryIcon = Texture2D.Create(".\\Resources\\Icons\\ContentBrowser\\DirectoryIcon.png")
            self.__FileIcon      = Texture2D.Create(".\\Resources\\Icons\\ContentBrowser\\FileIcon.png")

        self.__AdditionalImages = {}

    def SetProject(self, project: Project) -> None:
        self.__Project = project
        
        self.__CurrentDirectory = project.AssetsLocation
        self.__LastDirectory = project.AssetsLocation

    def __GetImage(self, filename) -> Texture2D:
        image = self.__AdditionalImages.get(filename, None)
        if not image:
            image = Texture2D.Create(filename)
            self.__AdditionalImages[filename] = image

        return image

    def OnImGuiRender(self) -> None:
        imgui.begin("Content Browser")

        if self.__CurrentDirectory != self.__Project.AssetsLocation:
            if imgui.button("<-"):
                self.__LastDirectory = self.__CurrentDirectory
                self.__CurrentDirectory = self.__CurrentDirectory.parent
        
        imgui.same_line()
        if imgui.button("->"):
            self.__CurrentDirectory = self.__LastDirectory
            self.__LastDirectory = self.__CurrentDirectory.parent \
                if self.__CurrentDirectory != self.__Project.AssetsLocation else self.__Project.AssetsLocation

        padding: float = 8.0
        thumbnailSize: float = 64
        cellSize: float = thumbnailSize + padding

        panelWidth = imgui.get_content_region_available()[0]
        columnCount = int(panelWidth / cellSize)
        if columnCount < 1: columnCount = 1

        imgui.columns(columnCount, border=False)

        for path in os.listdir(self.__CurrentDirectory.absolute()):
            path = self.__CurrentDirectory / pathlib.Path(path)
            relativePath = str(path.relative_to(self.__CurrentDirectory))

            if relativePath == "__pycache__": continue
            if not PI_DEBUG and relativePath == "Internal": continue

            imgui.push_id(str(path))

            icon = self.__DirectoryIcon if path.is_dir() else None

            if not icon and path.suffix in (".png", ".jpg"):icon = self.__GetImage(str(path))
            elif not icon: icon = self.__FileIcon

            imgui.push_style_color(imgui.COLOR_BUTTON, 0, 0, 0, 0)
            imgui.image_button(icon.RendererID, thumbnailSize, thumbnailSize, (0, 1), (1, 0))
            imgui.pop_style_color()

            if imgui.begin_drag_drop_source():
                imgui.set_drag_drop_payload("CONTENT_BROWSER_ITEM", str(path).encode('UTF-8'))
                imgui.end_drag_drop_source()

            if imgui.is_item_hovered() and imgui.is_mouse_double_clicked(imgui.MOUSE_BUTTON_LEFT) and path.is_dir():
                self.__CurrentDirectory = path

            imgui.pop_id()
            MAX_DISPLAY_LEN: int = 15
            if len(relativePath) > MAX_DISPLAY_LEN: relativePath = relativePath[:MAX_DISPLAY_LEN] + "..."
            imgui.text_wrapped(relativePath)
            imgui.next_column()

        imgui.columns(1)
        imgui.end()
