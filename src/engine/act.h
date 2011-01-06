#ifndef _HHD_ENGINE_ACT_H_
#define _HHD_ENGINE_ACT_H_

#include <QByteArray>
#include <QVariantMap>


namespace HedgehogHD {
    namespace Engine {
        class Zone;
        class Act {
        public:
            Act(Zone* zone, const QVariantMap& json, int number);
            int getWidth();
            int getHeight();
        private:
            Zone* zone;
            int number;
            int width;
            int height;
        };
    }
}

#endif
