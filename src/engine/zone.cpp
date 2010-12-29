#include "zone.h"

#include <QDebug>

using HedgehogHD::Engine::Game;

HedgehogHD::Engine::Zone::Zone(Game* game, QVariantMap json) {
    this->code = json["code"].toString();
    this->title = json["title"].toString();

    qDebug() << "Loaded Zone: " << this->code;
}
