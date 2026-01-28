#!/usr/bin/env clojure -M
;; PySide6 字体示例 (Clojure + libpython-clj)
;; 注意：QFontDatabase 需要 QGuiApplication，这里仅演示基础字体属性

(require '[libpython-clj2.python :as py])

(py/initialize!)

(defn demonstrate-font-properties
  "字体属性"
  []
  (println "\n=== 字体属性 ===")
  
  ;; 使用 Python 代码演示
  (py/run-simple-string "
from PySide6.QtGui import QFont, QFontMetrics

# 创建字体
font = QFont('Arial', 12)
print(f'字体族: {font.family()}')
print(f'大小: {font.pointSize()}pt')
print(f'粗体: {font.bold()}')
print(f'斜体: {font.italic()}')
print(f'下划线: {font.underline()}')

# 修改属性
font.setBold(True)
font.setItalic(True)
font.setUnderline(True)
print(f'\\n修改后:')
print(f'粗体: {font.bold()}')
print(f'斜体: {font.italic()}')

# 字重
print(f'\\n字重: {font.weight()}')
print(f'  (Normal={QFont.Normal}, Bold={QFont.Bold})')
")
  
  (println "字体属性演示完成"))

(defn demonstrate-font-weights
  "字体字重"
  []
  (println "\n=== 字体字重 ===")
  
  (py/run-simple-string "
from PySide6.QtGui import QFont

# 不同字重
weights = [
    (QFont.Thin, 'Thin'),
    (QFont.ExtraLight, 'ExtraLight'),
    (QFont.Light, 'Light'),
    (QFont.Normal, 'Normal'),
    (QFont.Medium, 'Medium'),
    (QFont.DemiBold, 'DemiBold'),
    (QFont.Bold, 'Bold'),
    (QFont.ExtraBold, 'ExtraBold'),
    (QFont.Black, 'Black')
]

print('字体字重:')
for weight, name in weights:
    print(f'  {weight}: {name}')

# 设置字重
font = QFont()
font.setWeight(QFont.Bold)
print(f'\\n当前字重: {font.weight()} (Bold={QFont.Bold})')
")
  
  (println "字体字重演示完成"))

(defn demonstrate-font-styles
  "字体样式"
  []
  (println "\n=== 字体样式 ===")
  
  (py/run-simple-string "
from PySide6.QtGui import QFont

font = QFont('Helvetica', 14)

# Hinting 策略（PySide6 中可用）
strategies = [
    (QFont.PreferDefaultHinting, 'PreferDefaultHinting'),
    (QFont.PreferNoHinting, 'PreferNoHinting'),
    (QFont.PreferVerticalHinting, 'PreferVerticalHinting'),
    (QFont.PreferFullHinting, 'PreferFullHinting'),
]

print('字体 Hinting 策略:')
for strategy, name in strategies:
    print(f'  {strategy}: {name}')

# 设置 Hinting 策略
font.setHintingPreference(QFont.PreferFullHinting)
print(f'\\n当前 Hinting: {font.hintingPreference()}')

# 抗锯齿设置
print('\\n抗锯齿设置:')
print(f'  优先抗锯齿: {QFont.PreferAntialias}')
print(f'  无抗锯齿: {QFont.NoAntialias}')
font.setStyleStrategy(QFont.PreferAntialias)
print(f'\\n当前样式策略: {font.styleStrategy()}')
")
  
  (println "字体样式演示完成"))

(defn -main
  [& args]
  (println "=== PySide6 字体示例 (Clojure) ===")
  
  (demonstrate-font-properties)
  (demonstrate-font-weights)
  (demonstrate-font-styles)
  
  (println "\n=== 字体要点 ===")
  (println "1. QFont: 字体类")
  (println "2. 属性: family, pointSize, bold, italic")
  (println "3. 字重: Thin, Normal, Bold, Black")
  (println "4. Hinting: 字体渲染提示策略")
  (println "5. QFontDatabase 需要 QGuiApplication（GUI 模式）")
  
  (println "\n=== 完成 ==="))

(-main)
