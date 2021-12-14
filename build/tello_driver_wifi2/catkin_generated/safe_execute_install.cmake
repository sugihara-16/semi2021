execute_process(COMMAND "/home/mech-user/semi_ws/build/tello_driver_wifi2/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/mech-user/semi_ws/build/tello_driver_wifi2/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
