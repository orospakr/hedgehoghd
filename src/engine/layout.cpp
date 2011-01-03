#include "layout.h"
#include "act.h"

#include <QDebug>
#include <QString>
#include <QStringList>

HedgehogHD::Engine::Layout::Layout(Act* act, QByteArray* csv_data) {
    // TODO ugh, too many copies.
    QString csv_str(*csv_data);
    QStringList csv_lines = csv_str.split("\n");
    qDebug() << "CSV lines loaded from map:" << csv_lines.length();
}
