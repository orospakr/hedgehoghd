#include <QDebug>
#include <QString>
#include <QStringList>

#include "act.h"
#include "zone.h"
#include "game.h"
#include "layout.h"

HedgehogHD::Engine::Act::Act(Zone* zone, const QVariantMap& json, int number) {
    this->zone = zone;
    this->number = number;
    width = json["width"].toInt();
    height = json["height"].toInt();
    QDir map_dir = zone->path().absoluteFilePath(QString("%1").arg(number));
    QString map_path(map_dir.absoluteFilePath("0.map"));
    // using QIODevice::Text here so I don't have to worry about funky
    // line endings in my CSV "parser", since QtCore will take care of it
    // for me.
    QFile map_fd(map_path);
    if(!map_fd.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qDebug() << "Argh!  Unable to open map file for act #" << number << ", path: " << map_path << ", error:" << map_fd.errorString();
    }
    QByteArray map_data = map_fd.readAll();
    Layout l(this, &map_data);
}

int HedgehogHD::Engine::Act::getHeight() {
    return height;
}

int HedgehogHD::Engine::Act::getWidth() {
    return width;
}
