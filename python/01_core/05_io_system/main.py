#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 I/O 系统示例

Qt提供跨平台的文件和I/O操作：
- QFile: 文件读写
- QDir: 目录操作
- QFileInfo: 文件信息
- QTextStream: 文本流
- QDataStream: 二进制流
- QStandardPaths: 标准路径

对比：
- Python方式: 使用open(), pathlib, os（推荐日常使用）
- Qt方式: 使用QFile, QDir等（与C++代码对应，跨平台一致）

官方文档: https://doc.qt.io/qtforpython/PySide6/QtCore/QFile.html
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from PySide6.QtCore import (
    QCoreApplication,
    QFile,
    QDir,
    QFileInfo,
    QTextStream,
    QDataStream,
    QIODevice,
    QTemporaryFile,
    QStandardPaths
)


def demonstrate_python_file_io():
    """Python标准库文件操作（推荐方式）"""
    print("=== Python 文件操作示例 ===\n")
    
    file_name = "test_python.txt"
    
    # 写入文本文件
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write("Hello, Python!\n")
        f.write("这是中文内容\n")
        f.write("Line 3\n")
    print(f"文件写入成功: {file_name}")
    
    # 读取文本文件 - 逐行
    print("\n文件内容 (逐行):")
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            print(f"  {line.rstrip()}")
    
    # 一次性读取
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"\n全部内容:\n{content}")
    
    # 追加模式
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write("追加的内容\n")
    print("内容已追加")
    
    # 清理
    os.remove(file_name)


def demonstrate_qfile():
    """QFile 文本文件操作（Qt方式）"""
    print("\n=== QFile 文本操作示例 ===\n")
    
    file_name = "test.txt"
    
    # 写入文本文件
    write_file = QFile(file_name)
    if write_file.open(QIODevice.WriteOnly | QIODevice.Text):
        stream = QTextStream(write_file)
        stream << "Hello, Qt6!\n"
        stream << "这是中文内容\n"
        stream << "Line 3\n"
        write_file.close()
        print(f"文件写入成功: {file_name}")
    
    # 读取文本文件
    read_file = QFile(file_name)
    if read_file.open(QIODevice.ReadOnly | QIODevice.Text):
        stream = QTextStream(read_file)
        print("\n文件内容:")
        while not stream.atEnd():
            line = stream.readLine()
            print(f"  {line}")
        read_file.close()
    
    # 一次性读取
    if read_file.open(QIODevice.ReadOnly | QIODevice.Text):
        content = read_file.readAll()
        print(f"\n全部内容: {content}")
        read_file.close()
    
    # 追加模式
    if write_file.open(QIODevice.Append | QIODevice.Text):
        stream = QTextStream(write_file)
        stream << "追加的内容\n"
        write_file.close()
        print("内容已追加")


def demonstrate_qdatastream():
    """QDataStream 二进制数据操作"""
    print("\n=== QDataStream (二进制) 示例 ===\n")
    
    bin_file_name = "data.bin"
    
    # 写入二进制
    write_file = QFile(bin_file_name)
    if write_file.open(QIODevice.WriteOnly):
        stream = QDataStream(write_file)
        
        # 写入各种类型
        stream.writeQString("Hello")
        stream.writeInt32(12345)
        stream.writeDouble(3.14159)
        
        # 写入列表
        stream.writeInt32(3)  # 列表长度
        for item in ["Apple", "Banana", "Cherry"]:
            stream.writeQString(item)
        
        write_file.close()
        print("二进制写入成功")
    
    # 读取二进制
    read_file = QFile(bin_file_name)
    if read_file.open(QIODevice.ReadOnly):
        stream = QDataStream(read_file)
        
        str_val = stream.readQString()
        num_val = stream.readInt32()
        dbl_val = stream.readDouble()
        
        # 读取列表
        list_len = stream.readInt32()
        list_val = []
        for _ in range(list_len):
            list_val.append(stream.readQString())
        
        print(f"读取字符串: {str_val}")
        print(f"读取整数: {num_val}")
        print(f"读取浮点: {dbl_val}")
        print(f"读取列表: {list_val}")
        
        read_file.close()


