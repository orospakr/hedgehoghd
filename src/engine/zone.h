#ifndef __HHD_ENGINE_ZONE_H_
#define __HHD_ENGINE_ZONE_H_

#include <QVariantMap>

namespace HedgehogHD {
    namespace Engine {
        class Zone {
        public:
            Zone(QVariantMap json);
        private:
            QString code;
            QString title;
            
        };
    }
}

#endif
