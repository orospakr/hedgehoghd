#include <QtGui>

#include <QSvgRenderer>

#include <QImage>

int main(int argc, char** argv) {
    QApplication app(argc, argv);
    QImage woot((256 * 128) + (4 * 256), 4 + (128 * 2), QImage::Format_ARGB32);
    QSvgRenderer test(QLatin1String("/home/orospakr/hhd_test/collision.svg"), 0);
    QPainter painter(&woot);

    test.render(&painter);

    woot.save("/tmp/out.png", 0, -1);

    // 1. load an svg file
    // 2. get it inside a GraphicsView
    // 3. Get a Level Editor window up with that graphicsview in it
    // 4. Create first real HHD objects, start filing and loading SVGs
    //    from such normalized directory layout.  Change importer
    //    as necessary.
    // 5. Get all the chunks loaded, display list (separate GraphicsView or a single one?) of Chunks.
    // 5.5. Invent format for HHD's equivalent of the Chunk Array.  arbitrary size in X/Y/D (depth, or "path" layer) dims
    // 6. Display a graphicsview of an entire level.
    // 7. Show some UI for selecting different levels and acts, loading tabs.  Objs. as necessary.
    // 8. Add treeview/sidepane for selecting levels, acts.
    // 9. Create separate Qt Window (and maybe separate QApplication) as the first frontend
    // 10. Make that frontend get a simple thread rendering to a QGLWidget
    // 11. Render an SVG using Qt's stuff (think about abstracting, HHD engine should probably not depend on Qt),
    //     get int into a texture and in the QGLWidget, simple projection matrix.
    // 11. Create first Engine objects, have them use the same classes created
    //     for #4, #7.
    // 12. Place a level's worth of Chunks into GL scene. Milestone!

    // Basic skeleton would now be in place!

    // Editor's first mutation ability will probably be changing layout.  Not sure if SVG editing of chunks is feasible or even appropriate.
    // Should my chunks even be SVG?  Maybe I should want a limited path format.  Maybe a limited (enforced) version of SVG is appropriate?

    // Engine should begin having an actual timed loop -- process next frame, use differences from initial timestamp to figure out how much
    // to sleep until flipping the buffers and resuming anew
    // using this, get some basic input working and allow the user to move the the "viewport"/perspective matrix


    //return app.exec();
    return 0;
}