def demonstrate_qdir():
    """QDir 目录操作"""
    print("\n=== QDir 示例 ===\n")
    
    current_dir = QDir.current()
    
    print(f"当前目录: {current_dir.absolutePath()}")
    print(f"主目录: {QDir.homePath()}")
    print(f"临时目录: {QDir.tempPath()}")
    print(f"根目录: {QDir.rootPath()}")
    
    # 列出文件
    print("\n当前目录文件:")
    files = current_dir.entryList(QDir.Files)
    for file in files[:10]:  # 限制数量
        print(f"  {file}")
    
    # 列出子目录
    print("\n子目录:")
    dirs = current_dir.entryList(QDir.Dirs | QDir.NoDotAndDotDot)
    for dir_name in dirs[:10]:
        print(f"  {dir_name}")
    
    # 过滤文件
    print("\nPython 文件:")
    py_files = current_dir.entryList(["*.py"], QDir.Files)
    for file in py_files:
        print(f"  {file}")
    
    # 创建目录
    test_dir = "test_dir"
    if current_dir.mkdir(test_dir):
        print(f"\n创建目录成功: {test_dir}")
        current_dir.rmdir(test_dir)
        print(f"删除目录成功: {test_dir}")


def demonstrate_pathlib():
    """Python pathlib（现代路径操作方式）"""
    print("\n=== Python pathlib 示例 ===\n")
    
    # 创建Path对象
    current = Path.cwd()
    print(f"当前目录: {current}")
    print(f"主目录: {Path.home()}")
    
    # 路径拼接
    file_path = current / "test.txt"
    print(f"文件路径: {file_path}")
    
    # 路径分解
    print(f"文件名: {file_path.name}")
    print(f"后缀: {file_path.suffix}")
    print(f"基本名: {file_path.stem}")
    print(f"父目录: {file_path.parent}")
    
    # 列出文件
    print("\nPython 文件:")
    for f in current.glob("*.py"):
        print(f"  {f}")
    
    # 文件信息
    if file_path.exists():
        stat = file_path.stat()
        print(f"\n文件大小: {stat.st_size} bytes")
        print(f"修改时间: {datetime.fromtimestamp(stat.st_mtime)}")


def demonstrate_qfileinfo():
    """QFileInfo 文件信息"""
    print("\n=== QFileInfo 示例 ===\n")
    
    info = QFileInfo("test.txt")
    
    if info.exists():
        print(f"文件名: {info.fileName()}")
        print(f"完整路径: {info.absoluteFilePath()}")
        print(f"目录: {info.absolutePath()}")
        print(f"后缀: {info.suffix()}")
        print(f"基本名: {info.baseName()}")
        print(f"大小: {info.size()} bytes")
        print(f"是文件: {info.isFile()}")
        print(f"是目录: {info.isDir()}")
        print(f"可读: {info.isReadable()}")
        print(f"可写: {info.isWritable()}")
        print(f"创建时间: {info.birthTime().toString()}")
        print(f"修改时间: {info.lastModified().toString()}")


def demonstrate_standard_paths():
    """QStandardPaths 标准路径"""
    print("\n=== QStandardPaths 示例 ===\n")
    
    print(f"桌面: {QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)}")
    print(f"文档: {QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)}")
    print(f"下载: {QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)}")
    print(f"音乐: {QStandardPaths.writableLocation(QStandardPaths.MusicLocation)}")
    print(f"图片: {QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)}")
    print(f"视频: {QStandardPaths.writableLocation(QStandardPaths.MoviesLocation)}")
    print(f"缓存: {QStandardPaths.writableLocation(QStandardPaths.CacheLocation)}")
    print(f"配置: {QStandardPaths.writableLocation(QStandardPaths.ConfigLocation)}")
    print(f"应用数据: {QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)}")


def demonstrate_temporary_file():
    """QTemporaryFile 临时文件"""
    print("\n=== QTemporaryFile 示例 ===\n")
    
    # 默认自动删除
    temp_file = QTemporaryFile()
    if temp_file.open():
        print(f"临时文件: {temp_file.fileName()}")
        temp_file.write("Temp Content".encode('utf-8'))
        temp_file.close()
        # 默认关闭时自动删除
    
    # Python tempfile 对比
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=True, suffix='.txt') as f:
        f.write("Python临时内容")
        print(f"Python临时文件: {f.name}")
    # 退出with块时自动删除
    
    # 保留临时文件
    persistent_temp = QTemporaryFile()
    persistent_temp.setAutoRemove(False)
    if persistent_temp.open():
        print(f"持久临时文件: {persistent_temp.fileName()}")
        persistent_temp.close()
        # 需要手动删除
        QFile(persistent_temp.fileName()).remove()


def main():
    """主函数"""
    app = QCoreApplication(sys.argv)
    
    print("=== PySide6 I/O 系统示例 ===\n")
    
    demonstrate_python_file_io()
    demonstrate_qfile()
    demonstrate_qdatastream()
    demonstrate_qdir()
    demonstrate_pathlib()
    demonstrate_qfileinfo()
    demonstrate_standard_paths()
    demonstrate_temporary_file()
    
    # 清理测试文件
    QFile.remove("test.txt")
    QFile.remove("data.bin")
    
    print("\n测试文件已清理")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
