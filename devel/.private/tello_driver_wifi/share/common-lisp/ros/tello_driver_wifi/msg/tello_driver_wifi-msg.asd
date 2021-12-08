
(cl:in-package :asdf)

(defsystem "tello_driver_wifi-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "TelloStatus" :depends-on ("_package_TelloStatus"))
    (:file "_package_TelloStatus" :depends-on ("_package"))
  ))