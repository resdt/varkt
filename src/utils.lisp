(require 'cl-csv)
(require 'cmu-infix)

(named-readtables:in-readtable cmu-infix:syntax)


(defconstant TMP-FOLD "tmp")
(defconstant PLOT-TABLE-PATH (pathname (format nil "~a/plot-data.csv" TMP-FOLD)))

;; Global constants
(defconstant G (* 6.6743  ; Gravitational constant
                  (expt 10 -11)))
(defconstant R_EARTH 6378100)  ; Earth radius
(defconstant M_EARTH (* 5.9742  ; Earth mass
                        (expt 10 24)))
(defconstant ENV_RES 0.4)  ; Environment resistance coefficient
(defconstant M_MASS_AIR 0.029)  ; Molar air mass
(defconstant R 8.314)  ; Universal gas constant

;; Initial values
(defconstant M0_ROCKET 344040)  ; Rocket mass
(defconstant M0_FUEL 284000)  ; Fuel mass
(defconstant T_FUEL 253)  ; Time for which the fuel will last
(defconstant S_ROCKET 13.28)  ; Surface area of ​​the rocket affected by the environment
(defconstant THAU 104)  ; Flight duration
(defconstant RHO0 1.225)  ; Density
(defconstant THRUST 41520000)  ; Engine thrust
(defconstant T0_AIR 288)  ; Air temperature (considered constant)

(defun write-flight-log (output-dir)
  (let ((output-dir (pathname output-dir))
        (plot-data '(("Time" "ax" "ay"
                      "vx" "vy" "Height"
                      "Mass" "Density")))
        (out-data '(("Time" "Velocity" "Acceleration"
                     "Mass" "Density"))))

    (loop for time from 0 to THAU
          with m = M0_ROCKET
          and h = 0
          and a = 0 and ax = 0 and ay = 0
          and v = 0 and vx = 0 and vy = 0
          and density = RHO0

          for cur_g = #I(M_EARTH * G / (R_EARTH+h)^^2)
          and alpha = #I(pi/2 - pi*time/300)

          do (setf plot-data (append plot-data
                                     (list (list time ax ay vx vy h m density)))
                   out-data (append out-data
                                    (list (list time v a m h)))
                   ax #I((cos(alpha) * THRUST -
                             ENV_RES * density * vx^^2 * S_ROCKET / 2)
                         / m)
                   ay #I((sin(alpha) * THRUST -
                             ENV_RES * density * vy^^2 * S_ROCKET / 2 -
                             G * m * M_EARTH / (R_EARTH+h)^^2)
                         / m)
                   density #I(RHO0 * exp(-M_MASS_AIR * cur_g * h / (R*T0_AIR)))
                   vx #I(vx + ax)
                   vy #I(vy + ay)
                   v #I(sqrt(vx^^2 + vy^^2))
                   a #I(sqrt(ax^^2 + ay^^2))
                   m #I(M0_ROCKET - M0_FUEL*time/T_FUEL)
                   h #I(h + vy)))

    (cl-csv:write-csv plot-data
                      :stream PLOT-TABLE-PATH)
    (cl-csv:write-csv out-data
                      :stream output-dir)))
