/**
 * Qt6 图形视图框架示例
 *
 * Graphics View Framework 用于管理大量2D图形项：
 * - QGraphicsScene: 场景 (管理所有图形项)
 * - QGraphicsView: 视图 (显示场景)
 * - QGraphicsItem: 图形项基类
 *
 * 内置图形项：
 * - QGraphicsRectItem, QGraphicsEllipseItem
 * - QGraphicsLineItem, QGraphicsPathItem
 * - QGraphicsTextItem, QGraphicsPixmapItem
 *
 * 官方文档: https://doc.qt.io/qt-6/graphicsview.html
 */

#include <QApplication>
#include <QMainWindow>
#include <QGraphicsScene>
#include <QGraphicsView>
#include <QGraphicsRectItem>
#include <QGraphicsEllipseItem>
#include <QGraphicsLineItem>
#include <QGraphicsTextItem>
#include <QGraphicsPathItem>
#include <QGraphicsItemGroup>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QPushButton>
#include <QSlider>
#include <QLabel>
#include <QToolBar>
#include <QWheelEvent>
#include <QRandomGenerator>
#include <QDebug>

// 自定义可拖动图形项
class DraggableRect : public QGraphicsRectItem
{
public:
    DraggableRect(qreal x, qreal y, qreal w, qreal h, QGraphicsItem *parent = nullptr)
        : QGraphicsRectItem(x, y, w, h, parent)
    {
        setFlag(QGraphicsItem::ItemIsMovable);
        setFlag(QGraphicsItem::ItemIsSelectable);
        setFlag(QGraphicsItem::ItemSendsGeometryChanges);
        setAcceptHoverEvents(true);
    }

protected:
    void hoverEnterEvent(QGraphicsSceneHoverEvent *event) override
    {
        setBrush(QBrush(QColor(255, 200, 200)));
        QGraphicsRectItem::hoverEnterEvent(event);
    }

    void hoverLeaveEvent(QGraphicsSceneHoverEvent *event) override
    {
        setBrush(QBrush(QColor(200, 200, 255)));
        QGraphicsRectItem::hoverLeaveEvent(event);
    }

    QVariant itemChange(GraphicsItemChange change, const QVariant &value) override
    {
        if (change == ItemPositionChange) {
            qDebug() << "位置变化:" << value.toPointF();
        }
        return QGraphicsRectItem::itemChange(change, value);
    }
};

// 自定义视图 (支持缩放)
class ZoomableView : public QGraphicsView
{
public:
    explicit ZoomableView(QGraphicsScene *scene, QWidget *parent = nullptr)
        : QGraphicsView(scene, parent), m_scaleFactor(1.0)
    {
        setRenderHint(QPainter::Antialiasing);
        setDragMode(QGraphicsView::RubberBandDrag);
        setTransformationAnchor(QGraphicsView::AnchorUnderMouse);
    }

    void zoomIn() { scale(1.2, 1.2); m_scaleFactor *= 1.2; }
    void zoomOut() { scale(1/1.2, 1/1.2); m_scaleFactor /= 1.2; }
    void resetZoom() { resetTransform(); m_scaleFactor = 1.0; }

protected:
    void wheelEvent(QWheelEvent *event) override
    {
        if (event->modifiers() & Qt::ControlModifier) {
            if (event->angleDelta().y() > 0) {
                zoomIn();
            } else {
                zoomOut();
            }
            event->accept();
        } else {
            QGraphicsView::wheelEvent(event);
        }
    }

private:
    qreal m_scaleFactor;
};

class GraphicsViewDemo : public QMainWindow
{
    Q_OBJECT

public:
    explicit GraphicsViewDemo(QWidget *parent = nullptr)
        : QMainWindow(parent)
    {
        setWindowTitle("Qt6 Graphics View Demo");
        resize(800, 600);

        // 创建场景
        m_scene = new QGraphicsScene(-400, -300, 800, 600, this);
        m_scene->setBackgroundBrush(QBrush(QColor(240, 240, 240)));

        // 创建视图
        m_view = new ZoomableView(m_scene, this);
        setCentralWidget(m_view);

        // 添加图形项
        createGraphicsItems();

        // 创建工具栏
        createToolBar();
    }

private slots:
    void addRectangle()
    {
        DraggableRect *rect = new DraggableRect(
            QRandomGenerator::global()->bounded(100) - 50,
            QRandomGenerator::global()->bounded(100) - 50,
            80, 60);
        rect->setPen(QPen(Qt::black, 2));
        rect->setBrush(QBrush(QColor(200, 200, 255)));
        m_scene->addItem(rect);
    }

    void addEllipse()
    {
        QGraphicsEllipseItem *ellipse = m_scene->addEllipse(
            QRandomGenerator::global()->bounded(80) - 40,
            QRandomGenerator::global()->bounded(80) - 40,
            70, 50,
            QPen(Qt::darkGreen, 2),
            QBrush(QColor(200, 255, 200))
        );
        ellipse->setFlag(QGraphicsItem::ItemIsMovable);
        ellipse->setFlag(QGraphicsItem::ItemIsSelectable);
    }

    void addText()
    {
        QGraphicsTextItem *text = m_scene->addText("Qt6 Graphics",
            QFont("Arial", 16, QFont::Bold));
        text->setPos(QRandomGenerator::global()->bounded(100) - 50,
                     QRandomGenerator::global()->bounded(100) - 50);
        text->setDefaultTextColor(Qt::darkBlue);
        text->setFlag(QGraphicsItem::ItemIsMovable);
        text->setFlag(QGraphicsItem::ItemIsSelectable);
    }

