#include "zone.h"

#include "game.h"

#include <QDebug>
#include <QFile>
#include <QIODevice>

using HedgehogHD::Engine::Game;

HedgehogHD::Engine::Zone::Zone(Game* game, QVariantMap json) {
    this->code = json["code"].toString();
    this->title = json["title"].toString();

    int num_of_acts = json["acts"].toInt();

    qDebug() << "Loaded Zone:" << this->code << "," << this->title << ", which has" << num_of_acts << "acts.";

    for(int a = 0; a < num_of_acts; a++) {
        acts << new Act(this, a);
    }
}

Game* HedgehogHD::Engine::Zone::getGame() {
    return game;
}

QDir HedgehogHD::Engine::Zone::path() {
    return QDir(game->zonesPath()).absoluteFilePath(this->code);
}
