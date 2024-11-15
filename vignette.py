from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSystemTrayIcon,
    QMenu,
    QWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QIcon, QLinearGradient
import sys


class VignetteOverlay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_tray()
        self.opacity = 0.7  # Initial opacity value

    def setup_window(self):
        # Set up the main window properties
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowTransparentForInput
            | Qt.WindowType.NoDropShadowWindowHint
            | Qt.WindowType.MaximizeUsingFullscreenGeometryHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WidgetAttribute.WA_MacAlwaysShowToolWindow)

        # Get primary screen geometry
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        # Create central widget
        central_widget = QWidget()
        central_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setCentralWidget(central_widget)

    def setup_tray(self):
        # Create system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon.fromTheme("display"))

        # Create tray menu
        tray_menu = QMenu()

        # Add opacity controls
        increase_opacity = tray_menu.addAction("Increase Opacity")
        decrease_opacity = tray_menu.addAction("Decrease Opacity")
        increase_opacity.triggered.connect(lambda: self.adjust_opacity(0.2))
        decrease_opacity.triggered.connect(lambda: self.adjust_opacity(-0.2))

        # Add quit option
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(QApplication.quit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def adjust_opacity(self, delta):
        self.opacity = max(0.0, min(1.0, self.opacity + delta))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Get dimensions
        width = self.width()
        height = self.height()

        # Create gradients for each edge
        left = QLinearGradient(0, height / 2, width * 0.35, height / 2)
        right = QLinearGradient(width, height / 2, width * 0.65, height / 2)
        top = QLinearGradient(width / 2, 0, width / 2, height * 0.35)
        bottom = QLinearGradient(width / 2, height, width / 2, height * 0.65)

        # Set up gradient colors
        for gradient in [left, right, top, bottom]:
            gradient.setColorAt(
                0.0, QColor(0, 0, 0, int(self.opacity * 255))
            )  # Full opacity at edge
            gradient.setColorAt(
                0.7, QColor(0, 0, 0, int(self.opacity * 255 * 0.3))
            )  # Fade
            gradient.setColorAt(1.0, QColor(0, 0, 0, 0))  # Transparent toward center

        # Paint each gradient
        painter.fillRect(0, 0, width, height, left)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        painter.fillRect(0, 0, width, height, right)
        painter.fillRect(0, 0, width, height, top)
        painter.fillRect(0, 0, width, height, bottom)


def main():
    app = QApplication(sys.argv)

    # Create and show the vignette overlay
    vignette = VignetteOverlay()
    vignette.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
