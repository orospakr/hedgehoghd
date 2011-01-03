#ifndef _HHD_ENGINE_LAYOUT_H_
#define _HHD_ENGINE_LAYOUT_H_

#include <QByteArray>

namespace HedgehogHD {
    namespace Engine {
        class Act;
        class Layout {

        public:
            Layout(Act* act, QByteArray* csv_data);
        };
    }
}

#endif
