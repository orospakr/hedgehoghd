#ifndef __HHD_ENGINE_ZONE_H_
#define __HHD_ENGINE_ZONE_H_

#include <QVariantMap>

#include "act.h"

namespace HedgehogHD {
    namespace Engine {
        // forward declaration of Game to avoid circular
        // dependency.
        class Game;

        class Zone {
        public:
            Zone(Game* game, QVariantMap json);
        private:
            QString code;
            QString title;
            Game* game;
            QList<Act> acts;
        };
    }
}

#endif
