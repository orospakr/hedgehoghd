#include <QApplication>

#include <editor_application.h>

#include <editor_window.h>

HedgehogHD::Editor::EditorApplication::EditorApplication(int & argc, char ** argv) : QApplication(argc, argv), mainWindow(new EditorWindow())
                                                                                    
{
    mainWindow->show();
}

int HedgehogHD::Editor::EditorApplication::run() {
    return exec();
}
