def run_block_1():
    exec(r"""
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
print(f'\n修改后:')
print(f'粗体: {font.bold()}')
print(f'斜体: {font.italic()}')

# 字重
print(f'\n字重: {font.weight()}')
print(f'  (Normal={QFont.Normal}, Bold={QFont.Bold})')
""", globals())

def run_block_2():
    exec(r"""
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
print(f'\n当前字重: {font.weight()} (Bold={QFont.Bold})')
""", globals())

def run_block_3():
    exec(r"""
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
print(f'\n当前 Hinting: {font.hintingPreference()}')

# 抗锯齿设置
print('\n抗锯齿设置:')
print(f'  优先抗锯齿: {QFont.PreferAntialias}')
print(f'  无抗锯齿: {QFont.NoAntialias}')
font.setStyleStrategy(QFont.PreferAntialias)
print(f'\n当前样式策略: {font.styleStrategy()}')
""", globals())
