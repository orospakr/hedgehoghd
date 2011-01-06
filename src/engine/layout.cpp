#include "layout.h"
#include "act.h"

#include <QDebug>
#include <QString>
#include <QStringList>

HedgehogHD::Engine::Layout::Layout(Act* act, QByteArray* csv_data) {
    // TODO ugh, too many copies.
    QString csv_str(*csv_data);
    QStringList csv_lines = csv_str.split("\n");
    QString line;
    // does this also make copies to line every time?  Pretty sure it does, ugh.  Can I use pointers?
    int loaded_rows = 0;
    foreach(line, csv_lines) {
        QStringList blocks = line.split(",");
        qDebug() << "Read line of length" << blocks.length();
        if(blocks.length() == 0) {
            continue;
        }
        if(blocks.length() != act->getWidth()) {
            qDebug() << "Row geometry does not match! (width:" << act->getWidth() << ", found:" << blocks.length();
            continue;
        }
        loaded_rows++;
        if(loaded_rows >= act->getHeight())
            break;
    }
    if(loaded_rows != act->getHeight()) {
        qDebug() << "Uh oh!  Didn't find enough lines in the layout file to satisfy the height (height:" << act->getHeight() << ", " << loaded_rows << ")";
    }
    qDebug() << "CSV lines loaded from map:" << loaded_rows;
}
