# Basilisp PySide6 Notes

经验汇总（跑通本仓库 Basilisp 例子时总结）：

- Python 关键字参数用 `** :kw value`，不要直接写 `:kw`（例如 `python/open ... ** :encoding "utf-8"`、`Property ... ** :notify sig`、`TextTestRunner ** :verbosity 2`）。
- `apply-kw` 不适合 PySide6 的 `Property` / `Slot`：用 `Property ... ** :notify ...` 或 `Slot ... ** :result ...`。
- Qt classmethod 调用用 `(. Class method)`，例如 `(. QDate currentDate)`、`(. QTime currentTime)`、`(. QStandardPaths writableLocation ...)`。
- 访问属性用 `.-`，不要用 `(. obj attr)`；例如 `(. current parent)` 会报错，应写 `(.-parent current)`。
- Python 迭代器/生成器不能 `seq`，用 `iterator-seq`：
  - 文件遍历：`(doseq [line (iterator-seq f2)] ...)`
  - `futures.as_completed` 返回生成器：`(iterator-seq (. futures as_completed ...))`
- Qt 的 `proxy` 子类经常触发 metaclass conflict。避免 `proxy [QWidget/QWindow/QGraphicsView]`：
  - 用 `python/type` 定义子类并实现事件方法（`paintEvent` / `wheelEvent` / `keyPressEvent` 等）。
- `threading/current_thread` 不是合法符号，使用 `(. threading current_thread)`。
- `QTimer.singleShot` 必须传可调用对象：`(. QTimer singleShot 100 (fn [] (. QCoreApplication quit)))`。
- `Signal` / `Property` 类型建议来自 `builtins`：`(def py-int (.-int builtins))`，`(Signal py-int)`。
- `ProcessPoolExecutor` 在 Basilisp 环境可能无法 pickle 函数；演示中应捕获异常并提示跳过。

常见报错对应修复：
- `Keyword object cannot be interpreted as an integer` → 忘了 `**` 传 kwargs。
- `Can't create sequence out of single-use iterable` → 用 `iterator-seq`。
- `metaclass conflict` → 不要 `proxy` Qt 类，改 `python/type`。
- `TypeError: Property argument 6 must be str` → 用 `Property ** :notify ...` 而非位置参数。
