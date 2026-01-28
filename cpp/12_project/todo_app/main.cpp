/**
 * Qt Widgets todo app demo
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
#include <QDateTime>
#include <QInputDialog>
#include <QButtonGroup>
#include <QComboBox>

static QString dataFilePath()
{
    const QString dir = QStandardPaths::writableLocation(QStandardPaths::AppDataLocation);
    QDir().mkpath(dir);
    return dir + "/todos.json";
}

static QString priorityColor(const QString &priority)
{
    if (priority == "High") {
        return "#ef4444";
    }
    if (priority == "Medium") {
        return "#f59e0b";
    }
    if (priority == "Low") {
        return "#10b981";
    }
    return "#9ca3af";
}

static void saveTasks(QListWidget *list)
{
    QJsonArray tasks;
    for (int i = 0; i < list->count(); ++i) {
        QListWidgetItem *item = list->item(i);
        QJsonObject obj;
        obj["text"] = item->text();
        obj["done"] = (item->checkState() == Qt::Checked);
        obj["createdAt"] = item->data(Qt::UserRole).toString();
        obj["priority"] = item->data(Qt::UserRole + 1).toString();
        obj["tag"] = item->data(Qt::UserRole + 2).toString();
        tasks.append(obj);
    }

    QFile file(dataFilePath());
    if (!file.open(QIODevice::WriteOnly | QIODevice::Truncate)) {
        return;
    }

    file.write(QJsonDocument(tasks).toJson(QJsonDocument::Compact));
}

static void updateItemLabel(QListWidgetItem *item)
{
    const QString base = item->data(Qt::UserRole + 3).toString();
    const QString priority = item->data(Qt::UserRole + 1).toString();
    const QString tag = item->data(Qt::UserRole + 2).toString();

    QString suffix = QString(" [%1]").arg(priority);
    if (!tag.isEmpty()) {
        suffix += QString(" #%1").arg(tag);
    }

    item->setText(base + suffix);
    item->setForeground(QColor(priorityColor(priority)));
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

    const QJsonArray tasks = doc.array();
    for (const QJsonValue &value : tasks) {
        const QJsonObject obj = value.toObject();
        const QString rawText = obj.value("text").toString();
        const bool done = obj.value("done").toBool(false);
        const QString createdAt = obj.value("createdAt").toString();
        const QString priority = obj.value("priority").toString("Medium");
        const QString tag = obj.value("tag").toString();

        auto *item = new QListWidgetItem(rawText, list);
        item->setFlags(item->flags() | Qt::ItemIsUserCheckable | Qt::ItemIsEditable);
        item->setCheckState(done ? Qt::Checked : Qt::Unchecked);
        item->setData(Qt::UserRole, createdAt);
        item->setData(Qt::UserRole + 1, priority);
        item->setData(Qt::UserRole + 2, tag);
        item->setData(Qt::UserRole + 3, rawText);
        updateItemLabel(item);
        list->addItem(item);
    }
}

enum class FilterMode {
    All,
    Active,
    Done
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    app.setStyle("Fusion");

    QPalette palette = app.palette();
    palette.setColor(QPalette::Window, QColor(245, 247, 250));
    palette.setColor(QPalette::Base, Qt::white);
    palette.setColor(QPalette::Button, QColor(238, 242, 246));
    palette.setColor(QPalette::Highlight, QColor(47, 111, 237));
    palette.setColor(QPalette::HighlightedText, Qt::white);
    app.setPalette(palette);

    QWidget window;
    window.setWindowTitle("Todo App");
    window.resize(560, 680);

    auto *layout = new QVBoxLayout(&window);
    layout->setContentsMargins(24, 24, 24, 24);
    layout->setSpacing(16);

    auto *title = new QLabel("Todo App");
    title->setObjectName("Title");
    auto *subtitle = new QLabel("Prioritized and tagged tasks with persistence.");
    subtitle->setObjectName("Subtitle");

    auto *inputCard = new QFrame();
    inputCard->setObjectName("Card");
    auto *inputLayout = new QGridLayout(inputCard);
    inputLayout->setContentsMargins(12, 12, 12, 12);
    inputLayout->setHorizontalSpacing(10);
    inputLayout->setVerticalSpacing(10);

    auto *input = new QLineEdit();
    input->setPlaceholderText("Add a task...");

    auto *priorityBox = new QComboBox();
    priorityBox->addItems({"High", "Medium", "Low"});
    priorityBox->setCurrentText("Medium");

    auto *tagInput = new QLineEdit();
    tagInput->setPlaceholderText("Tag (optional)");

    auto *addButton = new QPushButton("Add");
    addButton->setObjectName("Primary");
    auto *editButton = new QPushButton("Edit");

    inputLayout->addWidget(input, 0, 0, 1, 2);
    inputLayout->addWidget(priorityBox, 0, 2);
    inputLayout->addWidget(tagInput, 1, 0, 1, 2);
    inputLayout->addWidget(addButton, 1, 2);
    inputLayout->addWidget(editButton, 2, 2);

    auto *list = new QListWidget();
    list->setSelectionMode(QAbstractItemView::SingleSelection);
    list->setObjectName("TaskList");

    auto *filterRow = new QFrame();
    filterRow->setObjectName("Card");
    auto *filterLayout = new QHBoxLayout(filterRow);
    filterLayout->setContentsMargins(12, 8, 12, 8);
    filterLayout->setSpacing(8);

    auto *allButton = new QPushButton("All");
    auto *activeButton = new QPushButton("Active");
    auto *doneButton = new QPushButton("Done");
    allButton->setCheckable(true);
    activeButton->setCheckable(true);
    doneButton->setCheckable(true);
    allButton->setChecked(true);

    auto *filters = new QButtonGroup(&window);
    filters->setExclusive(true);
    filters->addButton(allButton, static_cast<int>(FilterMode::All));
    filters->addButton(activeButton, static_cast<int>(FilterMode::Active));
    filters->addButton(doneButton, static_cast<int>(FilterMode::Done));

    filterLayout->addWidget(allButton);
    filterLayout->addWidget(activeButton);
    filterLayout->addWidget(doneButton);
    filterLayout->addStretch();

    auto *statusRow = new QHBoxLayout();
    auto *stats = new QLabel("0 total, 0 active, 0 done");
    auto *removeButton = new QPushButton("Remove Selected");
    auto *clearButton = new QPushButton("Clear Completed");
    statusRow->addWidget(stats);
    statusRow->addStretch();
    statusRow->addWidget(removeButton);
    statusRow->addWidget(clearButton);

    auto *emptyState = new QLabel("No tasks yet. Add one above.");
    emptyState->setObjectName("EmptyState");
    emptyState->setAlignment(Qt::AlignCenter);

    layout->addWidget(title);
    layout->addWidget(subtitle);
    layout->addWidget(inputCard);
    layout->addWidget(filterRow);
    layout->addWidget(list);
    layout->addWidget(emptyState);
    layout->addLayout(statusRow);

    bool loading = true;
    loadTasks(list);
    loading = false;

    FilterMode currentFilter = FilterMode::All;

    auto updateEmptyState = [&]() {
        const bool empty = (list->count() == 0);
        emptyState->setVisible(empty);
        list->setVisible(!empty);
    };

    auto updateStats = [&]() {
        int total = list->count();
        int done = 0;
        for (int i = 0; i < list->count(); ++i) {
            if (list->item(i)->checkState() == Qt::Checked) {
                done++;
            }
        }
        int active = total - done;
        stats->setText(QString("%1 total, %2 active, %3 done").arg(total).arg(active).arg(done));
    };

    auto applyFilter = [&]() {
        for (int i = 0; i < list->count(); ++i) {
            QListWidgetItem *item = list->item(i);
            const bool done = (item->checkState() == Qt::Checked);
            bool hide = false;
            if (currentFilter == FilterMode::Active && done) {
                hide = true;
            } else if (currentFilter == FilterMode::Done && !done) {
                hide = true;
            }
            item->setHidden(hide);
        }
    };

    auto addTask = [&]() {
        const QString rawText = input->text().trimmed();
        if (rawText.isEmpty()) {
            return;
        }
        auto *item = new QListWidgetItem(rawText, list);
        item->setFlags(item->flags() | Qt::ItemIsUserCheckable | Qt::ItemIsEditable);
        item->setCheckState(Qt::Unchecked);
        item->setData(Qt::UserRole, QDateTime::currentDateTime().toString(Qt::ISODate));
        item->setData(Qt::UserRole + 1, priorityBox->currentText());
        item->setData(Qt::UserRole + 2, tagInput->text().trimmed());
        item->setData(Qt::UserRole + 3, rawText);
        updateItemLabel(item);
        list->addItem(item);
        input->clear();
        tagInput->clear();
        input->setFocus();
        updateStats();
        updateEmptyState();
        applyFilter();
        saveTasks(list);
    };

    QObject::connect(addButton, &QPushButton::clicked, addTask);
    QObject::connect(input, &QLineEdit::returnPressed, addButton, &QPushButton::click);

    QObject::connect(editButton, &QPushButton::clicked, [&]() {
        QListWidgetItem *item = list->currentItem();
        if (!item) {
            return;
        }
        bool ok = false;
        const QString current = item->data(Qt::UserRole + 3).toString();
        const QString text = QInputDialog::getText(&window, "Edit Task", "Task:",
                                                   QLineEdit::Normal, current, &ok);
        if (ok && !text.trimmed().isEmpty()) {
            item->setData(Qt::UserRole + 3, text.trimmed());
            updateItemLabel(item);
            saveTasks(list);
        }
    });

    QObject::connect(removeButton, &QPushButton::clicked, [&]() {
        const int row = list->currentRow();
        if (row < 0) {
            return;
        }
        delete list->takeItem(row);
        updateStats();
        updateEmptyState();
        saveTasks(list);
    });

    QObject::connect(clearButton, &QPushButton::clicked, [&]() {
        for (int i = list->count() - 1; i >= 0; --i) {
            QListWidgetItem *item = list->item(i);
            if (item->checkState() == Qt::Checked) {
                delete list->takeItem(i);
            }
        }
        updateStats();
        updateEmptyState();
        saveTasks(list);
    });

    QObject::connect(list, &QListWidget::itemChanged, [&](QListWidgetItem *item) {
        if (loading) {
            return;
        }
        if (item) {
            updateItemLabel(item);
        }
        updateStats();
        applyFilter();
        saveTasks(list);
    });

    QObject::connect(filters, QOverload<int>::of(&QButtonGroup::idClicked), [&](int id) {
        currentFilter = static_cast<FilterMode>(id);
        applyFilter();
    });

    updateStats();
    updateEmptyState();
    applyFilter();

    window.setStyleSheet(
        "QLabel#Title { font-size: 24px; font-weight: 600; color: #111827; }"
        "QLabel#Subtitle { color: #6b7280; }"
        "QLabel#EmptyState { color: #9ca3af; padding: 18px; }"
        "QFrame#Card { background: white; border: 1px solid #e5e7eb; border-radius: 10px; }"
        "QLineEdit { padding: 8px 10px; border: 1px solid #d1d5db; border-radius: 8px; }"
        "QLineEdit:focus { border-color: #2f6fed; }"
        "QComboBox { padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 8px; }"
        "QPushButton { padding: 8px 12px; border-radius: 8px; background: #eef2f6; border: 1px solid #d7dee7; }"
        "QPushButton:hover { background: #e2e8f0; }"
        "QPushButton#Primary { background: #2f6fed; color: white; border: none; }"
        "QPushButton#Primary:hover { background: #255ad0; }"
        "QPushButton:checked { background: #2f6fed; color: white; border: none; }"
        "QListWidget#TaskList { background: white; border: 1px solid #e5e7eb; border-radius: 10px; padding: 6px; }"
        "QListWidget::item { padding: 6px; }"
        "QListWidget::item:selected { background: #e5edff; color: #111827; }"
    );

    window.show();
    return app.exec();
}
