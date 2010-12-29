#include <QVariant>

#include <QDebug>

#include <QFile>

#include <iostream>

#include "qjson/parser.h"

#include "game.h"

HedgehogHD::Engine::Game::Game(const char* path) {
    bool ok;
    QJson::Parser parser;

    this->path = QString(path);

    qDebug() << "Loading HHD game from:" << this->path;
    
    QFile json_file(path);
    if(!json_file.open(QIODevice::ReadOnly)) {
      std::cout << "Problem reading from game JSON!";
    }

    QByteArray json_data = json_file.readAll();

    game_json = parser.parse(json_data, &ok).toMap();
    
    if(ok) {
      std::cout << "Success!\n";
    } else {
        std::cout << "Failed to parse game.json!  Have I been pointed at a valid path?\n";
    }
    qDebug() << "Loaded Game:" << game_json["title"].toString();
    if(!(game_json["zones"]).canConvert<QVariantList>()) {
        qDebug() << "Oh shit this won't work!";
    }
    QVariantList zone_json_list = game_json["zones"].toList();
    QVariant item;
    foreach(item, zone_json_list) {
        Zone *zm = new Zone(item.toMap());
        this->zones << zm;
    }
}

HedgehogHD::Engine::Game::~Game() {
    Zone *z;
    foreach(z, this->zones) {
        delete z;
    };
    this->zones.clear();
}
