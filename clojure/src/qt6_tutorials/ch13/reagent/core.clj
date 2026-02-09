;; Minimal data-driven Hiccup renderer for PySide6 (Clojure + libpython-clj)

(ns qt6_tutorials.ch13.reagent.core
  (:refer-clojure :exclude [atom])
  (:require [clojure.set :as set]
            [clojure.string :as str]
            [libpython-clj2.python :as py]
            [libpython-clj2.require :refer [require-python]]))

(py/initialize!)

(require-python '[PySide6.QtCore :as QtCore :bind-ns])
(require-python '[PySide6.QtWidgets :as QtWidgets :bind-ns])
(require-python '[PySide6.QtGui :as QtGui :bind-ns])

(def QTimer (py/get-attr QtCore "QTimer"))

(defonce ^:private tag-registry (clojure.core/atom {}))

(defn register-tag!
  "Register a tag keyword to a Python class."
  [tag py-class]
  (swap! tag-registry assoc tag py-class))

(defn- tag-key [tag]
  (cond
    (keyword? tag) tag
    (symbol? tag) (keyword (name tag))
    (string? tag) (keyword tag)
    :else (keyword (str tag))))

(defn- tag-name [tag]
  (name (tag-key tag)))

(defn- try-get-attr [module name]
  (try
    (py/get-attr module name)
    (catch Exception _ nil)))

(defn- resolve-class [tag]
  (let [k (tag-key tag)
        name (tag-name k)]
    (or (get @tag-registry k)
        (try-get-attr QtWidgets name)
        (try-get-attr QtGui name)
        (try-get-attr QtCore name)
        (throw (ex-info (str "Unknown Qt class tag: " name) {:tag tag})))))

(defn- layout-tag? [tag]
  (str/ends-with? (tag-name tag) "Layout"))

(defn- kebab->camel [s]
  (let [parts (str/split s #"-")
        head (first parts)
        tail (map str/capitalize (rest parts))]
    (apply str head tail)))

(defn- setter-name [k]
  (let [camel (kebab->camel (name k))]
    (str "set" (str (str/upper-case (subs camel 0 1)) (subs camel 1)))))

(defn- style->str [v]
  (cond
    (string? v) v
    (map? v) (->> v
                  (map (fn [[k val]]
                         (str (name k) ":" val ";")))
                  (apply str))
    :else (str v)))

(defn- event-key? [k]
  (and (keyword? k)
       (str/starts-with? (name k) "on-")))

(defn- event-signal-name [k]
  (kebab->camel (subs (name k) 3)))

(defn- normalize-children [children]
  (mapcat (fn [child]
            (cond
              (nil? child) []
              (vector? child) [child]
              (sequential? child) child
              (or (string? child) (number? child)) [[:QLabel {:text (str child)}]]
              :else []))
          children))

(defn- parse-element [element]
  (let [[tag & more] element
        props? (map? (first more))
        props (when props? (first more))
        children (if props? (rest more) more)]
    {:tag tag :props props :props? props? :children children}))

(defn- invoke-component [f props props? children]
  (if props?
    (apply f props children)
    (apply f children)))

(declare element->vnode)

(defn- element->vnode [element]
  (cond
    (nil? element) nil
    (vector? element)
    (let [{:keys [tag props props? children]} (parse-element element)]
      (cond
        (fn? tag)
        (element->vnode (invoke-component tag props props? children))

        (= (tag-key tag) :stretch)
        {:kind :stretch
         :value (let [v (first children)]
                  (if (number? v) v 1))}

        (= (tag-key tag) :<>)
        {:kind :fragment
         :children (->> (normalize-children children)
                        (map element->vnode)
                        (remove nil?)
                        vec)}

        :else
        (let [layout-tag (:layout props)
              content-el (:content props)
              content-vnode (when content-el (element->vnode content-el))
              key (:key props)
              props' (dissoc props :layout :key :content)
              child-elems (normalize-children children)
              layout-node (when layout-tag
                            (element->vnode (into [layout-tag] child-elems)))
              children' (if layout-tag
                          (if layout-node [layout-node] [])
                          (->> child-elems
                               (map element->vnode)
                               (remove nil?)
                               vec))]
          {:kind (if (layout-tag? tag) :layout :widget)
           :tag tag
           :key key
           :props props'
           :children children'
           :content content-vnode})))

    (sequential? element)
    {:kind :fragment
     :children (->> element
                    (map element->vnode)
                    (remove nil?)
                    vec)}

    (or (string? element) (number? element))
    (element->vnode [:QLabel {:text (str element)}])

    :else nil))

(defn- fragment? [node]
  (= (:kind node) :fragment))

(defn- flatten-fragments [nodes]
  (mapcat (fn [node]
            (if (fragment? node)
              (flatten-fragments (:children node))
              [node]))
          nodes))

(def ^:dynamic *ratom-context* nil)

(defn- notify-watches! [watches ref old-val new-val]
  (doseq [[k f] @watches]
    (try
      (f k ref old-val new-val)
      (catch Exception _ nil))))

(deftype RAtom [state watches]
  clojure.lang.IDeref
  (deref [this]
    (when *ratom-context*
      (swap! *ratom-context* conj this))
    @state)

  clojure.lang.IRef
  (addWatch [this key f]
    (swap! watches assoc key f)
    this)
  (removeWatch [this key]
    (swap! watches dissoc key)
    this)

  clojure.lang.IAtom
  (swap [this f]
    (let [old @state
          new (swap! state f)]
      (notify-watches! watches this old new)
      new))
  (swap [this f x]
    (let [old @state
          new (swap! state f x)]
      (notify-watches! watches this old new)
      new))
  (swap [this f x y]
    (let [old @state
          new (swap! state f x y)]
      (notify-watches! watches this old new)
      new))
  (swap [this f x y args]
    (let [old @state
          new (if (seq args)
                (apply swap! state f x y args)
                (swap! state f x y))]
      (notify-watches! watches this old new)
      new))
  (reset [this newv]
    (let [old @state
          new (reset! state newv)]
      (notify-watches! watches this old new)
      new))
  (compareAndSet [this oldv newv]
    (let [ok (.compareAndSet ^clojure.lang.Atom state oldv newv)]
      (when ok
        (notify-watches! watches this oldv newv))
      ok)))

(defn atom
  "Create a reactive atom that tracks deref dependencies during render."
  [value]
  (RAtom. (clojure.core/atom value) (clojure.core/atom {})))

(defn- run-tracked [f]
  (let [deps (clojure.core/atom #{})
        value (binding [*ratom-context* deps]
                (f))]
    {:value value :deps @deps}))

(defn- ui-dispatch! [f]
  (let [cb (py/make-callable (fn []
                               (try
                                 (f)
                                 (catch Exception e
                                   (println "ui-dispatch error:" e)))
                               nil))]
    (py/call-attr QTimer "singleShot" 0 cb)))

(defn- set-prop! [widget k v]
  (cond
    (= k :items)
    (try
      (py/call-attr widget "clear")
      (py/call-attr widget "addItems" (py/->py-list (or v [])))
      (catch Exception _ nil))
    (= k :contents-margins)
    (when (sequential? v)
      (let [vals (vec v)]
        (when (= 4 (count vals))
          (apply py/call-attr widget "setContentsMargins" vals))))
    (= k :widget-resizable)
    (try
      (py/call-attr widget "setWidgetResizable" (boolean v))
      (catch Exception _ nil))
    (= k :fixed-height)
    (try
      (py/call-attr widget "setFixedHeight" (int v))
      (catch Exception _ nil))
    (= k :fixed-width)
    (try
      (py/call-attr widget "setFixedWidth" (int v))
      (catch Exception _ nil))
    (= k :style) (py/call-attr widget "setStyleSheet" (style->str v))
    (= k :qss) (py/call-attr widget "setStyleSheet" (style->str v))
    (= k :ref) nil
    :else (let [setter (setter-name k)]
            (try
              (py/call-attr widget setter v)
              (catch Exception _
                (try
                  (py/call-attr widget "setProperty" (name k) v)
                  (catch Exception _ nil)))))))

(defn- apply-props! [widget old-props new-props]
  (when (contains? new-props :items)
    (let [v (get new-props :items)]
      (when (not= (get old-props :items) v)
        (set-prop! widget :items v))))
  (doseq [[k v] new-props]
    (when (and (not= k :items)
               (not= (get old-props k) v))
      (set-prop! widget k v))))

(defn- connect-event! [widget k handler]
  (let [signal-name (event-signal-name k)
        signal (py/get-attr widget signal-name)
        cb (py/make-callable (fn [& args]
                               (apply handler args)
                               nil))]
    (py/call-attr signal "connect" cb)
    {:signal signal :callback cb :handler handler}))

(defn- update-events! [widget old-events new-props]
  (let [new-handlers (into {} (filter (fn [[k _]] (event-key? k)) new-props))
        kept (clojure.core/atom {})]
    (doseq [[k {:keys [signal callback handler] :as entry}] old-events]
      (let [new-handler (get new-handlers k)]
        (if (identical? handler new-handler)
          (swap! kept assoc k entry)
          (try
            (py/call-attr signal "disconnect" callback)
            (catch Exception _ nil)))))
    (doseq [[k handler] new-handlers]
      (when-not (get @kept k)
        (swap! kept assoc k (connect-event! widget k handler))))
    @kept))

(defn- create-instance [tag parent]
  (let [klass (resolve-class tag)]
    (try
      (if parent
        (klass parent)
        (klass))
      (catch Exception _
        (klass)))))

(defn- layout-add-child! [layout child]
  (if (= (:kind child) :layout)
    (py/call-attr layout "addLayout" (:instance child))
    (py/call-attr layout "addWidget" (:instance child))))

(declare mount-vnode)

(defn- wrap-layout-vnode [layout-vnode]
  (element->vnode (into [:QWidget {:layout (:tag layout-vnode)}]
                        (:children layout-vnode))))

(defn- normalize-content-vnode [content-vnode]
  (cond
    (nil? content-vnode) nil
    (= (:kind content-vnode) :layout) (wrap-layout-vnode content-vnode)
    (= (:kind content-vnode) :fragment) (first (flatten-fragments (:children content-vnode)))
    :else content-vnode))

(defn- mount-layout-in-layout [parent-layout vnode]
  (let [layout (create-instance (:tag vnode) nil)
        _ (apply-props! layout {} (:props vnode))
        child-nodes (->> (:children vnode)
                         flatten-fragments
                         (map #(mount-vnode layout %))
                         (remove nil?)
                         vec)]
    (layout-add-child! parent-layout {:kind :layout :instance layout})
    {:kind :layout
     :tag (:tag vnode)
     :props (:props vnode)
     :instance layout
     :children child-nodes}))

(defn- mount-layout-on-widget [widget vnode]
  (let [layout (create-instance (:tag vnode) nil)
        _ (apply-props! layout {} (:props vnode))
        _ (py/call-attr widget "setLayout" layout)
        child-nodes (->> (:children vnode)
                         flatten-fragments
                         (map #(mount-vnode layout %))
                         (remove nil?)
                         vec)]
    {:kind :layout
     :tag (:tag vnode)
     :props (:props vnode)
     :instance layout
     :children child-nodes}))

(defn- mount-widget [parent-layout vnode]
  (let [widget (create-instance (:tag vnode) nil)
        props (:props vnode)
        event-props (into {} (filter (fn [[k _]] (event-key? k)) props))
        normal-props (into {} (remove (fn [[k _]] (event-key? k)) props))
        _ (apply-props! widget {} normal-props)
        events (reduce-kv (fn [m k v] (assoc m k (connect-event! widget k v)))
                          {}
                          event-props)
        _ (when parent-layout
            (layout-add-child! parent-layout {:kind :widget :instance widget}))
        layout-child (first (filter #(= (:kind %) :layout) (:children vnode)))
        layout-node (when layout-child
                      (mount-layout-on-widget widget layout-child))
        content-vnode (normalize-content-vnode (:content vnode))
        content-node (when content-vnode
                       (mount-vnode nil content-vnode))]
    (when content-node
      (py/call-attr widget "setWidget" (:instance content-node)))
    (when-let [ref-fn (:ref props)]
      (when (fn? ref-fn)
        (ref-fn widget)))
    {:kind :widget
     :tag (:tag vnode)
     :props props
     :instance widget
     :events events
     :layout layout-node
     :content content-node}))

(defn- mount-vnode [parent-layout vnode]
  (when vnode
    (case (:kind vnode)
      :layout (mount-layout-in-layout parent-layout vnode)
      :widget (mount-widget parent-layout vnode)
      :stretch (do
                 (when parent-layout
                   (py/call-attr parent-layout "addStretch" (:value vnode)))
                 vnode)
      :fragment (->> (:children vnode)
                     flatten-fragments
                     (map #(mount-vnode parent-layout %))
                     (remove nil?)
                     vec)
      nil)))

(defn- clear-layout! [layout]
  (loop []
    (let [count (py/call-attr layout "count")]
      (when (pos? count)
        (py/call-attr layout "takeAt" 0)
        (recur)))))

(defn- unmount-node [node]
  (when node
    (cond
      (vector? node) (doseq [n node] (unmount-node n))
      (= (:kind node) :widget)
      (do
        (when-let [layout (:layout node)]
          (unmount-node layout))
        (when-let [content (:content node)]
          (unmount-node content))
        (doseq [[_ {:keys [signal callback]}] (:events node)]
          (try
            (py/call-attr signal "disconnect" callback)
            (catch Exception _ nil)))
        (py/call-attr (:instance node) "deleteLater"))
      (= (:kind node) :layout)
      (do
        (doseq [child (:children node)]
          (unmount-node child))
        (clear-layout! (:instance node))
        (py/call-attr (:instance node) "deleteLater"))
      (= (:kind node) :stretch) nil
      :else nil)))

(declare reconcile)

(defn- reconcile-children [parent-layout old-children new-children]
  (let [new-children (vec (flatten-fragments new-children))
        old-children (vec (or old-children []))
        old-count (count old-children)
        new-count (count new-children)
        keep-count (min old-count new-count)
        updated (transient [])]
    (dotimes [i keep-count]
      (conj! updated (reconcile parent-layout
                                (nth old-children i)
                                (nth new-children i))))
    (when (> old-count new-count)
      (doseq [i (range (dec old-count) (dec new-count) -1)]
        (when parent-layout
          (try
            (py/call-attr parent-layout "takeAt" i)
            (catch Exception _ nil)))
        (unmount-node (nth old-children i))))
    (when (> new-count old-count)
      (doseq [i (range old-count new-count)]
        (conj! updated (mount-vnode parent-layout (nth new-children i)))))
    (persistent! updated)))

(defn- update-layout [_ old-node new-vnode]
  (let [layout (:instance old-node)]
    (apply-props! layout (:props old-node) (:props new-vnode))
    (let [new-children (reconcile-children layout
                                           (:children old-node)
                                           (:children new-vnode))]
      (assoc old-node :props (:props new-vnode) :children new-children))))

(defn- update-widget [parent-layout old-node new-vnode]
  (let [widget (:instance old-node)
        props (:props new-vnode)
        event-props (into {} (filter (fn [[k _]] (event-key? k)) props))
        normal-props (into {} (remove (fn [[k _]] (event-key? k)) props))
        old-normal-props (into {} (remove (fn [[k _]] (event-key? k)) (:props old-node)))]
    (apply-props! widget old-normal-props normal-props)
    (let [updated-events (update-events! widget (:events old-node) props)
          new-layout (first (filter #(= (:kind %) :layout) (:children new-vnode)))
          old-layout (:layout old-node)
          layout-node (cond
                        (and old-layout new-layout
                             (= (:tag old-layout) (:tag new-layout)))
                        (update-layout widget old-layout new-layout)

                        new-layout
                        (do
                          (when old-layout
                            (unmount-node old-layout))
                          (mount-layout-on-widget widget new-layout))

                        :else
                        (do
                          (when old-layout
                            (unmount-node old-layout))
                          nil))]
      (let [new-content-vnode (normalize-content-vnode (:content new-vnode))
            old-content (:content old-node)
            content-node (cond
                           (and old-content new-content-vnode)
                           (reconcile nil old-content new-content-vnode)

                           (and new-content-vnode (nil? old-content))
                           (mount-vnode nil new-content-vnode)

                           (and old-content (nil? new-content-vnode))
                           (do
                             (unmount-node old-content)
                             nil)

                           :else old-content)]
        (when content-node
          (try
            (py/call-attr widget "setWidget" (:instance content-node))
            (catch Exception _ nil)))
        (assoc old-node
               :props props
               :events updated-events
               :layout layout-node
               :content content-node)))))

(defn- reconcile [parent-layout old-node new-vnode]
  (cond
    (nil? new-vnode) (do (unmount-node old-node) nil)
    (nil? old-node) (mount-vnode parent-layout new-vnode)
    (vector? old-node) (do (unmount-node old-node)
                           (mount-vnode parent-layout new-vnode))
    (not= (:kind old-node) (:kind new-vnode)) (do (unmount-node old-node)
                                                  (mount-vnode parent-layout new-vnode))
    (not= (:tag old-node) (:tag new-vnode)) (do (unmount-node old-node)
                                                (mount-vnode parent-layout new-vnode))
    (= (:kind old-node) :layout) (update-layout parent-layout old-node new-vnode)
    (= (:kind old-node) :widget) (update-widget parent-layout old-node new-vnode)
    :else old-node))

(defn mount!
  "Mount a Hiccup element into a root QWidget. Returns a mount map."
  [root element]
  (let [root-layout (create-instance :QVBoxLayout nil)
        _ (py/call-attr root "setLayout" root-layout)
        mount (clojure.core/atom {:root root
                     :layout root-layout
                     :element element
                     :tree (clojure.core/atom nil)
                     :deps (clojure.core/atom #{})
                     :pending? (clojure.core/atom false)
                     :watch-key (gensym "qt-hiccup")})
        schedule! (fn []
                    (let [pending? (:pending? @mount)]
                      (when (compare-and-set! pending? false true)
                        (ui-dispatch!
                         (fn []
                           (reset! pending? false)
                           ((:render! @mount)))))))
        render! (fn []
                  (let [{:keys [value deps]} (run-tracked
                                              (fn []
                                                (element->vnode
                                                 (if (vector? element) element [element]))))
                        old-deps @(:deps @mount)]
                    (doseq [dep (set/difference old-deps deps)]
                      (remove-watch dep (:watch-key @mount)))
                    (doseq [dep (set/difference deps old-deps)]
                      (add-watch dep (:watch-key @mount) (fn [& _] (schedule!))))
                    (reset! (:deps @mount) deps)
                    (swap! (:tree @mount)
                           (fn [old]
                             (reconcile root-layout old value)))))]
    (swap! mount assoc :render! render!)
    (render!)
    @mount))

(defn unmount!
  "Unmount a mounted tree."
  [mount]
  (when mount
    (doseq [dep @(:deps mount)]
      (remove-watch dep (:watch-key mount)))
    (unmount-node @(:tree mount))
    (reset! (:tree mount) nil)))

(defn flush!
  "Force a synchronous render for a mount."
  [mount]
  (when mount
    ((:render! mount))))
