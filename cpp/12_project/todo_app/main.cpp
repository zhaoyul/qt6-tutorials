/**
 * Simple Qt Widgets todo app demo
 */

#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLineEdit>
#include <QPushButton>
#include <QListWidget>
#include <QLabel>
#include <QStandardPaths>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QFile>
#include <QDir>

static QString dataFilePath()
{
    const QString dir = QStandardPaths::writableLocation(QStandardPaths::AppDataLocation);
    QDir().mkpath(dir);
    return dir + "/todos.json";
}

static void saveTasks(QListWidget *list)
{
    QJsonArray tasks;
    for (int i = 0; i < list->count(); ++i) {
        QListWidgetItem *item = list->item(i);
        QJsonObject obj;
        obj["text"] = item->text();
        obj["done"] = (item->checkState() == Qt::Checked);
        tasks.append(obj);
    }

    QFile file(dataFilePath());
    if (!file.open(QIODevice::WriteOnly | QIODevice::Truncate)) {
        return;
    }

    file.write(QJsonDocument(tasks).toJson(QJsonDocument::Compact));
}

static void loadTasks(QListWidget *list)
{
    QFile file(dataFilePath());
    if (!file.open(QIODevice::ReadOnly)) {
        return;
    }

    const QJsonDocument doc = QJsonDocument::fromJson(file.readAll());
    if (!doc.isArray()) {
        return;
    }

    list->blockSignals(true);
    const QJsonArray tasks = doc.array();
    for (const QJsonValue &value : tasks) {
        const QJsonObject obj = value.toObject();
        const QString text = obj.value("text").toString();
        const bool done = obj.value("done").toBool(false);

        auto *item = new QListWidgetItem(text, list);
        item->setFlags(item->flags() | Qt::ItemIsUserCheckable);
        item->setCheckState(done ? Qt::Checked : Qt::Unchecked);
        list->addItem(item);
    }
    list->blockSignals(false);
}

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    window.setWindowTitle("Todo App");
    window.resize(460, 520);

    auto *layout = new QVBoxLayout(&window);
    auto *title = new QLabel("Todo App");
    QFont titleFont = title->font();
    titleFont.setPointSize(16);
    titleFont.setBold(true);
    title->setFont(titleFont);

    auto *inputLayout = new QHBoxLayout();
    auto *input = new QLineEdit();
    input->setPlaceholderText("Add a task...");
    auto *addButton = new QPushButton("Add");
    inputLayout->addWidget(input);
    inputLayout->addWidget(addButton);

    auto *list = new QListWidget();
    auto *buttonRow = new QHBoxLayout();
    auto *removeButton = new QPushButton("Remove Selected");
    auto *clearButton = new QPushButton("Clear Completed");
    buttonRow->addWidget(removeButton);
    buttonRow->addWidget(clearButton);

    layout->addWidget(title);
    layout->addLayout(inputLayout);
    layout->addWidget(list);
    layout->addLayout(buttonRow);

    loadTasks(list);

    QObject::connect(addButton, &QPushButton::clicked, [&]() {
        const QString text = input->text().trimmed();
        if (text.isEmpty()) {
            return;
        }
        auto *item = new QListWidgetItem(text, list);
        item->setFlags(item->flags() | Qt::ItemIsUserCheckable);
        item->setCheckState(Qt::Unchecked);
        list->addItem(item);
        input->clear();
        input->setFocus();
        saveTasks(list);
    });

    QObject::connect(input, &QLineEdit::returnPressed, addButton, &QPushButton::click);

    QObject::connect(removeButton, &QPushButton::clicked, [&]() {
        const int row = list->currentRow();
        if (row < 0) {
            return;
        }
        delete list->takeItem(row);
        saveTasks(list);
    });

    QObject::connect(clearButton, &QPushButton::clicked, [&]() {
        for (int i = list->count() - 1; i >= 0; --i) {
            QListWidgetItem *item = list->item(i);
            if (item->checkState() == Qt::Checked) {
                delete list->takeItem(i);
            }
        }
        saveTasks(list);
    });

    QObject::connect(list, &QListWidget::itemChanged, [&]() {
        saveTasks(list);
    });

    window.show();
    return app.exec();
}
