#include <QtGui>

#include <editor_window.h>
#include <game.h>

HedgehogHD::Editor::EditorWindow::EditorWindow() : levelScene(new QGraphicsScene())  {
    HedgehogHD::Engine::Game pingas("/home/orospakr/code/mine/hedgehoghd/scratch/hhd_s2_current/game.json");
    QPixmap *thinger = new QPixmap("/home/orospakr/hhd_test2/chunk/ARZ/0b.svg", 0, Qt::AutoColor);
    levelDisplay = new QGraphicsView(levelScene);

    QGraphicsPixmapItem * thingerItem = new QGraphicsPixmapItem(*thinger, 0, levelScene);
    QGraphicsPixmapItem * thingerItem2 = new QGraphicsPixmapItem(*thinger, 0, levelScene);
    thingerItem->setPos(0, 0);
    thingerItem2->setPos(128, 0);
    this->setCentralWidget(levelDisplay);
}
