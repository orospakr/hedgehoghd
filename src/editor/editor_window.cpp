#include <QtGui>

#include <editor_window.h>

HedgehogHD::Editor::EditorWindow::EditorWindow() : levelScene(new QGraphicsScene())  {
    // QPixmap thinger(
    QPixmap *thinger = new QPixmap("/home/orospakr/hhd_test2/chunk/ARZ/0b.svg", 0, Qt::AutoColor);
    levelDisplay = new QGraphicsView(levelScene);

    // const QPixmap& thingerMap(*thinger);
    
    QGraphicsPixmapItem * thingerItem = new QGraphicsPixmapItem(*thinger, 0, levelScene);
    QGraphicsPixmapItem * thingerItem2 = new QGraphicsPixmapItem(*thinger, 0, levelScene);
    thingerItem->setPos(0, 0);
    thingerItem2->setPos(128, 0);
    this->setCentralWidget(levelDisplay);

    // add(levelDisplay);

    // QPlainTextEdit widget(QString("HWLLOW"));
    // setCentralWidget(&widget);
    // widget.show();
    // QMessageBox::warning(this, tr("Application"),
    //                      tr("... is launching!"));
    // resize(QSize(400, 400));
    // showFullScreen();
}
