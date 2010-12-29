#ifndef __HHD_ENGINE_GAME_H_
#define __HHD_ENGINE_GAME_H_

#include <QVariantMap>
#include <QString>

#include "zone.h"
#include "chunk.h"

namespace HedgehogHD {
    namespace Engine {
        class Game {
        public:
            Game(const char* path);
            ~Game();
            
        private:
            QVariantMap game_json;
            QString path;
            QHash<QString, Zone*> zones;
            QHash<int, Chunk*> chunks;
            void loadChunks();
            void loadZones();
        };
    }
}

#endif
