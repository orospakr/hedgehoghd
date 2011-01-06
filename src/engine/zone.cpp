#include "zone.h"

#include "game.h"

#include <QDebug>
#include <QFile>
#include <QIODevice>

using HedgehogHD::Engine::Game;

HedgehogHD::Engine::Zone::Zone(Game* game, QVariantMap json) {
    this->code = json["code"].toString();
    this->title = json["title"].toString();
    this->game = game;

    QVariantList acts_json = json["acts"].toList();
    QVariant act_json;
    int act_no = 0;
    foreach(act_json, acts_json) {
        if(!act_json.canConvert<QVariantMap>()) {
            qDebug() << "Can't coerce Act JSON into map!";
        }
        acts << new Act(this, act_json.toMap(), act_no);
    }

    qDebug() << "Loaded Zone:" << this->code << "," << this->title << ", which has" << acts.length() << "acts.";
}

Game* HedgehogHD::Engine::Zone::getGame() {
    return game;
}

QDir HedgehogHD::Engine::Zone::path() {
    return QDir(game->zonesPath()).absoluteFilePath(this->code);
}
