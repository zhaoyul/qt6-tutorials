;; PySide6 Hiccup Todo App (Clojure + libpython-clj)
;; Note: macOS GUI requires -XstartOnFirstThread

(ns qt6_tutorials.ch13.reagent.todo_app
  (:require [clojure.data.json :as json]
            [clojure.string :as str]
            [libpython-clj2.python :as py]
            [libpython-clj2.require :refer [require-python]]
            [qt6_tutorials.ch13.reagent.core :as q]))

(py/initialize!)

(require-python '[PySide6.QtWidgets :as QtWidgets :bind-ns])
(require-python '[PySide6.QtCore :as QtCore :bind-ns])
(require-python '[pathlib :as pathlib :bind-ns])
(require-python '[os :as os :bind-ns])

(def QApplication (py/get-attr QtWidgets "QApplication"))
(def QWidget (py/get-attr QtWidgets "QWidget"))
(def QStandardPaths (py/get-attr QtCore "QStandardPaths"))

(defonce app-instance (atom nil))
(defonce mount-ref (atom nil))
(defonce state (q/atom {:input ""
                        :priority "Medium"
                        :tag ""
                        :editing-id nil
                        :filter :all
                        :tasks []}))

(defn- assoc-state!
  [& kvs]
  (apply swap! state assoc kvs))

(defn- update-state!
  [f & args]
  (apply swap! state f args))

(defn- update-tasks!
  [f & args]
  (apply update-state! update :tasks f args))

(defn- map-tasks!
  [f]
  (update-tasks! (fn [tasks] (mapv f tasks))))

(defn- remove-tasks!
  [pred]
  (update-tasks! (fn [tasks] (vec (remove pred tasks)))))

(defn- update-task!
  [task-id f]
  (map-tasks! (fn [task] (if (= (:id task) task-id) (f task) task))))

(defn- reset-input!
  []
  (assoc-state! :input "" :tag "" :priority "Medium" :editing-id nil))

(defn data-file-path
  []
  (let [data-dir (py/call-attr QStandardPaths "writableLocation"
                               (py/get-attr QStandardPaths "AppDataLocation"))
        path-class (py/get-attr pathlib "Path")
        data-path (path-class data-dir)
        os-path (py/get-attr os "path")]
    (py/call-attr-kw data-path "mkdir" [] {"parents" true "exist_ok" true})
    (py/call-attr os-path "join" data-dir "hiccup_todos.json")))

(defn save-tasks!
  [tasks]
  (try
    (spit (data-file-path) (json/write-str tasks))
    (catch Exception e
      (println "save-tasks error:" e))))

(defn load-tasks
  []
  (try
    (let [tasks (json/read-str (slurp (data-file-path)) :key-fn keyword)]
      (mapv (fn [task]
              (merge {:priority "Medium" :tag ""}
                     task))
            tasks))
    (catch java.io.FileNotFoundException _
      [])
    (catch Exception e
      (println "load-tasks error:" e)
      [])))

(defonce persist-watch
  (do
    (add-watch state ::persist
               (fn [_ _ old new]
                 (when (not= (:tasks old) (:tasks new))
                   (save-tasks! (:tasks new)))))
    true))

(defn new-task
  [text priority tag]
  {:id (str (random-uuid))
   :text text
   :priority priority
   :tag tag
   :done false
   :created (System/currentTimeMillis)})

(defn add-or-update-task!
  []
  (let [{:keys [input priority tag editing-id]} @state
        text (str/trim input)
        tag (str/trim tag)]
    (when (seq text)
      (if editing-id
        (do
          (update-task! editing-id #(assoc % :text text :priority priority :tag tag))
          (reset-input!))
        (do
          (update-tasks! conj (new-task text priority tag))
          (reset-input!))))))

(defn start-edit!
  [task]
  (assoc-state! :editing-id (:id task)
                :input (:text task)
                :priority (:priority task)
                :tag (:tag task)))

(defn cancel-edit!
  []
  (reset-input!))

(defn delete-task!
  [task-id]
  (remove-tasks! #(= (:id %) task-id)))

(defn toggle-task!
  [task-id done?]
  (update-task! task-id #(assoc % :done (boolean done?))))

(defn clear-completed!
  []
  (remove-tasks! :done))

(defn toggle-all!
  []
  (let [all-done? (every? :done (:tasks @state))]
    (map-tasks! #(assoc % :done (not all-done?)))))

(defn visible-tasks
  [{:keys [filter tasks]}]
  (let [tasks (or tasks [])]
    (case filter
      :active (filterv (comp not :done) tasks)
      :done (filterv :done tasks)
      tasks)))

(defn stats
  [tasks]
  (let [total (count tasks)
        done (count (filter :done tasks))]
    {:total total
     :done done
     :active (- total done)}))

(defn button-style
  [active?]
  (if active?
    {:background "#111827"
     :color "#ffffff"
     :padding "6px 10px"
     :border-radius "6px"}
    {:background "#f3f4f6"
     :color "#111827"
     :padding "6px 10px"
     :border-radius "6px"}))

(defn html-escape
  [s]
  (str/escape (str s)
              {\& "&amp;"
               \< "&lt;"
               \> "&gt;"
               \" "&quot;"
               \' "&#39;"}))

(defn css
  [m]
  (->> m
       (map (fn [[k v]] (str (name k) ":" v ";")))
       (apply str)))

(defn html
  [node]
  (cond
    (nil? node) ""
    (string? node) (html-escape node)
    (number? node) (html-escape (str node))
    (vector? node)
    (let [[tag & more] node
          [attrs children] (if (map? (first more)) [(first more) (rest more)] [nil more])
          tag-name (name tag)
          attrs (or attrs {})
          attr-str (->> attrs
                        (map (fn [[k v]]
                               (when (some? v)
                                 (let [v (if (and (= k :style) (map? v)) (css v) v)]
                                   (str (name k) "=\"" (html-escape (str v)) "\"")))))
                        (remove nil?)
                        (str/join " "))
          open (if (seq attr-str)
                 (str "<" tag-name " " attr-str ">")
                 (str "<" tag-name ">"))
          inner (apply str (map html children))
          close (str "</" tag-name ">")]
      (str open inner close))
    (sequential? node) (apply str (map html node))
    :else ""))

(defn html*
  [& nodes]
  (html nodes))

(defn task-row
  [task]
  (let [{:keys [id text done priority tag]} task
        priority-color (case priority
                         "High" "#ef4444"
                         "Medium" "#f59e0b"
                         "Low" "#10b981"
                         "#9ca3af")
        label (html*
               (if done
                 [:span {:style "color:#9ca3af;"} [:s text]]
                 [:span {:style "color:#111827;"} text])
               [:span {:style (str "color:" priority-color ";")} (str " [" priority "]")]
               (when (seq tag)
                 [:span {:style "color:#6b7280;"} (str " #" tag)]))]
    [:QWidget
     {:style {:background "#ffffff"
              :border "1px solid #e5e7eb"
              :border-radius "6px"}
      :fixed-height 48}
     [:QHBoxLayout {:spacing 8
                    :contents-margins [10 4 10 4]}
      [:QCheckBox {:checked (boolean done)
                   :on-toggled #(toggle-task! id %)}]
      [:QLabel {:text label
                :word-wrap false
                :minimum-width 220}]
      [:stretch]
      [:QPushButton {:text "Edit"
                     :style {:background "#e0e7ff"
                             :color "#3730a3"
                             :padding "4px 8px"
                             :border-radius "6px"}
                     :on-clicked #(start-edit! task)}]
      [:QPushButton {:text "Delete"
                     :style {:background "#fee2e2"
                             :color "#991b1b"
                             :padding "4px 8px"
                             :border-radius "6px"}
                     :on-clicked #(delete-task! id)}]]]))

(defn filter-button
  [label filter-key]
  (let [active? (= filter-key (:filter @state))]
    [:QPushButton {:text label
                   :style (button-style active?)
                   :on-clicked #(assoc-state! :filter filter-key)}]))

(defn todo-app
  []
  (let [{:keys [input tasks priority tag editing-id]} @state
        {:keys [total done active]} (stats tasks)
        visible (visible-tasks @state)
        input-row
        [:QWidget
         [:QHBoxLayout {:spacing 8}
          [:QLineEdit {:placeholder-text "What needs to be done?"
                       :text input
                       :on-text-changed #(assoc-state! :input %)
                       :on-return-pressed #(add-or-update-task!)}]
          [:QComboBox {:items ["High" "Medium" "Low"]
                       :current-text priority
                       :on-current-text-changed #(assoc-state! :priority %)}]
          [:QLineEdit {:placeholder-text "Tag"
                       :text tag
                       :on-text-changed #(assoc-state! :tag %)}]
          [:QPushButton {:text (if editing-id "Save" "Add")
                         :enabled (boolean (seq (str/trim input)))
                         :style {:background "#2563eb"
                                 :color "#ffffff"
                                 :padding "6px 12px"
                                 :border-radius "6px"}
                         :on-clicked #(add-or-update-task!)}]
          (when editing-id
            [:QPushButton {:text "Cancel"
                           :style {:background "#e5e7eb"
                                   :color "#111827"
                                   :padding "6px 12px"
                                   :border-radius "6px"}
                           :on-clicked #(cancel-edit!)}])]]
        filter-row
        [:QWidget
         [:QHBoxLayout {:spacing 8}
          (filter-button "All" :all)
          (filter-button "Active" :active)
          (filter-button "Done" :done)
          [:QLabel {:text (html [:span {:style "color:#6b7280;"} (str active " active / " done " done")])}]
          [:QPushButton {:text "Toggle All"
                         :style {:background "#111827"
                                 :color "#ffffff"
                                 :padding "6px 10px"
                                 :border-radius "6px"}
                         :on-clicked #(toggle-all!)}]]]
        list-content
        [:QWidget
         {:style {:background "transparent"}}
         [:QVBoxLayout {:spacing 6
                        :contents-margins [4 4 4 4]}
          (if (empty? visible)
            [:QLabel {:text (html [:span {:style "color:#9ca3af;"} "No tasks"])}]
            (into [:<>] (map task-row visible)))]]
        list-row
        [:QScrollArea {:widget-resizable true
                       :minimum-height 260
                       :style {:background "transparent"
                               :border "none"}
                       :qss "QScrollBar:vertical{background:transparent;width:10px;margin:0 2px;}QScrollBar::handle:vertical{background:#cbd5f5;border-radius:5px;min-height:24px;}QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0;}QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{background:transparent;}"
                       :content list-content}]
        footer-row
        [:QWidget
         [:QHBoxLayout {:spacing 8}
          [:QLabel {:text (html [:span {:style "color:#6b7280;"} (str "Total: " total)])}]
          [:QPushButton {:text "Clear Completed"
                         :enabled (pos? done)
                         :style {:background "#f97316"
                                 :color "#ffffff"
                                 :padding "6px 12px"
                                 :border-radius "6px"}
                         :on-clicked #(clear-completed!)}]]]]
    [:QWidget
     (into [:QVBoxLayout {:spacing 10
                          :contents-margins [16 14 16 14]}]
           [[:QLabel {:text (html [:span {:style "font-size:22px; font-weight:700;"} "Todo App"])}]
            [:QLabel {:text (html [:span {:style "color:#6b7280;"} "Data-driven Hiccup UI with PySide6"])}]
            input-row
            filter-row
            list-row
            footer-row])]))

(defn -main
  [& _]
  (reset! app-instance (QApplication (py/->py-list [])))
  (assoc-state! :tasks (vec (load-tasks)))
  (let [root (QWidget)]
    (py/call-attr root "setWindowTitle" "Hiccup Todo App")
    (py/call-attr root "resize" 520 640)
    (reset! mount-ref (q/mount! root [todo-app]))
    (py/call-attr root "show")
    (py/call-attr @app-instance "exec")))
