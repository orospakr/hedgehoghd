#include <QVariant>

#include <QDebug>
#include <QDir>
#include <QIODevice>
#include <QFile>

#include <iostream>

#include "qjson/parser.h"

#include "game.h"
#include "chunk.h"

HedgehogHD::Engine::Game::Game(const char* path_) {
    bool ok;
    QJson::Parser parser;

    this->path = QDir(QString(path_));

    qDebug() << "Loading HHD game from:" << this->path.path();
    
    QFile json_file(this->path.absoluteFilePath("game.json"));
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
    loadZones();
    loadChunks();
}

QDir HedgehogHD::Engine::Game::zonesPath() {
    return path.absoluteFilePath("zones");
}

QDir HedgehogHD::Engine::Game::chunksPath() {
    return path.absoluteFilePath("chunks");
}

void HedgehogHD::Engine::Game::loadZones() {
    if(!(game_json["zones"]).canConvert<QVariantList>()) {
        qDebug() << "Can't coerce 'zones' field of JSON into list!";
    }
    QVariantList zone_json_list = game_json["zones"].toList();
    QVariant item;
    foreach(item, zone_json_list) {
        QVariantMap map = item.toMap();
        Zone *zm = new Zone(this, map);
        this->zones[map["code"].toString()] = zm;
    }
}

void HedgehogHD::Engine::Game::loadChunks() {
    if(!(game_json["chunks"]).canConvert<QVariantList>()) {
        qDebug() << "Can't coerce 'chunks' field of JSON into list!";
    }
    QVariantList chunk_json_list = game_json["chunks"].toList();
    QVariant item;
    foreach(item, chunk_json_list) {
        QVariantMap map = item.toMap();
        Chunk *c = new Chunk(map);
        this->chunks[map["id"].toInt()] = c;
    }
}

HedgehogHD::Engine::Game::~Game() {
    Zone *z;
    foreach(z, this->zones) {
        delete z;
    };
    Chunk *c;
    foreach(c, this->chunks) {
        delete c;
    }
    this->zones.clear();
}
