#ifndef _HHD_EDITOR_WINDOW_H_
#define _HHD_EDITOR_WINDOW_H_

#include <QMainWindow>
#include <QGraphicsView>
#include <QGraphicsScene>
#include <QBoxLayout>

namespace HedgehogHD {
    namespace Editor {
        class EditorWindow : public QMainWindow {
	  Q_OBJECT
	  
	public:
	  EditorWindow();

	private:
	  QGraphicsView *levelDisplay;
	  QGraphicsScene *levelScene;
        };
    }
}

#endif
