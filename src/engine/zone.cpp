#include "zone.h"

#include <QDebug>

HedgehogHD::Engine::Zone::Zone(QVariantMap json) {
    this->code = json["code"].toString();
    this->title = json["title"].toString();
    qDebug() << "Loaded Zone: " << this->code;
}