    void deleteSelected()
    {
        for (QGraphicsItem *item : m_scene->selectedItems()) {
            m_scene->removeItem(item);
            delete item;
        }
    }

    void clearAll()
    {
        m_scene->clear();
        createGraphicsItems();  // 重新创建初始项目
    }

private:
    void createGraphicsItems()
    {
        // 矩形
        QGraphicsRectItem *rect = m_scene->addRect(-200, -150, 100, 80,
            QPen(Qt::blue, 2), QBrush(Qt::cyan));
        rect->setFlag(QGraphicsItem::ItemIsMovable);
        rect->setFlag(QGraphicsItem::ItemIsSelectable);
        rect->setToolTip("矩形 (可拖动)");

        // 椭圆
        QGraphicsEllipseItem *ellipse = m_scene->addEllipse(-50, -150, 100, 80,
            QPen(Qt::darkGreen, 2), QBrush(Qt::green));
        ellipse->setFlag(QGraphicsItem::ItemIsMovable);
        ellipse->setFlag(QGraphicsItem::ItemIsSelectable);
        ellipse->setToolTip("椭圆");

        // 线条
        QGraphicsLineItem *line = m_scene->addLine(100, -150, 200, -70,
            QPen(Qt::red, 3));
        line->setFlag(QGraphicsItem::ItemIsMovable);
        line->setFlag(QGraphicsItem::ItemIsSelectable);
        line->setToolTip("线条");

        // 文本
        QGraphicsTextItem *text = m_scene->addText("Qt6 Graphics View",
            QFont("Arial", 20, QFont::Bold));
        text->setPos(-100, 50);
        text->setDefaultTextColor(Qt::darkMagenta);
        text->setFlag(QGraphicsItem::ItemIsMovable);
        text->setToolTip("文本项");

        // 路径 (星形)
        QPainterPath starPath;
        for (int i = 0; i < 5; ++i) {
            double angle = i * 72 * M_PI / 180 - M_PI / 2;
            QPointF p(30 * cos(angle), 30 * sin(angle));
            if (i == 0)
                starPath.moveTo(p);
            else
                starPath.lineTo(p);
        }
        starPath.closeSubpath();

        QGraphicsPathItem *star = m_scene->addPath(starPath,
            QPen(Qt::darkYellow, 2), QBrush(Qt::yellow));
        star->setPos(-200, 100);
        star->setFlag(QGraphicsItem::ItemIsMovable);
        star->setFlag(QGraphicsItem::ItemIsSelectable);
        star->setToolTip("星形路径");

        // 自定义可拖动矩形
        DraggableRect *draggable = new DraggableRect(100, 50, 100, 80);
        draggable->setPen(QPen(Qt::black, 2));
        draggable->setBrush(QBrush(QColor(200, 200, 255)));
        draggable->setToolTip("悬停变色的矩形");
        m_scene->addItem(draggable);

        // 图形组
        QGraphicsItemGroup *group = new QGraphicsItemGroup;
        QGraphicsRectItem *groupRect = new QGraphicsRectItem(-20, -15, 40, 30);
        groupRect->setBrush(Qt::lightGray);
        QGraphicsEllipseItem *groupEllipse = new QGraphicsEllipseItem(-10, -10, 20, 20);
        groupEllipse->setBrush(Qt::darkGray);
        group->addToGroup(groupRect);
        group->addToGroup(groupEllipse);
        group->setPos(0, -50);
        group->setFlag(QGraphicsItem::ItemIsMovable);
        group->setFlag(QGraphicsItem::ItemIsSelectable);
        group->setToolTip("图形组 (一起移动)");
        m_scene->addItem(group);

        // 说明文本
        QGraphicsTextItem *info = m_scene->addText(
            "操作说明:\n"
            "• 拖动图形项移动\n"
            "• Ctrl+滚轮缩放\n"
            "• 点击选择，拖动框选\n"
            "• 使用工具栏按钮添加/删除",
            QFont("Arial", 10));
        info->setPos(-380, 150);
    }

    void createToolBar()
    {
        QToolBar *toolBar = addToolBar("工具");

        toolBar->addAction("添加矩形", this, &GraphicsViewDemo::addRectangle);
        toolBar->addAction("添加椭圆", this, &GraphicsViewDemo::addEllipse);
        toolBar->addAction("添加文本", this, &GraphicsViewDemo::addText);
        toolBar->addSeparator();
        toolBar->addAction("删除选中", this, &GraphicsViewDemo::deleteSelected);
        toolBar->addAction("清空", this, &GraphicsViewDemo::clearAll);
        toolBar->addSeparator();
        toolBar->addAction("放大", m_view, &ZoomableView::zoomIn);
        toolBar->addAction("缩小", m_view, &ZoomableView::zoomOut);
        toolBar->addAction("重置", m_view, &ZoomableView::resetZoom);
    }

    QGraphicsScene *m_scene;
    ZoomableView *m_view;
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    qDebug() << "=== Qt6 图形视图框架示例 ===\n";
    qDebug() << "功能:";
    qDebug() << "- 拖动图形项移动";
    qDebug() << "- Ctrl+滚轮缩放视图";
    qDebug() << "- 点击选择，拖动框选多个";
    qDebug() << "- 工具栏添加/删除图形项\n";

    GraphicsViewDemo demo;
    demo.show();

    return app.exec();
}

#include "main.moc"
