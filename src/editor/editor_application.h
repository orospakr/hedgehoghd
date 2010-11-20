#ifndef _HHD_EDITOR_APPLICATION_H_
#define _HHD_EDITOR_APPLICATION_H_

#include <QApplication>

#include <editor_window.h>

namespace HedgehogHD {
    namespace Editor {
        class EditorApplication : public QApplication {
            Q_OBJECT
            
        public:
            EditorApplication(int & argc, char ** argv);
	    
	    int run();
            
        private:
            int weenis;
            QObject woorea;

	    EditorWindow *mainWindow;
        };
    }
}

#endif
