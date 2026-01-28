/**
 * Qt6 3D basics demo
 */

#include <QGuiApplication>
#include <Qt3DExtras/Qt3DWindow>
#include <Qt3DCore/QEntity>
#include <Qt3DExtras/QSphereMesh>
#include <Qt3DExtras/QPhongMaterial>
#include <Qt3DExtras/QForwardRenderer>
#include <Qt3DRender/QCamera>
#include <Qt3DRender/QPointLight>
#include <Qt3DExtras/QOrbitCameraController>
#include <Qt3DCore/QTransform>
#include <QPropertyAnimation>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    Qt3DExtras::Qt3DWindow view;
    view.setTitle("Qt 3D Basics");
    view.defaultFrameGraph()->setClearColor(QColor(30, 30, 40));

    auto *root = new Qt3DCore::QEntity();

    // Camera setup
    Qt3DRender::QCamera *camera = view.camera();
    camera->lens()->setPerspectiveProjection(45.0f, 16.0f / 9.0f, 0.1f, 1000.0f);
    camera->setPosition(QVector3D(0.0f, 0.0f, 10.0f));
    camera->setViewCenter(QVector3D(0.0f, 0.0f, 0.0f));

    auto *camController = new Qt3DExtras::QOrbitCameraController(root);
    camController->setCamera(camera);

    // Sphere entity
    auto *sphere = new Qt3DCore::QEntity(root);
    auto *mesh = new Qt3DExtras::QSphereMesh();
    mesh->setRadius(1.5f);

    auto *material = new Qt3DExtras::QPhongMaterial();
    material->setDiffuse(QColor(0, 170, 255));
    material->setSpecular(QColor(255, 255, 255));
    material->setShininess(80.0f);

    auto *transform = new Qt3DCore::QTransform();

    sphere->addComponent(mesh);
    sphere->addComponent(material);
    sphere->addComponent(transform);

    // Simple light
    auto *lightEntity = new Qt3DCore::QEntity(root);
    auto *light = new Qt3DRender::QPointLight(lightEntity);
    light->setColor(QColor(255, 255, 255));
    light->setIntensity(1.0f);
    auto *lightTransform = new Qt3DCore::QTransform(lightEntity);
    lightTransform->setTranslation(QVector3D(6.0f, 6.0f, 6.0f));
    lightEntity->addComponent(light);
    lightEntity->addComponent(lightTransform);

    // Rotation animation
    auto *spin = new QPropertyAnimation(transform, "rotation");
    spin->setStartValue(QQuaternion::fromAxisAndAngle(QVector3D(0.0f, 1.0f, 0.0f), 0.0f));
    spin->setEndValue(QQuaternion::fromAxisAndAngle(QVector3D(0.0f, 1.0f, 0.0f), 360.0f));
    spin->setDuration(6000);
    spin->setLoopCount(-1);
    spin->start();

    view.setRootEntity(root);
    view.resize(800, 600);
    view.show();

    return app.exec();
}
