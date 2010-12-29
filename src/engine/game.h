#ifndef __HHD_ENGINE_GAME_H_
#define __HHD_ENGINE_GAME_H_

#include <QVariantMap>
#include <QString>

#include "zone.h"

namespace HedgehogHD {
    namespace Engine {
        class Game {
        public:
            Game(const char* path);
            ~Game();
            
        private:
            QVariantMap game_json;
            QString path;
            QList<Zone*> zones;
        };
    }
}

#endif
