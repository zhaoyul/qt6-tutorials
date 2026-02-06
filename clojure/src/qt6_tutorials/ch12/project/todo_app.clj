;; PySide6 Todo App Demo (Clojure + libpython-clj)
;; A feature-rich TODO application with priorities, tags, and persistence
;; Note: macOS 需要使用 -XstartOnFirstThread JVM 参数运行

(ns qt6_tutorials.ch12.project.todo_app)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]]
         '[clojure.data.json :as json]
         '[clojure.java.io :as io]
         '[nrepl.server :as nrepl])

(py/initialize!)

;; 导入模块
(require-python '[PySide6.QtCore :as QtCore :bind-ns])
(require-python :from "12_project/todo_app"
                '[embedded :as py-embedded :bind-ns :reload])
(require-python '[PySide6.QtWidgets :as QtWidgets :bind-ns])
(require-python '[PySide6.QtGui :as QtGui :bind-ns])
(require-python '[pathlib :as pathlib :bind-ns])
(require-python '[os :as os :bind-ns])

(def Qt (py/get-attr QtCore "Qt"))

(def FilterMode
  {:ALL 0 :ACTIVE 1 :DONE 2})

(defonce nrepl-server (atom nil))
(defonce extra-widgets (atom []))

(defn start-nrepl!
  "Start an in-process nREPL server. Returns the server map."
  ([] (start-nrepl! 0))
  ([port]
   (when-not @nrepl-server
     (let [server (nrepl/start-server :port port)]
       (reset! nrepl-server server)
       (let [port-str (str (:port server))
             port-file (io/file ".nrepl-port")]
         (spit port-file port-str)
         (println (str "nREPL listening on port " port-str))
         (println (str "nREPL port written to " (.getAbsolutePath port-file)))
         (flush))
       server))))

(defn stop-nrepl!
  "Stop the in-process nREPL server if it is running."
  []
  (when-let [server @nrepl-server]
    (nrepl/stop-server server)
    (reset! nrepl-server nil)
    (try
      (io/delete-file ".nrepl-port" true)
      (catch Exception _ nil))))

(defn window
  "Return the PySide6 main window instance created by embedded.py."
  []
  (py/get-attr py-embedded "window"))

(defn ui-dispatch!
  "Schedule a function to run on the Qt UI thread."
  [f]
  (let [callback (py/make-callable (fn []
                                     (try
                                       (f)
                                       (catch Exception e
                                         (println "UI dispatch error:" e)))
                                     nil))]
    (py/call-attr py-embedded "enqueue_ui" callback)))

(defn set-title!
  "Update the window title."
  [title]
  (ui-dispatch!
   (fn []
     (py/call-attr (window) "setWindowTitle" title))))

(defn set-subtitle!
  "Update the subtitle label."
  [text]
  (ui-dispatch!
   (fn []
     (py/call-attr (py/get-attr (window) "subtitle") "setText" text))))

(defn add-task!
  "Add a task via the UI controls. Options: :priority, :tag."
  ([text] (add-task! text {}))
  ([text {:keys [priority tag] :or {priority "Medium" tag ""}}]
   (ui-dispatch!
    (fn []
      (let [wnd (window)]
        (py/call-attr (py/get-attr wnd "input_field") "setText" text)
        (py/call-attr (py/get-attr wnd "priority_box") "setCurrentText" priority)
        (py/call-attr (py/get-attr wnd "tag_input") "setText" tag)
        (py/call-attr wnd "add_task"))))))

(defn add-button!
  "Add a button to the main layout and wire an on-click handler."
  ([label] (add-button! label (fn [] (println "Clicked:" label))))
  ([label on-click]
   (ui-dispatch!
    (fn []
      (let [QPushButton (py/get-attr QtWidgets "QPushButton")
            btn (QPushButton label)
            handler (py/make-callable (fn [] (on-click) nil))]
        (py/call-attr (py/get-attr btn "clicked") "connect" handler)
        (py/call-attr (py/call-attr (window) "layout") "addWidget" btn)
        (swap! extra-widgets conj btn)
        btn)))))

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
    (py/call-attr item "setForeground"
                  (py/call-attr QtGui "QColor" (priority-color priority)))))

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

(defn- parse-args
  "Parse CLI args for experimental features."
  [args]
  (println args)
  (loop [opts {} xs args]
    (if (empty? xs)
      opts
      (let [[x & more] xs]
        (case x
          "--nrepl" (recur (assoc opts :nrepl true) more)
          "--nrepl-port" (recur (assoc opts :nrepl-port (Integer/parseInt (first more))) (rest more))
          (recur opts more))))))

(defn -main
  [& args]
  (println "=== PySide6 Todo App (Clojure + libpython-clj) ===")
  (let [{:keys [nrepl nrepl-port]} (parse-args args)]
    (when (or nrepl nrepl-port)
      (start-nrepl! (or nrepl-port 0)))
    (run-todo-app))

  (println "\n=== 完成 ==="))
