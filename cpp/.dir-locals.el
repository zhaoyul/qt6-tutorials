((c++-mode
  . ((eval . (let* ((file (buffer-file-name))
                    (dir (and file (file-name-directory file))))
               (when (and file (string= (file-name-nondirectory file) "main.cpp"))
                 (let* ((root (or (locate-dominating-file dir ".git")
                                  (locate-dominating-file dir "CMakeLists.txt")
                                  dir))
                        (cmake (expand-file-name "CMakeLists.txt" dir))
                        (target (when (file-readable-p cmake)
                                  (with-temp-buffer
                                    (insert-file-contents cmake)
                                    (goto-char (point-min))
                                    (when (re-search-forward
                                           "add_executable\\s-*(\\s-*\\([^ )\n]+\\)"
                                           nil t)
                                      (match-string 1))))))
                   (when target
                     (let* ((rel (file-relative-name dir root))
                            (build (expand-file-name "build" root))
                            (exe (expand-file-name target
                                                   (expand-file-name rel build))))
                       (setq-local compile-command
                                   (format "cmake --build %s --target %s -j 8 && %s"
                                           (shell-quote-argument build)
                                           target
                                           (shell-quote-argument exe)))
                       (message "dir-locals: file=%s target=%s compile=%s"
                                file target compile-command))))))))))
