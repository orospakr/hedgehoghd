#ifndef _HHD_ENGINE_ACT_H_
#define _HHD_ENGINE_ACT_H_

#include <QByteArray>


namespace HedgehogHD {
    namespace Engine {
        class Zone;
        class Act {
        public:
            Act(Zone* zone, int number);
        private:
            Zone* zone;
            int number;
        };
    }
}

#endif
