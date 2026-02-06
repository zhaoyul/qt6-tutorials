#!/usr/bin/env clojure -M
;; PySide6 Todo App Demo (Clojure + libpython-clj)
;; A feature-rich TODO application with priorities, tags, and persistence
;; Note: macOS 需要使用 -XstartOnFirstThread JVM 参数运行

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]]
         '[clojure.data.json :as json])

(py/initialize!)

;; 导入模块
(require-python '[PySide6.QtCore :as QtCore :bind-ns])
(require-python :from "12_project/todo_app"
                '[embedded :as py-embedded :bind-ns :reload])
(require-python '[PySide6.QtWidgets :as QtWidgets :bind-ns])
(require-python '[pathlib :as pathlib :bind-ns])
(require-python '[os :as os :bind-ns])

(def Qt (py/get-attr QtCore "Qt"))

(def FilterMode
  {:ALL 0 :ACTIVE 1 :DONE 2})

(defn- macos?
  []
  (.startsWith (System/getProperty "os.name") "Mac"))

(defn- started-on-first-thread?
  []
  (= "1" (System/getenv "JAVA_STARTED_ON_FIRST_THREAD_")))

(defn- ensure-macos-gui-thread
  []
  (when (and (macos?) (not (started-on-first-thread?)))
    (println "macOS 需要使用 -XstartOnFirstThread 运行此 GUI 示例，已跳过。")
    (System/exit 0)))

(defn data-file-path
  "Get the path for storing todo data."
  []
  (let [QStandardPaths (py/get-attr QtCore "QStandardPaths")
        data-dir (py/call-attr QStandardPaths "writableLocation"
                               (py/get-attr QStandardPaths "AppDataLocation"))
        path-class (py/get-attr pathlib "Path")
        data-path (py/call-attr path-class data-dir)
        os-path (py/get-attr os "path")]
    (py/call-attr-kw data-path "mkdir" [] {"parents" true "exist_ok" true})
    (py/call-attr os-path "join" data-dir "todos.json")))

(defn priority-color
  "Get color for a given priority."
  [priority]
  (case priority
    "High" "#ef4444"
    "Medium" "#f59e0b"
    "Low" "#10b981"
    "#9ca3af"))

(defn update-item-label
  "Update the display label of an item."
  [item]
  (let [base-text (py/call-attr item "data" (py/get-attr Qt "UserRole") 3)
        priority (or (py/call-attr item "data" (py/get-attr Qt "UserRole") 1) "Medium")
        tag (or (py/call-attr item "data" (py/get-attr Qt "UserRole") 2) "")
        base (or base-text "")
        suffix (str " [" priority "]" (if (seq tag) (str " #" tag) ""))]
    (py/call-attr item "setText" (str base suffix))
    (py/call-attr item "setForeground" (priority-color priority))))

(defn save-tasks
  "Save tasks to JSON file."
  [list-widget]
  (let [tasks (atom [])
        count (py/call-attr list-widget "count")]
    (doseq [i (range count)]
      (let [item (py/call-attr list-widget "item" i)
            task {:text (py/call-attr item "text")
                  :done (= (py/call-attr item "checkState") (py/get-attr Qt "Checked"))
                  :createdAt (or (py/call-attr item "data" (py/get-attr Qt "UserRole")) "")
                  :priority (or (py/call-attr item "data" (py/get-attr Qt "UserRole") 1) "Medium")
                  :tag (or (py/call-attr item "data" (py/get-attr Qt "UserRole") 2) "")}]
        (swap! tasks conj task)))
    (try
      (spit (data-file-path) (json/write-str @tasks))
      (catch Exception e
        (println "Error saving tasks:" e)))))

(defn load-tasks
  "Load tasks from JSON file."
  [list-widget loading-atom]
  (let [QListWidgetItem (py/get-attr QtWidgets "QListWidgetItem")]
    (try
      (let [tasks (json/read-str (slurp (data-file-path)) :key-fn keyword)]
        (doseq [task tasks]
          (let [raw-text (:text task)
                done (:done task false)
                created-at (:createdAt task "")
                priority (:priority task "Medium")
                tag (:tag task "")
                base-text (if (clojure.string/includes? raw-text " [")
                            (first (clojure.string/split raw-text #" \["))
                            raw-text)
                item (QListWidgetItem)]
            (py/call-attr item "setFlags"
                          (bit-or (py/call-attr item "flags")
                                  (py/get-attr Qt "ItemIsUserCheckable")
                                  (py/get-attr Qt "ItemIsEditable")))
            (py/call-attr item "setCheckState" (if done (py/get-attr Qt "Checked") (py/get-attr Qt "Unchecked")))
            (py/call-attr item "setData" (py/get-attr Qt "UserRole") created-at)
            (py/call-attr item "setData" (py/get-attr Qt "UserRole") priority 1)
            (py/call-attr item "setData" (py/get-attr Qt "UserRole") tag 2)
            (py/call-attr item "setData" (py/get-attr Qt "UserRole") base-text 3)
            (update-item-label item)
            (py/call-attr list-widget "addItem" item))))
      (catch java.io.FileNotFoundException _
        nil)
      (catch Exception e
        (println "Error loading tasks:" e)))))

(defn run-todo-app
  "Call the embedded Python entry point (`run_block_1`) that spins up the shared PySide6 UI."
  []
  (py/call-attr py-embedded "run_block_1"))

(defn -main
  [& args]
  (println "=== PySide6 Todo App (Clojure + libpython-clj) ===")
  (println "注意: macOS 必须使用 -XstartOnFirstThread JVM 参数")

  (ensure-macos-gui-thread)
  (run-todo-app)

  (println "\n=== 完成 ==="))

(-main)
