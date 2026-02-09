;; PySide6 Hiccup Renderer Demo (Clojure + libpython-clj)
;; Note: macOS GUI requires -XstartOnFirstThread

(ns qt6_tutorials.ch03.widgets.hiccup_demo
  (:require [libpython-clj2.python :as py]
            [libpython-clj2.require :refer [require-python]]
            [qt6_tutorials.ch13.reagent.core :as q]))

(py/initialize!)

(require-python '[PySide6.QtWidgets :as QtWidgets :bind-ns])

(def QApplication (py/get-attr QtWidgets "QApplication"))
(def QWidget (py/get-attr QtWidgets "QWidget"))

(defonce app-instance (atom nil))
(defonce state (q/atom {:count 0 :name "Qt"}))

(defn counter []
  [:QWidget {:layout :QVBoxLayout}
   [:QLabel {:text (str "Hello " (:name @state))}]
   [:QLabel {:text (str "Count: " (:count @state))}]
   [:QLineEdit {:placeholder-text "Name"
                :text (:name @state)
                :on-text-changed #(swap! state assoc :name %)}]
   [:QPushButton {:text "Inc"
                  :on-clicked #(swap! state update :count inc)}]])

(defn -main
  [& _]
  (reset! app-instance (QApplication (py/->py-list [])))
  (let [root (QWidget)]
    (py/call-attr root "setWindowTitle" "Hiccup Qt Demo")
    (q/mount! root [counter])
    (py/call-attr root "resize" 360 220)
    (py/call-attr root "show")
    (py/call-attr @app-instance "exec")))
